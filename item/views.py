# -*- coding: utf-8 -*-


from .models import Item, SendNewsletterAfterActivating
from .serializers import ItemSerializer
from backend.project_conf import NBR_ITEMS_PER_PAGE
from backend.static_variables import PRICES_RANGES_VALUES
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


@api_view(['GET'])
def items_list(request):
    """
    List items.
    """
    kwargs = {}
    bathrooms_number = request.GET.get("bathrooms_number", "")
    bedrooms_number = request.GET.get("bedrooms_number", "")
    building_type = request.GET.get("building_type", "")
    city = request.GET.get("city", "")
    construction_age = request.GET.get("construction_age", "")
    has_dining_room = request.GET.get("has_dining_room", "")
    has_garage = request.GET.get("has_garage", "")
    has_garden = request.GET.get("has_garden", "")
    has_fireplace = request.GET.get("has_fireplace", "")
    has_swimming_pool = request.GET.get("has_swimming_pool", "")
    item_status = request.GET.get("item_status", "")
    property_type = request.GET.get("property_type", "")
    price_range = request.GET.get("price_range", "")
    searched_txt = request.GET.get("searched_txt", "")
    if bathrooms_number:
        kwargs["bathrooms_number"] = bathrooms_number
    if bedrooms_number:
        kwargs["bedrooms_number"] = bedrooms_number
    if building_type:
        kwargs["building_type"] = building_type
    if city:
        kwargs["city"] = city
    if construction_age:
        kwargs["construction_age"] = construction_age
    if has_dining_room != "":
        kwargs["has_dining_room"] = json.loads(has_dining_room.lower())
    if has_fireplace != "":
        kwargs["has_fireplace"] = json.loads(has_fireplace.lower())
    if has_garage != "":
        kwargs["has_garage"] = json.loads(has_garage.lower())
    if has_garden != "":
        kwargs["has_garden"] = json.loads(has_garden.lower())
    if has_swimming_pool != "":
        kwargs["has_swimming_pool"] = json.loads(has_swimming_pool.lower())
    if item_status:
        kwargs["status"] = item_status
    if price_range:
        min_max = PRICES_RANGES_VALUES[price_range]
        kwargs["price__gte"] = min_max["min"]
        kwargs["price__lte"] = min_max["max"]
    if property_type:
        kwargs["property_type"] = property_type
    items = Item.objects.filter(
        Q(address__contains=searched_txt) |
        Q(description__contains=searched_txt) |
        Q(label__contains=searched_txt) |
        Q(short_description__contains=searched_txt)
    ).distinct().filter(is_active=True, **kwargs).exclude(status="sold").order_by('-createdAt')
    page = int(request.GET.get('current_page', 0)) + 1
    paginator = Paginator(items, NBR_ITEMS_PER_PAGE)
    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = ItemSerializer(data, context={'request': request}, many=True)
    # if data.has_next():
    #     next_page = data.next_page_number()
    # else:
    #     next_page = 0
    # if data.has_previous():
    #     previous_page = data.previous_page_number()
    # else:
    #     previous_page = 0

    return Response({
        'current_page': page,
        'count': paginator.count,
        'data': serializer.data,
        'numpages': paginator.num_pages
        # 'nextLink': '/api/items/?page=' + str(next_page) if next_page else '',
        # 'prevLink': '/api/items/?page=' + str(previous_page) if previous_page else ''
    })


@api_view(['GET'])
def item_details(request, pk):
    try:
        item = Item.objects.get(pk=pk, is_active=True)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item, context={'request': request})
    return Response(serializer.data)

from backend.utils import get_list_social_links_images
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail, EmailMultiAlternatives
from django.template.loader import get_template
from email.mime.image import MIMEImage
from newsletter.models import Newsletter
from settings_db.models import SettingsDb
from sociallink.views import get_list_social_links


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


@receiver(post_save, sender=Item)
@on_transaction_commit
def send_property_to_newsletters(sender, **kwargs):
    instance = kwargs['instance']
    if instance.is_active:
        instance_data = ItemSerializer(instance).data
        images_items = instance.images.all()
        is_updated = not SendNewsletterAfterActivating.objects.filter(item_id=instance.item_id).exists() and \
                     instance.is_updated
        context = {
            "backend_url": settings.BACKEND_URL_ROOT,
            "environment": settings.ENVIRONMENT,
            "logo_url": settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg"),
            "property_description": instance_data['description'],
            "property_id": instance_data['pk'],
            "property_images": images_items,
            "property_label": instance_data['label'],
            "property_short_description": instance_data['short_description'],
            "is_updated": is_updated,
            "site_name": SettingsDb.get_site_name(),
            "site_url_root": settings.SITE_URL_ROOT,
            "show_unsubscribe_url": True,
            "social_links": get_list_social_links(),
            "social_links_images": get_list_social_links_images(),
        }
        html_content = get_template('item/new_item_template.html').render(context)
        text_content = get_template('item/new_item_template.txt').render(context)
        newsletters_emails = [
            newsletter_email['email'] for newsletter_email in Newsletter.objects.filter(is_active=True).values('email')
        ]
        msg = EmailMultiAlternatives(
            _('A property has been updated' if is_updated else 'New property'), text_content,
            settings.EMAIL_HOST_USER, newsletters_emails[0:1], bcc=newsletters_emails[1:]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        for item_image in images_items:
            # Create an inline attachment
            ext = '.'+item_image.image.url.split('.')[-1]
            image = MIMEImage(item_image.image.read(), _subtype=ext)
            image.add_header('Content-ID', '<{}>'.format(item_image.image_filename))
            msg.attach(image)

        # try:
        msg.send()
        if not is_updated:
            SendNewsletterAfterActivating.objects.filter(item_id=instance.item_id).delete()
        # except Exception as e:
        #     pass