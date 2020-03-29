# -*- coding: utf-8 -*-
from .apps import UsefullinksConfig
from .models import LinkCategory, UsefulLink
from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.test import Client, TestCase
from django.urls import reverse
import json


class ContactConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(UsefullinksConfig.name, 'usefullinks')
        self.assertEqual(apps.get_app_config('usefullinks').name, 'usefullinks')


class UsefulLinkModelTest(TestCase):
    def setUp(self):
        self.link_category = LinkCategory.objects.create(
            label="Link category"
        )
        self.useful_link = UsefulLink.objects.create(
            label="Useful link",
            url="link",
            category=self.link_category,
        )

    def test___str__(self):
        self.assertEqual("Useful link", self.useful_link.__str__())


class LinkCategoryModelTest(TestCase):
    def setUp(self):
        self.link_category = LinkCategory.objects.create(
            label="Link category"
        )

    def test___str__(self):
        self.assertEqual("Link category", self.link_category.__str__())


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.link_category1 = LinkCategory.objects.create(
            label="Link category1"
        )
        self.useful_link11 = UsefulLink.objects.create(
            label="Useful link11",
            url="link11",
            category=self.link_category1,
        )
        self.useful_link12 = UsefulLink.objects.create(
            label="Useful link12",
            url="link12",
            category=self.link_category1,
        )
        self.link_category2 = LinkCategory.objects.create(
            label="Link category2"
        )
        self.useful_link21 = UsefulLink.objects.create(
            label="Useful link21",
            url="link21",
            category=self.link_category2,
        )
        self.useful_link22 = UsefulLink.objects.create(
            label="Useful link22",
            url="link22",
            category=self.link_category2,
        )
        self.link_category3 = LinkCategory.objects.create(
            label="Link category3"
        )

    def test_links_list(self):
        response = self.client.post(reverse('links_list'))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('links_list'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue("categories" in content)
        self.assertTrue("guides" in content)
        self.assertEqual(len(list(content["categories"].keys())), 2)
        self.assertEqual(len(content["guides"]), 2)
        self.assertEqual(len(content["categories"]["Link category2"]), 2)
        self.assertEqual(content["categories"]["Link category2"][0]["pk"], 3)
        self.assertEqual(content["categories"]["Link category2"][0]["url"], "link21")
        self.assertEqual(content["categories"]["Link category1"][0]["label"], "Useful link11")
        self.assertEqual(content["guides"][0]["url"], settings.BACKEND_URL_ROOT + static("usefullinks/docs/en/buyers-guide.pdf"))
