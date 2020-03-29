# -*- coding: utf-8 -*-


from .admin import get_item_image_map_preview, get_item_images_preview, ItemAdmin
from .apps import ItemConfig
from .models import Item, ItemImage
from datetime import datetime, timedelta
from django.apps import apps
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from newsletter.models import Newsletter
import json
import os
from .views import send_property_to_newsletters

from django.conf import settings
from django.core import mail


class ItemConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ItemConfig.name, 'item')
        self.assertEqual(apps.get_app_config('item').name, 'item')


class AdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        Item.objects.filter().delete()
        self.item1 = Item.objects.create(
            item_id="AEXXXXXXXX1",
            label="label1",
            short_description="short_description1",
            address="address1",
            description="description1",
            city="motreal",
            property_type="apartment",
        )
        self.item2 = Item.objects.create(
            item_id="AEXXXXXXXX2",
            label="label2",
            short_description="short_description2",
            address="address2",
            description="description2",
            city="motreal",
            property_type="apartment",
            image_map=SimpleUploadedFile(name='image_test.png', content=open(os.path.dirname(os.path.abspath(__file__)) + "/static/item/test/images/image_test.png", 'rb').read(), content_type='image/png'),
        )
        self.image_item1 = ItemImage.objects.create(
            image=SimpleUploadedFile(name='image_test.png', content=open(os.path.dirname(os.path.abspath(__file__)) + "/static/item/test/images/image_test.png", 'rb').read(), content_type='image/png'),
            item=self.item1
        )
        self.image_item2 = ItemImage.objects.create(
            item=self.item1
        )

    def test_get_item_images_preview(self):
        self.assertEqual("No file selected!", get_item_images_preview(self.image_item2))
        self.assertTrue(get_item_images_preview(self.image_item1).count('<img src="/media/images/item/itemsImages/image_test') == 1)

    def test_get_item_image_map_preview(self):
        self.assertEqual("No file selected!", get_item_image_map_preview(self.item1))
        self.assertTrue(get_item_image_map_preview(self.item2).count('<img src="/media/images/item/itemsImages/image_test') == 1)

    def test_save_model(self):
        Item.objects.all().delete()
        item = Item(
            label="label",
            short_description="short_description",
            address="address",
            description="description",
            city="motreal",
            property_type="apartment",
        )
        item_admin_instance = ItemAdmin(Item, self.admin_site)
        item_admin_instance.save_model(None, item, None, False)
        created_item = Item.objects.filter().latest('createdAt')
        self.assertEqual("AEXXXXXXXX1", created_item.item_id)
        item2 = Item(
            label="label2",
            short_description="short_description2",
            address="address2",
            description="description2",
            city="motreal",
            property_type="apartment",
        )
        item_admin_instance.save_model(None, item2, None, False)
        created_item2 = Item.objects.filter().latest('createdAt')
        self.assertEqual("AEXXXXXXXX2", created_item2.item_id)


class ItemModelTest(TestCase):
    def setUp(self):
        Item.objects.filter().delete()
        self.item1 = Item.objects.create(
            item_id="AEXXXXXXXX1",
            label="Label1",
            short_description="short_description1",
            address="address1",
            description="description1",
            city="motreal",
            property_type="apartment",
        )
        self.item2 = Item.objects.create(
            item_id="AEXXXXXXXX2",
            label="label2",
            short_description="short_description2",
            address="address2",
            description="description2",
            city="motreal",
            property_type="apartment",
            createdAt=datetime.now() - timedelta(days=9)
        )

    def test___str__(self):
        self.assertEqual("Label1", self.item1.__str__())
        self.assertEqual("label2", self.item2.__str__())

    def test_is_new(self):
        self.assertTrue(self.item1.is_new)
        # self.assertFalse(self.item2.is_new)  # return True because by Item model don't take createdAt attribute; It save current date


class ItemImageModelTest(TestCase):
    def setUp(self):
        Item.objects.filter().delete()
        self.item = Item.objects.create(
            item_id="AEXXXXXXXX1",
            label="Label1",
            short_description="short_description1",
            address="address1",
            description="description1",
            city="motreal",
            property_type="apartment",
        )
        self.image_item = ItemImage.objects.create(
            image=SimpleUploadedFile(name='image_test.png', content=open(os.path.dirname(os.path.abspath(__file__)) + "/static/item/test/images/image_test.png", 'rb').read(), content_type='image/png'),
            item=self.item
        )

    def test___str__(self):
        self.assertTrue(self.image_item.__str__().count('image_test') == 1)

    def test_image_filename(self):
        self.assertEqual(self.image_item.image_filename, os.path.basename(self.image_item.image.name))


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        Item.objects.filter().delete()
        self.item1 = Item.objects.create(
            item_id="AEXXXXXXXX1",
            label="label1",
            short_description="short_description1",
            address="address1",
            description="description1",
            city="montreal",
            property_type="apartment",
            price=300000,
            has_dining_room=True,
            has_fireplace=True,
            has_swimming_pool=False,
            has_garden=False
        )
        self.item2 = Item.objects.create(
            item_id="AEXXXXXXXX2",
            label="label2",
            short_description="short_description2",
            address="address2",
            description="description1",
            city="ottawa",
            property_type="duplex",
            status="sold",
            price=350000,
            has_fireplace=False,
            has_garage=False,
            has_swimming_pool=True
        )
        self.item3 = Item.objects.create(
            item_id="AEXXXXXXXX3",
            label="label3",
            short_description="short_description3",
            address="address3",
            description="description3",
            city="montreal",
            property_type="apartment",
            construction_age="newly_built",
            bedrooms_number="1",
            status="for_sale",
            price=100000,
            has_dining_room=True,
            has_fireplace=False,
            has_garage=True,
            has_garden=True
        )
        self.item4 = Item.objects.create(
            item_id="AEXXXXXXXX4",
            label="label4",
            short_description="short_description4",
            address="description1",
            description="description4",
            city="alma",
            property_type="apartment",
            construction_age="10_years_and_less",
            bedrooms_number="2",
            status="for_rent",
            price=550000,
            has_dining_room=False,
            has_fireplace=True,
            has_garage=True,
            has_garden=False
        )

        self.image_item1 = ItemImage.objects.create(
            image=SimpleUploadedFile(name='image_test.png', content=open(os.path.dirname(os.path.abspath(__file__)) + "/static/item/test/images/image_test.png", 'rb').read(), content_type='image/png'),
            item=self.item1
        )
        self.newsletter = Newsletter.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="to@yopmail.com",
        )

    def test_items_list(self):
        response = self.client.post(reverse('items_list'))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('items_list'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 3)  # we excluded items with status: sold

        response = self.client.get(reverse('items_list'), {
            "searched_txt": "description1"
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 2)

        response = self.client.get(reverse('items_list'), {
            "searched_txt": "descriptionj1"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 0)

        response = self.client.get(reverse('items_list'), {
            "searched_txt": "description1",
            "property_type": "apartment"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 2)

        response = self.client.get(reverse('items_list'), {
            "property_type": "apartment"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 3)

        response = self.client.get(reverse('items_list'), {
            "price_range": "300_400"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 1)

        response = self.client.get(reverse('items_list'), {
            "city": "montreal"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 2)

        response = self.client.get(reverse('items_list'), {
            "city": "ottawa"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 0)

        response = self.client.get(reverse('items_list'), {
            "building_type": "detached"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 0)

        response = self.client.get(reverse('items_list'), {
            "construction_age": "10_years_and_less"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 1)

        response = self.client.get(reverse('items_list'), {
            "item_status": "for_sale"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 2)

        response = self.client.get(reverse('items_list'), {
            "bedrooms_number": "1"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 1)

        response = self.client.get(reverse('items_list'), {
            "bathrooms_number": "1"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 0)

        response = self.client.get(reverse('items_list'), {
            "has_dining_room": "true"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 2)

        response = self.client.get(reverse('items_list'), {
            "has_fireplace": "true"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 2)

        response = self.client.get(reverse('items_list'), {
            "has_garage": "true"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 2)

        response = self.client.get(reverse('items_list'), {
            "has_swimming_pool": "true"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 0)

        response = self.client.get(reverse('items_list'), {
            "has_garden": "true"
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 1)

        response = self.client.get(reverse('items_list'), {
            "current_page": 3
        })
        content = json.loads(response.content)
        self.assertEqual(len(content["data"]), 3)

    def test_item_details(self):
        response = self.client.get(reverse('item_detail', kwargs={'pk': "None"}))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('item_detail', kwargs={'pk': "AEXXXXXXXX1"}))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('item_detail', kwargs={'pk': "AEXXXXXXXX1"}))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content["pk"], "AEXXXXXXXX1")
        self.assertEqual(content["label"], "label1")


# class SignalsTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#
#     def test_send_property_to_newsletters(self):
#         item = Item(
#             item_id="AEXXXXXXXX5",
#             label="label",
#             short_description="short_description",
#             address="address",
#             description="description",
#             city="montreal",
#             property_type="apartment",
#             price=300000,
#             has_dining_room=True,
#             has_fireplace=True,
#             has_swimming_pool=False,
#             has_garden=False
#         )
#         item.save()