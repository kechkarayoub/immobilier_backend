# -*- coding: utf-8 -*-
from .models import SocialLink
from rest_framework import serializers


class SocialLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialLink
        fields = ('fa_icon', 'label', 'url')
