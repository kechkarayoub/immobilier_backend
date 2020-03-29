# -*- coding: utf-8 -*-
from .models import Contact, ContactBuy, ContactRent
from django.contrib import admin
from django.http import HttpResponseRedirect


class ContactAdmin(admin.ModelAdmin):

    class Media:
        js = ('contact/js/contact_form.js',)

    list_display = ('first_name', 'last_name', 'object', 'email',)
    list_filter = ['createdAt']
    ordering = ('-createdAt',)
    search_fields = ['first_name', 'last_name', 'object', 'email']

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass


class ContactBuyAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'contact/js/contact_buy_form.js',
        )

    list_display = ('first_name', 'last_name', 'email', 'has_been_processed',)
    list_filter = [
        'has_been_processed', 'createdAt',  'has_dining_room', 'has_fireplace', 'has_garage', 'has_swimming_pool',
        'has_garden'
    ]
    ordering = ('-createdAt',)
    search_fields = ['first_name', 'last_name', 'email']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields if field.name != "is_active"]
        return self.readonly_fields

    def changelist_view(self, request, extra_context=None):
        if not request.META['QUERY_STRING'] and \
                not request.META.get('HTTP_REFERER', '').startswith(request.build_absolute_uri()):
            return HttpResponseRedirect(request.path + "?has_been_processed__exact=0")
        return super(ContactBuyAdmin, self).changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request, obj=None):
        return False


class ContactRentAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'contact/js/contact_rent_form.js',
        )

    list_display = ('first_name', 'last_name', 'email', 'has_been_processed',)
    list_filter = [
        'has_been_processed', 'createdAt',  'has_dining_room', 'has_fireplace', 'has_garage', 'has_swimming_pool',
        'has_garden'
    ]
    ordering = ('-createdAt',)
    search_fields = ['first_name', 'last_name', 'email']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields if field.name != "is_active"]
        return self.readonly_fields

    def changelist_view(self, request, extra_context=None):
        if not request.META['QUERY_STRING'] and \
                not request.META.get('HTTP_REFERER', '').startswith(request.build_absolute_uri()):
            return HttpResponseRedirect(request.path + "?has_been_processed__exact=0")
        return super(ContactBuyAdmin, self).changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactBuy, ContactBuyAdmin)
admin.site.register(ContactRent, ContactRentAdmin)
