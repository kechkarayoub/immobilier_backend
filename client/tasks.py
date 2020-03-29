from backend.celery import app
import datetime
from backend.utils import send_email
from django.conf import settings
from .models import Client
import json
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from .models import GroupClient
from settings_db.models import SettingsDb
from django.core.mail import EmailMultiAlternatives
from sociallink.views import get_list_social_links
from backend.utils import send_email, get_list_social_links_images


@app.task
def email_de_rappel_de_paiement(is_test=False, to_email_test="kechkarayoub@gmail.com"):
    logo_url = settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg")
    site_name = SettingsDb.get_site_name()
    social_links = get_list_social_links()
    social_links_images = get_list_social_links_images()
    for group_client in GroupClient.objects.filter(is_active=True):
        reminder_email_data = group_client.to_reminder_email_data()
        context = {
            "backend_url": settings.BACKEND_URL_ROOT,
            "environment": settings.ENVIRONMENT,
            "logo_url": logo_url,
            "message_1": reminder_email_data['message_1'],
            "message_2": reminder_email_data['message_2'],
            "message_3": reminder_email_data['message_3'],
            "footer_1": reminder_email_data['footer_1'],
            "footer_2": reminder_email_data['footer_2'],
            "site_name": site_name,
            "site_url_root": settings.SITE_URL_ROOT,
            "social_links": social_links,
            "social_links_images": social_links_images,
        }
        html_content = get_template('client/payment_reminder_email.html').render(context)
        text_content = get_template('client/payment_reminder_email.txt').render(context)
        if is_test:
            # f = open("/home/ubuntu/log_backend/test_log.txt", "w+")
            # f.write("hfgfhfhfh \r\n")
            # f.write("This is line {}\r\n".format(str(is_test)))
            # f.write("This is line {}\r\n".format(to_email_test))
            clients_emails = [to_email_test if to_email_test else "kechkarayoub@gmail.com"]
            # f.close()
        else:
            clients_emails = [
                client['email'] for client in group_client.clients.filter(is_active=True, type="locataire").values('email')
            ]
        msg = EmailMultiAlternatives(
            reminder_email_data['object'], text_content, settings.EMAIL_HOST_USER, clients_emails[0:1],
            bcc=clients_emails[1:],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        msg.send()
        # send_email("Test celery", "Celery work perfectly", settings.EMAIL_HOST_USER, "kechkarayoub@gmail.com")
