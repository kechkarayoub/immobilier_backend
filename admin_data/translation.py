# -*- coding: utf-8 -*-
from .models import AdminData
from modeltranslation.translator import translator, TranslationOptions


class AdminDataTranslationOptions(TranslationOptions):
    fields = ('address',)


translator.register(AdminData, AdminDataTranslationOptions)