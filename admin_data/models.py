# -*- coding: utf-8 -*-


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _


class AdminData(models.Model):
    class Meta:
        db_table = "admin_data"

    address = models.CharField(_("Adresse"), blank=False, max_length=510, null=False)
    agency_name = models.CharField(_("Nom de l'agence"), blank=False, max_length=255, null=False)
    email = models.CharField(_("Email"), blank=False, default="Jalil.elmahboubi@gmail.com", max_length=255, null=False)
    enable_map = models.BooleanField(_("Activer la carte"), default=True)
    fax = models.CharField(_("Fax"), blank=False, default="450 462 1509", max_length=255, null=False)
    full_name = models.CharField(_("Nom complet"), blank=False, default="ELMAHBOUBI Abdjalil", max_length=255, null=False)
    gps_latitude = models.FloatField(_("GPS Latitude"), blank=True, default=45.474459, null=True)
    gps_longitude = models.FloatField(_("GPS Longitude"), blank=True, default=-73.470234, null=True)
    image = models.ImageField(help_text=_("L'image de l'administrateur"), null=False, upload_to=settings.IMAGES_FOLDER + 'admin_data')
    tel = models.CharField(_("Téléphone"), blank=False, default="514 967 3743", max_length=255, null=False)

    def __str__(self):
        return "Admin data"

    @classmethod
    def get_admin_email(cls):
        try:
            return cls.objects.get().email
        except:
            if settings.ENVIRONMENT == "development":
                return "kechkarayoub@gmail.com"
            return "Jalil.elmahboubi@gmail.com"

    @classmethod
    def get_admin_data(cls):
        try:
            return cls.objects.get().to_dict()
        except:
            return {
                "full_name": "ELMAHBOUBI Jalil",
                "agency_name": "Royal Le page Triomphe",
                "address": "2190, Boul. Lapiniere, Brossard PQ J4W 1M2",
                "email": cls.get_admin_email(),
                "image": "",
                "tel": "514 967 3743",
                "fax": "450 462 1509",
                "position": {
                    "gps_latitude": 45.474459,
                    "gps_longitude": -73.470234,
                }
            }

    def to_dict(self):
        res = {
            "address": self.address,
            "agency_name": self.agency_name,
            "email": self.email,
            "enable_map": self.address,
            "fax": self.fax,
            "full_name": self.full_name,
            "image": settings.BACKEND_URL_ROOT + self.image.url,
            "tel": self.tel
        }
        if self.enable_map:
            res["position"] = {
                "gps_latitude": self.gps_latitude,
                "gps_longitude": self.gps_longitude
            }
        return res