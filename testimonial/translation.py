# -*- coding: utf-8 -*-
from .models import Testimonial
from modeltranslation.translator import translator, TranslationOptions


class TestimonialTranslationOptions(TranslationOptions):
    fields = (
        'testimonial',
    )


translator.register(Testimonial, TestimonialTranslationOptions)
