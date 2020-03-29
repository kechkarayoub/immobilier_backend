# -*- coding: utf-8 -*-
from .models import Funding
from django.conf import settings
from django.utils.translation import get_language
from rest_framework import serializers
import locale


class FundingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Funding
        fields = (
            'bank_name', 'createdAt', 'bank_logo', 'free_field_label', 'free_field_value', 'bank_email', 'pk'
        )

    def to_representation(self, instance):
        representation = super(FundingSerializer, self).to_representation(instance)
        current_language = get_language()
        if current_language == "fr":
            try:
                locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
            except:
                try:
                    locale.setlocale(locale.LC_ALL, "fr")
                except:
                    pass

            representation['createdAt'] = instance.createdAt.strftime("%d %B, %Y")
        else:
            representation['createdAt'] = instance.createdAt.strftime("%B %d, %Y")
        if instance.bank_logo and instance.bank_logo.url:
            representation['bank_logo'] = settings.BACKEND_URL_ROOT + instance.bank_logo.url
        else:
            representation['bank_logo'] = ""

        return representation
