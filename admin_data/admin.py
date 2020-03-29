# -*- coding: utf-8 -*-
from .models import AdminData
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin


def get_admin_image_preview(obj):
    if obj.image:
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (str(obj.image)))
    return _("No file selected!")


get_admin_image_preview.allow_tags = True
get_admin_image_preview.short_description = _("Image Preview")


class AdminDataAdmin(TranslationAdmin):

    class Media:
        js = (
            'admin_data/js/admin_data_form.js',
        )
    list_display = (
        '__str__', 'full_name', 'email', 'agency_name', 'fax', 'tel'
    )
    fieldsets = [
        (_("General information"), {
            'fields': ['full_name', 'agency_name', 'email', 'tel', 'fax', 'address', 'image', get_admin_image_preview]
        }),
        (_("Map options"), {
            'fields': ['enable_map', 'gps_latitude', 'gps_longitude']
        }),
    ]
    readonly_fields = [get_admin_image_preview]

    def save_model(self, request, obj, form, change):
        if len(AdminData.objects.all()) > 0:
            AdminData.objects.exclude(id=obj.id).delete()
        super(AdminDataAdmin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return len(AdminData.objects.all()) < 1


admin.site.register(AdminData, AdminDataAdmin)
