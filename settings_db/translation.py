# -*- coding: utf-8 -*-
from .models import SettingsDb
from modeltranslation.translator import translator, TranslationOptions


class AdminDataTranslationOptions(TranslationOptions):
    fields = (
        'home_page_title_1', 'home_page_title_2', 'home_page_row_1_title', 'home_page_row_1_p_1', 'home_page_row_1_p_2',
        'home_page_row_1_p_3', 'home_page_row_2_title', 'home_page_row_2_p_1', 'home_page_row_2_p_2',
        'home_page_row_2_p_3', 'home_page_row_3_title', 'home_page_row_3_p_1', 'home_page_row_3_p_2',
        'home_page_row_3_p_3',
    )


translator.register(SettingsDb, AdminDataTranslationOptions)