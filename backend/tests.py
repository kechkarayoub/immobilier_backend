# -*- coding: utf-8 -*-


from django.test import TestCase
from .utils import send_email, generate_random_color, get_complementary_color, choices_format_to_dict, generate_id, \
    get_list_social_links_images
from django.core import mail
from colour import Color
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.test import Client
from django.urls import reverse
from backend import added_settings
import json


class UtilsPackageTest(TestCase):

    def test_send_email(self):
        send_email('Subject here', 'Here is the message.', 'from@example.com', 'to@example.com', "<div>test html</div>")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
        self.assertEqual(mail.outbox[0].body, 'Here is the message.')
        self.assertEqual(mail.outbox[0].from_email, 'from@example.com')
        self.assertEqual(mail.outbox[0].to, ['to@example.com'])
        self.assertEqual(mail.outbox[0].alternatives[0][0], "<div>test html</div>")

    def test_get_complementary_color(self):
        self.assertEqual("#FFFFFF", get_complementary_color("#000000"))
        self.assertEqual("#000000", get_complementary_color("#ffffff"))
        self.assertEqual("#6929D6", get_complementary_color("#96D629"))
        self.assertEqual("#12ED21", get_complementary_color("#ED12DE"))

    def test_generate_random_color(self):
        random_color, complementary = generate_random_color(with_complementary=True)
        self.assertTrue(isinstance(Color(generate_random_color()), Color))
        self.assertTrue(isinstance(Color(random_color), Color))
        self.assertEqual(complementary, get_complementary_color(random_color))

    def test_choices_format_to_dict(self):
        self.assertEqual({"key": "value"}, choices_format_to_dict((("key", "value"),)))
        self.assertEqual(2, len(list(choices_format_to_dict((("key", "value"), ("key2", "value2"),)).keys())))

    def test_generate_id(self):
        self.assertEqual("AEXXXXXXXX1", generate_id())
        self.assertEqual("AEXXXXXXXX2", generate_id("AEXXXXXXXX1"))
        self.assertEqual("AEXXXX12059", generate_id("AEXXXX12058"))
        self.assertEqual("AE999999999", generate_id("AE999999998"))
        self.assertEqual("AE9999999999", generate_id("AE9999999998"))

    def test_get_list_social_links_images(self):
        self.assertEqual(6, len(list(get_list_social_links_images().keys())))
        self.assertTrue("facebook" in list(get_list_social_links_images().keys()))
        self.assertEqual(get_list_social_links_images()["youtube"], settings.BACKEND_URL_ROOT + static("contact/images/youtube.png"))


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_global_params_view(self):
        response = self.client.get(reverse('global_params'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue("realtor_data" in content)
        self.assertTrue("selects_choices" in content)
        self.assertTrue("is_maps_active" in content)
        self.assertEqual(content["is_maps_active"], added_settings.IS_MAPS_ACTIVE)
        self.assertEqual(content["footer_params"]["site_url_root"], settings.SITE_URL_ROOT)

