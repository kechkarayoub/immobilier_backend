# -*- coding: utf-8 -*-

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


# @receiver(post_save, sender=Model)
# @on_transaction_commit
# def create_next_leasing_entry(sender, **kwargs):
#     pass