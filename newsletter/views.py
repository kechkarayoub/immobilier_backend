# -*- coding: utf-8 -*-


from .models import Newsletter
from .serializers import NewsletterSerializer
from backend.utils import send_email, get_list_social_links_images
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from settings_db.models import SettingsDb
from sociallink.views import get_list_social_links


@api_view(['POST'])
def newsletter_create(request):
    """
    user subscription to the newsletter.
    """
    data = request.data
    already_exists = False
    subscription = Newsletter.objects.filter(email=data["email"])
    if subscription.exists():
        subscription = subscription[0]
        if Newsletter.objects.filter(
            email=data["email"],
            is_active=True,
            first_name=data["first_name"],
            last_name=data["last_name"]
        ).exists():
            pass
        else:
            if not subscription.is_active:
                response_type = "reactivated"
            else:
                response_type = "updated"
            already_exists = True
            Newsletter.objects.filter(email=data["email"]).update(
                is_active=True,
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
    if not already_exists:
        serializer = NewsletterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_type = "created"
        else:
            response_type = "conflict"
    if response_type != "conflict":
        footer_text_content = get_template('newsletter/footer_email.txt').render({
            "unsubscribe_url": "{site_url_root}/#/newsletter/unsubscribe/{user_email}".format(
                site_url_root=settings.SITE_URL_ROOT, user_email=data["email"]
            )
        })
        context = {
            "environment": settings.ENVIRONMENT,
            "first_name": data['first_name'],
            "footer_text_content": footer_text_content,
            "last_name": data['last_name'],
            "logo_url": settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg"),
            "site_name": SettingsDb.get_site_name(),
            "site_url_root": settings.SITE_URL_ROOT,
            "social_links": get_list_social_links(),
            "social_links_images": get_list_social_links_images(),
            "unsubscribe_url": "{site_url_root}/#/newsletter/unsubscribe/{user_email}".format(
                site_url_root=settings.SITE_URL_ROOT, user_email=data["email"]
            ),
            "show_unsubscribe_url": True
        }
        html_content = get_template('newsletter/subscription_template.html').render(context)
        text_content = get_template('newsletter/subscription_template.txt').render(context)
        send_email(
            _("Subscription to the newsletter"),
            text_content,
            settings.EMAIL_HOST_USER,
            data["email"],
            html_content
        )
        if response_type in ["updated", "reactivated"]:
            return Response({
                "response_type": response_type
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "data": serializer.data,
                "response_type": response_type
            }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
def newsletter_unsubscribe(request):
    """
    user unsubscription from the newsletter.
    """
    user_email = request.GET.get("user_email")
    if not Newsletter.objects.filter(email=user_email).exists():
        response = {
            "success": False,
            "message": _("Sorry, you haven't any subscription in our newsletter!"),
        }
    else:
        subscription = Newsletter.objects.get(email=user_email)
        if subscription.is_active:
            Newsletter.objects.filter(email=user_email).update(is_active=False)
            context = {
                "environment": settings.ENVIRONMENT,
                "first_name": subscription.first_name,
                "last_name": subscription.last_name,
                "logo_url": settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg"),
                "resubscribe_url": "{site_url_root}/#/newsletter/resubscribe/{user_email}".format(
                    site_url_root=settings.SITE_URL_ROOT, user_email=subscription.email
                ),
                "site_name": SettingsDb.get_site_name(),
                "site_url_root": settings.SITE_URL_ROOT,
                "show_unsubscribe_url": True,
                "social_links": get_list_social_links(),
                "social_links_images": get_list_social_links_images()
            }
            html_content = get_template('newsletter/unsubscription_template.html').render(context)
            text_content = get_template('newsletter/unsubscription_template.txt').render(context)
            send_email(
                _("Unsubscription from the newsletter"), text_content, settings.EMAIL_HOST_USER, subscription.email,
                html_content
            )
            response ={
                "success": True,
                "message": _("Your subscription is deactivated!"),
            }
        else:
            response = {
                "success": False,
                "message": _("Your subscription is already deactivated!"),
            }
    return Response({
        'data': response
    })


@api_view(['GET'])
def newsletter_resubscribe(request):
    """
    user resubscription from the newsletter.
    """
    user_email = request.GET.get("user_email")
    if not Newsletter.objects.filter(email=user_email).exists():
        response = {
            "success": False,
            "message": _("Sorry, you haven't any subscription in our newsletter!"),
        }
    else:
        subscription = Newsletter.objects.get(email=user_email)
        if not subscription.is_active:
            Newsletter.objects.filter(email=user_email).update(is_active=True)

            footer_text_content = get_template('newsletter/footer_email.txt').render({
                "unsubscribe_url": "{site_url_root}/#/newsletter/unsubscribe/{user_email}".format(
                    site_url_root=settings.SITE_URL_ROOT, user_email=subscription.email
                )
            })
            context = {
                "environment": settings.ENVIRONMENT,
                "first_name": subscription.first_name,
                "footer_text_content": footer_text_content,
                "last_name": subscription.last_name,
                "logo_url": settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg"),
                "site_name": SettingsDb.get_site_name(),
                "site_url_root": settings.SITE_URL_ROOT,
                "show_unsubscribe_url": True,
                "social_links": get_list_social_links(),
                "social_links_images": get_list_social_links_images(),
                "unsubscribe_url": "{site_url_root}/#/newsletter/unsubscribe/{user_email}".format(
                    site_url_root=settings.SITE_URL_ROOT, user_email=subscription.email
                )
            }
            html_content = get_template('newsletter/resubscription_template.html').render(context)
            text_content = get_template('newsletter/resubscription_template.txt').render(context)
            send_email(
                _("Resubscription to the newsletter"), text_content, settings.EMAIL_HOST_USER, subscription.email,
                html_content
            )
            response = {
                "success": True,
                "message": _("Your subscription is reactivated!"),
            }
        else:
            response = {
                "success": False,
                "message": _("Your subscription is already activated!"),
            }
    return Response({
        'data': response
    })
