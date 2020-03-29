# -*- coding: utf-8 -*-
from .models import LinkCategory, UsefulLink
from modeltranslation.translator import translator, TranslationOptions


class UsefulLinkTranslationOptions(TranslationOptions):
    fields = ('label',)


class LinkCategoryTranslationOptions(TranslationOptions):
    fields = ('label',)


translator.register(LinkCategory, LinkCategoryTranslationOptions)
translator.register(UsefulLink, UsefulLinkTranslationOptions)