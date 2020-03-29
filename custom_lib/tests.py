# -*- coding: utf-8 -*-


from django.test import TestCase
from .apps import CustomLibConfig
from django.apps import apps
from .templatetags.custom_tags import get_value


class ContactConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(CustomLibConfig.name, 'custom_lib')
        self.assertEqual(apps.get_app_config('custom_lib').name, 'custom_lib')


class CustomLibTest(TestCase):
    def test_get_value(self):
        self.assertEqual(None, get_value({}, "key"))
        self.assertEqual("value", get_value({"key": "value"}, "key"))
