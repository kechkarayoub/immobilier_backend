# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from admin_data.models import AdminData
from backend import added_settings, static_variables
from backend.utils import choices_format_to_dict
from django.conf import settings
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from settings_db.models import SettingsDb
from sociallink.views import get_list_social_links


def global_params(request):
    return JsonResponse({
        "home_page_data": SettingsDb.get_home_page_data(),
        "realtor_data": AdminData.get_admin_data(),
        "selects_choices": {
            "CITIES": [[canadian_city[0], _(canadian_city[1])] for canadian_city in static_variables.CANADIAN_CITIES],
            "PROPERTIES_TYPES": [
                [property_type[0], _(property_type[1])] for property_type in static_variables.PROPERTIES_TYPES
            ],
            "BUILDINGS_TYPES": [
                [building_type[0], _(building_type[1])] for building_type in static_variables.BUILDINGS_TYPES
            ],
            "BEDROOMS_NUMBER": [
                [bedrooms_number[0], _(bedrooms_number[1])] for bedrooms_number in static_variables.BEDROOMS_NUMBER
            ],
            "BATHROOMS_NUMBER": [
                [bathrooms_number[0], _(bathrooms_number[1])] for bathrooms_number in static_variables.BATHROOMS_NUMBER
            ],
            "CONSTRUCTION_AGE": [
                [construction_age[0], _(construction_age[1])] for construction_age in static_variables.CONSTRUCTION_AGE
            ],
            "ITEMS_STATUS": [
                [item_status[0], _(item_status[1])] for item_status in static_variables.ITEMS_STATUS
            ],
            "PRICES_RANGES": [
                [price_range[0], _(price_range[1])] for price_range in static_variables.PRICES_RANGES
            ]
        },
        "selects_choices_dict": {
            "CITIES": choices_format_to_dict(static_variables.CANADIAN_CITIES),
            "PROPERTIES_TYPES": choices_format_to_dict(static_variables.PROPERTIES_TYPES),
            "BUILDINGS_TYPES": choices_format_to_dict(static_variables.BUILDINGS_TYPES),
            "BEDROOMS_NUMBER": choices_format_to_dict(static_variables.BEDROOMS_NUMBER),
            "BATHROOMS_NUMBER": choices_format_to_dict(static_variables.BATHROOMS_NUMBER),
            "CONSTRUCTION_AGE": choices_format_to_dict(static_variables.CONSTRUCTION_AGE),
            "ITEMS_STATUS": choices_format_to_dict(static_variables.ITEMS_STATUS),
            "PRICES_RANGES": choices_format_to_dict(static_variables.PRICES_RANGES)
        },
        "is_maps_active": added_settings.IS_MAPS_ACTIVE,
        "footer_params": {
            "socialLinks": get_list_social_links(),
            "site_name": SettingsDb.get_site_name(),
            "site_url_root": settings.SITE_URL_ROOT
        },
        "header_params": {
            "i18n": added_settings.I18N_ACTIVE,
            "langue_label": _("French"),
            "langue_url": settings.SITE_URL_ROOT,
            "realtor_data": AdminData.get_admin_data(),
            "header_settings": SettingsDb.get_header_settings()
        }

    })
