# -*- coding: utf-8 -*-
from .models import SettingsDb #ExecutedBackup,
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import admin
from django.core import management
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
import sys


def get_header_image_preview(obj):
    if obj.header_image:
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (str(obj.header_image)))
    return _("No file selected!")


def get_header_background_image_preview(obj):
    if obj.header_background_image:
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (str(obj.header_background_image)))
    return _("No file selected!")


def get_main_bg_image_preview(obj):
    if obj.main_bg_image:
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (str(obj.main_bg_image)))
    return _("No file selected!")


def get_logo_image_preview(obj):
    if obj.logo:
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (str(obj.logo)))
    return _("No file selected!")


get_header_image_preview.allow_tags = True
get_header_image_preview.short_description = _("Preview de l'image du background de l'entete")


get_header_background_image_preview.allow_tags = True
get_header_background_image_preview.short_description = _("Preview de l'image du background de l'entete")


get_main_bg_image_preview.allow_tags = True
get_main_bg_image_preview.short_description = _("Preview de l'image principale du background de l'entete")


get_logo_image_preview.allow_tags = True
get_logo_image_preview.short_description = _("Preview du l'image du logo")


class SettingsDbAdmin(TranslationAdmin):

    class Media:
        js = (
            'settings_db/js/settings_db_form.js',
        )
    list_display = ('__str__',)
    fieldsets = [
        (_("Paramètres générals"), {
            'fields': ['main_bg_image', get_main_bg_image_preview]
        }),
        (_("Paramètres de l'entete"), {
            'fields': [
                'site_name', 'header_background_image', get_header_background_image_preview, 'header_image',
                get_header_image_preview, "header_text_color", "logo", get_logo_image_preview
            ]
        }),
        (_("E-mail de rappel de paiement"), {
            'fields': [
                'reminder_payment_email_object', 'reminder_payment_email_message1', 'reminder_payment_email_message2',
                'reminder_payment_email_message3', "reminder_payment_email_footer_line1",
                'reminder_payment_email_footer_line2'
            ]
        }),
        (_("Paramètres de la page d'accueil"), {
            'fields': [
                'home_page_title_1', 'home_page_title_2', 'home_page_row_1_title', 'home_page_row_1_p_1',
                'home_page_row_1_p_2', 'home_page_row_1_p_3', 'home_page_row_2_title', 'home_page_row_2_p_1',
                'home_page_row_2_p_2', 'home_page_row_2_p_3', 'home_page_row_3_title', 'home_page_row_3_p_1',
                'home_page_row_3_p_2', 'home_page_row_3_p_3'
            ]
        }),
    ]
    readonly_fields = [
        get_header_background_image_preview, get_header_image_preview, get_main_bg_image_preview, get_logo_image_preview
    ]

    def save_model(self, request, obj, form, change):
        if len(SettingsDb.objects.all()) > 0:
            SettingsDb.objects.exclude(id=obj.id).delete()
        super(SettingsDbAdmin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return len(SettingsDb.objects.all()) < 1


# class ExecutedBackupAdmin(admin.ModelAdmin):
#
#     list_display = ('createdAt', 'is_automatically',)
#     list_filter = ['is_automatically']
#     ordering = ('-createdAt',)
#     search_fields = ['comment']
#
#     def save_model(self, request, obj, form, change):
#         # if not obj.id:
#         #     if not ExecutedBackup.objects.filter(createdAt__gte=datetime.now()-timedelta(hours=1)).exists():
#         #         if "linux" in sys.platform:
#         #             kwargs = {}
#         #             if settings.ENVIRONMENT == "preproduction":
#         #                 kwargs.update({
#         #                     "settings": "backend.settings.preproduction"
#         #                 })
#         #             elif settings.ENVIRONMENT == "production":
#         #                 kwargs.update({
#         #                     "settings": "backend.settings.production"
#         #                 })
#         #             try:
#         #                 management.call_command('dbbackup', **kwargs)
#         #                 management.call_command('mediabackup', **kwargs)
#         #             except:
#         #                 pass
#         super(ExecutedBackupAdmin, self).save_model(request, obj, form, change)


admin.site.register(SettingsDb, SettingsDbAdmin)
# admin.site.register(ExecutedBackup, ExecutedBackupAdmin)