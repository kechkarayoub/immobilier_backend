# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Contact, ContactBuy, ContactRent


class ContactSellSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('pk', 'email', 'first_name', 'last_name', 'message', 'object', 'phone')


class ContactBuySerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactBuy
        fields = (
            'pk', 'bathrooms_number', 'bedrooms_number', 'building_type', 'city', 'construction_age', 'email',
            'first_name', 'has_dining_room', 'has_fireplace', 'has_garage', 'has_garden', 'has_swimming_pool',
            'last_name', 'lot_size_max', 'lot_size_min', 'occupation_date', 'other_characteristics', 'phone',
            'price_range', 'property_type', 'status'
        )


class ContactRentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactRent
        fields = (
            'pk', 'bathrooms_number', 'bedrooms_number', 'building_type', 'city', 'construction_age', 'email',
            'first_name', 'has_dining_room', 'has_fireplace', 'has_garage', 'has_garden', 'has_swimming_pool',
            'last_name', 'lot_size_max', 'lot_size_min', 'occupation_date', 'other_characteristics', 'phone',
            'price_range', 'property_type', 'status'
        )
