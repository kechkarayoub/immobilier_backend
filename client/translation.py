# -*- coding: utf-8 -*-
from .models import Client, GroupClient
from modeltranslation.translator import translator, TranslationOptions


class ClientTranslationOptions(TranslationOptions):
    fields = ('address', 'first_name', 'last_name')


class GroupClientTranslationOptions(TranslationOptions):
    fields = (
        'group_name', 'reminder_payment_email_footer_line1', 'reminder_payment_email_footer_line2',
        'reminder_payment_email_message1', 'reminder_payment_email_message2', 'reminder_payment_email_message3',
        'reminder_payment_email_object'
    )


translator.register(Client, ClientTranslationOptions)
translator.register(GroupClient, GroupClientTranslationOptions)
