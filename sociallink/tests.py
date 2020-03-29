# -*- coding: utf-8 -*-
from .admin import SocialLinkAdmin
from .apps import SociallinkConfig
from .models import SocialLink
from django.apps import apps
from django.contrib.admin.sites import AdminSite
from django.test import TestCase


class ContactConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(SociallinkConfig.name, 'sociallink')
        self.assertEqual(apps.get_app_config('sociallink').name, 'sociallink')


class AdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()

    def test_has_add_permission(self):
        social_link_admin_instance = SocialLinkAdmin(SocialLink, self.admin_site)
        self.assertTrue(social_link_admin_instance.has_add_permission(None))
        SocialLink.objects.create(
            label="social_link1",
            url="social_link_url_1"
        )
        SocialLink.objects.create(
            label="social_link2",
            url="social_link_url_2"
        )
        SocialLink.objects.create(
            label="social_link3",
            url="social_link_url_3"
        )
        SocialLink.objects.create(
            label="social_link4",
            url="social_link_url_4"
        )
        SocialLink.objects.create(
            label="social_link5",
            url="social_link_url_5"
        )
        self.assertTrue(social_link_admin_instance.has_add_permission(None))
        SocialLink.objects.create(
            label="social_link6",
            url="social_link_url_6",
            is_active=False
        )
        self.assertFalse(social_link_admin_instance.has_add_permission(None))

