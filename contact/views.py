# -*- coding: utf-8 -*-
from .serializers import ContactBuySerializer, ContactRentSerializer, ContactSellSerializer
from admin_data.models import AdminData
from backend.utils import get_list_social_links_images, send_email
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from newsletter.models import Newsletter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from settings_db.models import SettingsDb
from sociallink.views import get_list_social_links
import datetime


@api_view(['POST'])
def contact_sell_create(request):
    """
    Create a contact entry for selling a property.
    """
    if request.method == 'POST':
        data = request.data
        if data.get("email") and (data.get("first_name") or data.get("last_name")) and not Newsletter.objects.filter(
                email=data["email"]
        ).exists():
            Newsletter.objects.create(
                email=data["email"],
                first_name=data["first_name"] or data["last_name"],
                last_name=data["last_name"] or data["first_name"]
            )
        serializer = ContactSellSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            context = {
                "email": data['email'],
                "environment": settings.ENVIRONMENT,
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "logo_url": settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg"),
                "message": data['message'],
                "site_name": SettingsDb.get_site_name(),
                "site_url_root": settings.SITE_URL_ROOT,
                "show_unsubscribe_url": True,
                "social_links": get_list_social_links(),
                "social_links_images": get_list_social_links_images(),
                "phone": data.get('phone', "")
            }
            html_content = get_template('contact/contact_template.html').render(context)
            text_content = get_template('contact/contact_template.txt').render(context)
            send_email(data["object"], text_content, data["email"], AdminData.get_admin_email(), html_content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contact_buy_create(request):
    """
    Create a contact entry for buying a property.
    """
    data = request.data.copy()
    if data.get("email") and (data.get("first_name") or data.get("last_name")) and not Newsletter.objects.filter(
            email=data["email"]
    ).exists():
        Newsletter.objects.create(
            email=data["email"],
            first_name=data["first_name"] or data["last_name"],
            last_name=data["last_name"] or data["first_name"]
        )
    if not data.get("lot_size_max", ""):
        data["lot_size_max"] = 0
        data["lot_size_min"] = 0
    if not data.get("lot_size_min", ""):
        data["lot_size_min"] = 0
    try:
        data["occupation_date"] = datetime.datetime.strptime(data.get("occupation_date"), "%d-%m-%Y").date()
    except:
        data["occupation_date"] = None
    serializer = ContactBuySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        context = {
            "email": data['email'],
            "environment": settings.ENVIRONMENT,
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "logo_url": settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg"),
            "phone": data.get('phone', ""),
            "property_information": [
                (_("Nombre de salles de bain"), data.get('bathrooms_number_text', "")
                if data.get('bathrooms_number', "") else ""),
                (_("Nombre de chambres"), data.get('bedrooms_number_text', "")
                if data.get('bedrooms_number', "") else ""),
                (_("Type de bâtiment"), data.get('building_type_text', "") if data.get('building_type', "") else ""),
                (_("Ville"), data.get('city_text', "") if data.get('city', "") else ""),
                (_("Âge de construction"), data.get('construction_age_text', "")
                if data.get('construction_age', "") else ""),
                (_("Salle à manger"), data.get('has_dining_room', False)),
                (_("Cheminée"), data.get('has_fireplace', False)),
                (_("Garage"), data.get('has_garage', False)),
                (_("Jardin"), data.get('has_garden', False)),
                (_("Taille de la propriété maximale"), str(data['lot_size_max'])
                    if int(data.get('lot_size_max', 0)) > 0 else ""),
                (_("Taille de la propriété minimale"), str(data['lot_size_min'])
                    if int(data.get('lot_size_min', 0)) > 0 else ""),
                (_("Intervalle de prix"), data.get('price_range_text', "") if data.get('price_range', "") else ""),
                (_("Type de la Propriété"), data.get('property_type_text', "") if  data.get('property_type', "") else ""),
                (_("Date d'occupation"), data.get('occupation_date', "")),
                (_("Autres caractéristiques"), data.get('other_characteristics', "")),
                (_("Statut"), data.get('status_text', "")),
                (_("Piscine"), data.get('has_swimming_pool', False))
            ],
            "site_name": SettingsDb.get_site_name(),
            "site_url_root": settings.SITE_URL_ROOT,
            "show_unsubscribe_url": True,
            "social_links": get_list_social_links(),
            "social_links_images": get_list_social_links_images()
        }
        html_content = get_template('contact/contact_buying_template.html').render(context)
        text_content = get_template('contact/contact_buying_template.txt').render(context)
        send_email(_("Achat d'une propriété"), text_content, data["email"], AdminData.get_admin_email(), html_content)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contact_rent_create(request):
    """
    Create a contact entry for rent a property.
    """
    data = request.data.copy()
    if data.get("email") and (data.get("first_name") or data.get("last_name")) and not Newsletter.objects.filter(
            email=data["email"]
    ).exists():
        Newsletter.objects.create(
            email=data["email"],
            first_name=data["first_name"] or data["last_name"],
            last_name=data["last_name"] or data["first_name"]
        )
    if not data.get("lot_size_max", ""):
        data["lot_size_max"] = 0
        data["lot_size_min"] = 0
    if not data.get("lot_size_min", ""):
        data["lot_size_min"] = 0
    try:
        data["occupation_date"] = datetime.datetime.strptime(data.get("occupation_date"), "%d-%m-%Y").date()
    except:
        data["occupation_date"] = None
    serializer = ContactRentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        context = {
            "email": data['email'],
            "environment": settings.ENVIRONMENT,
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "logo_url": settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg"),
            "phone": data.get('phone', ""),
            "property_information": [
                (_("Nombre de salles de bain"), data.get('bathrooms_number_text', "")
                if data.get('bathrooms_number', "") else ""),
                (_("Nombre de chambres"), data.get('bedrooms_number_text', "")
                if data.get('bedrooms_number', "") else ""),
                (_("Type de bâtiment"), data.get('building_type_text', "") if data.get('building_type', "") else ""),
                (_("Ville"), data.get('city_text', "") if data.get('city', "") else ""),
                (_("Âge de construction"), data.get('construction_age_text', "")
                if data.get('construction_age', "") else ""),
                (_("Salle à manger"), data.get('has_dining_room', False)),
                (_("Cheminée"), data.get('has_fireplace', False)),
                (_("Garage"), data.get('has_garage', False)),
                (_("Jardin"), data.get('has_garden', False)),
                (_("Taille de la propriété maximale"), str(data['lot_size_max'])
                    if int(data.get('lot_size_max', 0)) > 0 else ""),
                (_("Taille de la propriété minimale"), str(data['lot_size_min'])
                    if int(data.get('lot_size_min', 0)) > 0 else ""),
                (_("Intervalle de prix"), data.get('price_range_text', "") if data.get('price_range', "") else ""),
                (_("Type de la Propriété"), data.get('property_type_text', "") if  data.get('property_type', "") else ""),
                (_("Date d'occupation"), data.get('occupation_date', "")),
                (_("Autres caractéristiques"), data.get('other_characteristics', "")),
                (_("Statut"), data.get('status_text', "")),
                (_("Piscine"), data.get('has_swimming_pool', False))
            ],
            "site_name": SettingsDb.get_site_name(),
            "site_url_root": settings.SITE_URL_ROOT,
            "show_unsubscribe_url": True,
            "social_links": get_list_social_links(),
            "social_links_images": get_list_social_links_images()
        }
        html_content = get_template('contact/contact_renting_template.html').render(context)
        text_content = get_template('contact/contact_renting_template.txt').render(context)
        send_email(_("location d'une propriété"), text_content, data["email"], AdminData.get_admin_email(), html_content)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contact(request):
    """
    send mail from client to administrator.
    """
    if request.method == 'POST':
        data = request.data
        if data.get("email") and (data.get("first_name") or data.get("last_name")) and not Newsletter.objects.filter(
                email=data["email"]
        ).exists():
            Newsletter.objects.create(
                email=data["email"],
                first_name=data["first_name"] or data["last_name"],
                last_name=data["last_name"] or data["first_name"]
            )
        context = {
            "email": data['email'],
            "environment": settings.ENVIRONMENT,
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "logo_url": settings.BACKEND_URL_ROOT + static("contact/images/logo.jpg"),
            "message": data['message'],
            "site_name": SettingsDb.get_site_name(),
            "site_url_root": settings.SITE_URL_ROOT,
            "show_unsubscribe_url": True,
            "social_links": get_list_social_links(),
            "social_links_images": get_list_social_links_images(),
            "phone": data.get('phone', ""),
            "property_url": data.get('property_url', '')
        }
        html_content = get_template('contact/contact_template.html').render(context)
        text_content = get_template('contact/contact_template.txt').render(context)
        send_email(data["object"], text_content, data["email"], AdminData.get_admin_email(), html_content)
        return Response({
            "success": True
        })
