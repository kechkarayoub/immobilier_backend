# -*- coding: utf-8 -*-
from .models import Item, ItemImage
from django.conf import settings
from rest_framework import serializers


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('pk', 'image',)

    def to_representation(self, instance):
        representation = super(ItemImageSerializer, self).to_representation(instance)
        if instance.image and instance.image.url:
            representation['image'] = settings.BACKEND_URL_ROOT + instance.image.url
        else:
            representation['image'] = ""

        return representation


class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = (
            'pk', 'added_field_1_label', 'added_field_1_value', 'added_field_2_label', 'added_field_2_value',
            'added_field_3_label', 'added_field_3_value', 'address', 'annual_income', 'apartments_number',
            'bedrooms_number', 'bathrooms_number', 'building_type', 'ccd', 'city', 'construction_age',
            'cost_per_housing', 'description', 'down_payment_required', 'economic_value', 'gps_latitude',
            'gps_longitude', 'gross_revenue_multiplier', 'has_dining_room', 'has_fireplace', 'has_garage', 'has_garden',
            'has_swimming_pool', 'housing_descriptions', 'image_map', 'images', 'is_active', "is_new", 'label',
            'lot_size', 'maximum_loan', 'net_income_multiplier', 'overall_rate_update', 'property_type', 'price',
            'short_description', 'status', 'with_map', 'catalog'
        )

    def to_representation(self, instance):
        representation = super(ItemSerializer, self).to_representation(instance)
        if instance.catalog and instance.catalog.url:
            representation['catalog'] = settings.BACKEND_URL_ROOT + instance.catalog.url
        else:
            representation['catalog'] = ""

        return representation
