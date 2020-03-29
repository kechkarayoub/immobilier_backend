# -*- coding: utf-8 -*-


from django.test import TestCase
from .apps import TestimonialConfig
from django.apps import apps
from django.contrib.admin.sites import AdminSite
from .models import Testimonial
from .admin import TestimonialAdmin
from .serializers import TestimonialSerializer
import datetime
from django.test import Client
from django.urls import reverse
import json
from backend.utils import get_complementary_color


class ContactConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(TestimonialConfig.name, 'testimonial')
        self.assertEqual(apps.get_app_config('testimonial').name, 'testimonial')


class AdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.testimonial_admin_instance = TestimonialAdmin(Testimonial, self.admin_site)

    def test_has_add_permission(self):
        self.assertFalse(self.testimonial_admin_instance.has_add_permission(None))

    def test_save_model(self):
        self.assertEqual(None, self.testimonial_admin_instance.save_model(None, None, None, None))


class SerializerTest(TestCase):
    def setUp(self):

        self.testimonial_data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            "testimonial": "testimonial"
        }

        self.testimonial = Testimonial.objects.create(**self.testimonial_data)
        self.serializer_testimonial = TestimonialSerializer(instance=self.testimonial)

    def test_to_representation(self):
        self.assertEqual(self.serializer_testimonial.data, {
            "pk": 1,
            "city": "",
            "city_val": "",
            'first_name': 'first_name',
            'last_name': 'last_name',
            "testimonial": "testimonial",
            "initials_color": "#000000",
            "initials_bg_color": "#ffffff",
            "createdAt": datetime.datetime.now().strftime("%d %B, %Y")
        })


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_testimonials_list(self):
        response = self.client.post(reverse('testimonials_list'))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('testimonials_list'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 0)
        self.assertEqual(content["count"], 0)
        self.assertEqual(content["numpages"], 1)
        self.assertEqual(content["nextLink"], "")
        self.assertEqual(content["prevLink"], "")

        self.testimonial1 = Testimonial.objects.create(
            first_name='first_name1',
            last_name='last_name1',
            testimonial="testimonial1"
        )
        self.testimonial2 = Testimonial.objects.create(
            first_name='first_name2',
            last_name='last_name2',
            testimonial="testimonial2"
        )
        self.testimonial3 = Testimonial.objects.create(
            first_name='first_name3',
            last_name='last_name3',
            testimonial="testimonial3"
        )

        response = self.client.get(reverse('testimonials_list'), {
            "test": True
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 1)
        self.assertEqual(content["count"], 3)
        self.assertEqual(content["numpages"], 3)
        self.assertEqual(content["nextLink"], "/api/testimonials/?page=2")
        self.assertEqual(content["prevLink"], "")

        response = self.client.get(reverse('testimonials_list'), {
            "page": 2,
            "test": True
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 1)
        self.assertEqual(content["count"], 3)
        self.assertEqual(content["numpages"], 3)
        self.assertEqual(content["nextLink"], "/api/testimonials/?page=3")
        self.assertEqual(content["prevLink"], "/api/testimonials/?page=1")

        response = self.client.get(reverse('testimonials_list'), {
            "page": 3,
            "test": True
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 1)
        self.assertEqual(content["count"], 3)
        self.assertEqual(content["numpages"], 3)
        self.assertEqual(content["nextLink"], "")
        self.assertEqual(content["prevLink"], "/api/testimonials/?page=2")

        response = self.client.get(reverse('testimonials_list'), {
            "page": 4,
            "test": True
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 1)
        self.assertEqual(content["count"], 3)
        self.assertEqual(content["numpages"], 3)
        self.assertEqual(content["nextLink"], "")
        self.assertEqual(content["prevLink"], "/api/testimonials/?page=2")

    def test_create_testimonial(self):
        response = self.client.get(reverse('create_testimonial'))
        self.assertEqual(response.status_code, 405)

        response = self.client.post(reverse('create_testimonial'), {
            'last_name': 'last_name',
            "testimonial": "testimonial"
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('create_testimonial'), {
            'first_name': 'first_name',
            'last_name': 'last_name',
            "testimonial": "testimonial"
        })
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content["pk"], 1)
        self.assertEqual(content["first_name"], "first_name")
        self.assertEqual(content["last_name"], "last_name")
        self.assertEqual(content["testimonial"], "testimonial")
        self.assertEqual(content["initials_color"], get_complementary_color(content["initials_bg_color"]))



