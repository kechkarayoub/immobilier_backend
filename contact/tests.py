# -*- coding: utf-8 -*-


from django.test import TestCase
from .apps import ContactConfig
from django.apps import apps
from .admin import ContactAdmin, ContactBuyAdmin
from .models import Contact, ContactBuy
from django.contrib.admin.sites import AdminSite
from django.test import Client
from django.urls import reverse
from backend import added_settings
import json


class ContactConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ContactConfig.name, 'contact')
        self.assertEqual(apps.get_app_config('contact').name, 'contact')


class AdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()

    def test_contact_admin_has_add_permission(self):
        contact_admin_instance = ContactAdmin(Contact, self.admin_site)
        self.assertFalse(contact_admin_instance.has_add_permission(None))
        self.assertEqual(None, contact_admin_instance.save_model(None, None, None, None))

    def test_contact_buy_admin_has_add_permission(self):
        contact_buy_admin_instance = ContactBuyAdmin(ContactBuy, self.admin_site)
        self.assertFalse(contact_buy_admin_instance.has_add_permission(None))
        self.assertEqual(None, contact_buy_admin_instance.save_model(None, None, None, None))


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_sell_create(self):
        response = self.client.get(reverse('contact_sell_create'))
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse('contact_sell_create'), {})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('contact_sell_create'), {
            "first_name": "First Name",
            "last_name": "Last Name",
            "object": "Object",
            "email": "email@yopmail.com",
            "phone": "060000000000",
            "message": "Message",
        })
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertTrue("pk" in content)
        self.assertEqual("First Name", content["first_name"])
        self.assertEqual("Message", content["message"])

    def test_contact_buy_create(self):
        response = self.client.get(reverse('contact_buy_create'))
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse('contact_buy_create'), {})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('contact_buy_create'), {
            "first_name": "First Name",
            "last_name": "Last Name",
            "object": "Object",
            "email": "email@yopmail.com",
            "phone": "060000000000",
            "city": "montreal",
            "city_text": "Montreal",
            "occupation_date": "",
            "property_type": "apartment",
            "property_type_text": "Apartment",
            "building_type": "detached",
            "building_type_text": "Detached",
            "construction_age": "newly_built",
            "construction_age_text": "Newly built",
            "bedrooms_number": "1",
            "bedrooms_number_text": "1",
            "bathrooms_number": "2",
            "bathrooms_number_text": "2",
            "price_range": "200_300",
            "price_range_text": "200$-300$",
            "lot_size_min": 0,
            "lot_size_mAX": 0,
            "has_dining_room": "",
            "has_fireplace": "",
            "has_garage": "",
            "has_swimming_pool": "",
            "has_garden": "",
            "other_characteristics": "Other caracteristics"
        })
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertTrue("pk" in content)
        self.assertEqual("First Name", content["first_name"])
        self.assertEqual("Other caracteristics", content["other_characteristics"])
        self.assertEqual("newly_built", content["construction_age"])
        self.assertEqual("200_300", content["price_range"])

    def test_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse('contact'), {
            "first_name": "First Name",
            "last_name": "Last Name",
            "object": "Object",
            "email": "email@yopmail.com",
            "phone": "060000000000",
            "message": "Message",
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue("success" in content)
        self.assertTrue(content["success"])
