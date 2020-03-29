# -*- coding: utf-8 -*-
from .models import Testimonial
from backend.utils import generate_random_color
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from easy_select2 import select2_modelform


TestimonialForm = select2_modelform(Testimonial, attrs={'width': '250px'})


def get_user_image_preview(obj):
    if obj.image:
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (str(obj.image)))
    return _("No file selected!")


get_user_image_preview.allow_tags = True
get_user_image_preview.short_description = _("Image Preview")


class TestimonialAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'testimonial/js/testimonial_form.js',
        )
    form = TestimonialForm

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'city', 'testimonial_en', 'testimonial_fr', 'image', get_user_image_preview,)
        }),
    )
    list_display = ('first_name', 'last_name', 'city',)
    list_filter = ['createdAt',  'city']
    search_fields = ['first_name', 'last_name', 'testimonial']
    ordering = ('-createdAt',)
    readonly_fields = [get_user_image_preview]

    def save_model(self, request, obj, form, change):
        color, complementary_color = generate_random_color(with_complementary=True)
        obj.initials_color = color
        obj.initials_bg_color = complementary_color
        super(TestimonialAdmin, self).save_model(request, obj, form, change)


admin.site.register(Testimonial, TestimonialAdmin)
