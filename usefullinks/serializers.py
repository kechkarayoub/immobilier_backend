# -*- coding: utf-8 -*-
from .models import LinkCategory, UsefulLink
from rest_framework import serializers


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulLink
        fields = ('pk', 'label', 'url')


class LinkCategorySerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = LinkCategory
        fields = ('label', 'links')
