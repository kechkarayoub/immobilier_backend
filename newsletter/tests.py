# -*- coding: utf-8 -*-
from .apps import NewsletterConfig
from .models import Newsletter
from django.apps import apps
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
import json


class ContactConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(NewsletterConfig.name, 'newsletter')
        self.assertEqual(apps.get_app_config('newsletter').name, 'newsletter')


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.newsletter1 = Newsletter.objects.create(
            first_name="first_name1",
            last_name="last_name1",
            email="newsletter1@yopmail.com",
        )
        self.newsletter2 = Newsletter.objects.create(
            first_name="first_name2",
            last_name="last_name2",
            email="newsletter2@yopmail.com",
            is_active=False
        )

    def test_newsletter_create(self):
        response = self.client.get(reverse('newsletter_create'))
        self.assertEqual(response.status_code, 405)

        with self.assertRaises(MultiValueDictKeyError):
            self.client.post(reverse('newsletter_create'))

        response = self.client.post(reverse('newsletter_create'), {
            "email": "newsletter1@yopmail.com",
            "first_name": "first_name1",
            "last_name": "last_name1"
        })
        self.assertEqual(response.status_code, 409)
        content = json.loads(response.content)
        self.assertEqual(content["email"], ["newsletter with this Email already exists."])

        response = self.client.post(reverse('newsletter_create'), {
            "email": "newsletter2@yopmail.com",
            "first_name": "first_name2",
            "last_name": "last_name2"
        })
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content["response_type"], "reactivated")

        response = self.client.post(reverse('newsletter_create'), {
            "email": "newsletter2@yopmail.com",
            "first_name": "first_name3",
            "last_name": "last_name3"
        })
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content["response_type"], "updated")

        response = self.client.post(reverse('newsletter_create'), {
            "email": "newsletter3@yopmail.com",
            "first_name": "first_name3",
            "last_name": "last_name3"
        })
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content["response_type"], "created")
        self.assertTrue("data" in content)
        self.assertEqual(content["data"]["email"], "newsletter3@yopmail.com")
        self.assertEqual(content["data"]["first_name"], "first_name3")
        self.assertEqual(content["data"]["last_name"], "last_name3")

    def test_newsletter_unsubscribe(self):
        response = self.client.post(reverse('newsletter_unsubscribe'))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('newsletter_unsubscribe'), {
            "user_email": "not_exists@yopmail.com"
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertFalse(content["data"]["success"])
        self.assertEqual(content["data"]["message"], "Sorry, you haven't any subscription in our newsletter!")

        response = self.client.get(reverse('newsletter_unsubscribe'), {
            "user_email": "newsletter2@yopmail.com"
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertFalse(content["data"]["success"])
        self.assertEqual(content["data"]["message"], "Your subscription is already deactivated!")

        response = self.client.get(reverse('newsletter_unsubscribe'), {
            "user_email": "newsletter1@yopmail.com"
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue(content["data"]["success"])
        self.assertEqual(content["data"]["message"], "Your subscription is deactivated!")

    def test_newsletter_resubscribe(self):
        response = self.client.post(reverse('newsletter_resubscribe'))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('newsletter_resubscribe'), {
            "user_email": "not_exists@yopmail.com"
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertFalse(content["data"]["success"])
        self.assertEqual(content["data"]["message"], "Sorry, you haven't any subscription in our newsletter!")

        response = self.client.get(reverse('newsletter_resubscribe'), {
            "user_email": "newsletter2@yopmail.com"
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue(content["data"]["success"])
        self.assertEqual(content["data"]["message"], "Your subscription is reactivated!")

        response = self.client.get(reverse('newsletter_resubscribe'), {
            "user_email": "newsletter1@yopmail.com"
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertFalse(content["data"]["success"])
        self.assertEqual(content["data"]["message"], "Your subscription is already activated!")
