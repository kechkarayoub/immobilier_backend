# -*- coding: utf-8 -*-
from .models import Funding
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


def get_bank_logo_preview(obj):
    if obj.image:
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (str(obj.bank_logo)))
    return _("No file selected!")


get_bank_logo_preview.allow_tags = True
get_bank_logo_preview.short_description = _("Image Preview")


class FundingAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'funding/js/funding_form.js',
        )

    fieldsets = (
        (None, {
            'fields': (
                'bank_name', 'free_field_label', 'free_field_value', 'bank_logo', get_bank_logo_preview, 'bank_email',
            )
        }),
    )
    list_display = ('bank_name', 'bank_email')
    search_fields = ['bank_name', 'bank_email', 'free_field_label', 'free_field_value']
    ordering = ('-createdAt',)
    readonly_fields = [get_bank_logo_preview]

    def save_model(self, request, obj, form, change):
        super(FundingAdmin, self).save_model(request, obj, form, change)


admin.site.register(Funding, FundingAdmin)
