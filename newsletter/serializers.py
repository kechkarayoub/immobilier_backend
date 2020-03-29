# -*- coding: utf-8 -*-
from .models import Newsletter
from rest_framework import serializers


class NewsletterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Newsletter
        fields = ('pk', 'email', 'first_name', 'last_name')
