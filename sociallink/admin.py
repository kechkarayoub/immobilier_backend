# -*- coding: utf-8 -*-
from .models import SocialLink
from django.contrib import admin


class SocialLinkAdmin(admin.ModelAdmin):

    list_display = ('label', 'is_active',)
    list_filter = ['is_active']
    search_fields = ['label', 'url']

    def has_add_permission(self, request, obj=None):
        if len(SocialLink.objects.all()) >= 6:
            return False
        return True


admin.site.register(SocialLink, SocialLinkAdmin)
