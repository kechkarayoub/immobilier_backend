# -*- coding: utf-8 -*-
from .models import LinkCategory, UsefulLink
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


class LinkCategoryAdmin(TranslationAdmin):
    list_display = ('label',)
    search_fields = ['label']


class UsefulLinkAdmin(TranslationAdmin):
    list_display = ('label', 'category',)
    list_filter = ['category']
    search_fields = ['label', 'url']


admin.site.register(LinkCategory, LinkCategoryAdmin)
admin.site.register(UsefulLink, UsefulLinkAdmin)
