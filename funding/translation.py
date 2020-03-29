# -*- coding: utf-8 -*-
from .models import Funding
from modeltranslation.translator import translator, TranslationOptions


class FundingTranslationOptions(TranslationOptions):
    fields = ('free_field_label', 'free_field_value',)


translator.register(Funding, FundingTranslationOptions)
