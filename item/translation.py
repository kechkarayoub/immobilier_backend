# -*- coding: utf-8 -*-
from .models import Item
from modeltranslation.translator import translator, TranslationOptions


class ItemTranslationOptions(TranslationOptions):
    fields = (
        'added_field_1_label', 'added_field_1_value', 'added_field_2_label', 'added_field_2_value',
        'added_field_3_label', 'added_field_3_value', 'address', 'description', 'label', 'housing_descriptions',
        'short_description',
    )


translator.register(Item, ItemTranslationOptions)