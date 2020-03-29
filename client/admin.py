# -*- coding: utf-8 -*-
from .models import Client, GroupClient
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
import datetime


class ClientAdmin(admin.ModelAdmin):

    class Media:
        js = ('client/js/client_form.js',)

    fieldsets = [
        (None, {
            'fields': [
                'address', 'apartment', 'first_name', 'last_name', 'email', 'phone', 'group_client', 'type', 'is_active'
            ]
        }),
    ]
    list_display = ('first_name', 'last_name', 'email', 'address', 'type', 'group_client')
    list_filter = ['is_active', 'type', 'group_client']
    ordering = ('-createdAt',)
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'address']


class GroupClientAdmin(admin.ModelAdmin):

    class Media:
        js = ('client/js/group_client_form.js',)

    fieldsets = [
        (_("Paramètres générals"), {
            'fields': [
                'group_name', 'is_active'
            ]
        }),
        (_("E-mail de rappel de paiement"), {
            'fields': [
                'reminder_payment_email_object', 'reminder_payment_email_message1', 'reminder_payment_email_message2',
                'reminder_payment_email_message3', "reminder_payment_email_footer_line1",
                'reminder_payment_email_footer_line2'
            ]
        }),
    ]
    list_display = ('__str__', 'is_active')
    list_filter = ['is_active']
    search_fields = ['__str__']


admin.site.register(Client, ClientAdmin)
admin.site.register(GroupClient, GroupClientAdmin)
