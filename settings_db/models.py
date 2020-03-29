# -*- coding: utf-8 -*-


from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


class SettingsDb(models.Model):
    class Meta:
        db_table = "settings_db"

    header_image = models.ImageField(
        blank=True,
        help_text=_("Image d'en-tête"),
        null=True,
        upload_to=settings.IMAGES_FOLDER + 'settings_db/header'
    )
    header_background_image = models.ImageField(
        blank=True,
        help_text=_("Image d'arrière-plan de l'en-tête"),
        null=True,
        upload_to=settings.IMAGES_FOLDER + 'settings_db/header'
    )
    header_text_color = ColorField(_("Couleur du texte de l'en-tête"), default='#FFFFFF')
    logo = models.ImageField(
        blank=True, help_text=_("Image logo"), null=True, upload_to=settings.IMAGES_FOLDER + 'settings_db/header'
    )
    main_bg_image = models.ImageField(
        blank=True,
        help_text=_("Image d'arrière-plan du body"),
        null=True,
        upload_to=settings.IMAGES_FOLDER + 'settings_db/header'
    )
    site_name = models.CharField(_("Nom du site"), blank=False, max_length=255, null=False)

    home_page_title_1 = models.CharField(_("1er ligne du titre"), blank=False, max_length=765, null=False)
    home_page_title_2 = models.CharField(_("2eme ligne du titre"), blank=True, max_length=765, null=True)

    home_page_row_1_title = models.CharField(_("Titre de la première partie"), blank=True, max_length=510, null=True)
    home_page_row_1_p_1 = models.TextField(_("1er paragraphe de la première partie"), blank=True, null=True)
    home_page_row_1_p_2 = models.TextField(_("2eme paragraphe de la première partie"), blank=True, null=True)
    home_page_row_1_p_3 = models.TextField(_("3eme paragraphe de la première partie"), blank=True, null=True)

    home_page_row_2_title = models.CharField(_("Titre de la deuxième partie"), blank=True, max_length=510, null=True)
    home_page_row_2_p_1 = models.TextField(_("1er paragraphe de la deuxième partie"), blank=True, null=True)
    home_page_row_2_p_2 = models.TextField(_("2eme paragraphe de la deuxième partie"), blank=True, null=True)
    home_page_row_2_p_3 = models.TextField(_("3eme paragraphe de la deuxième partie"), blank=True, null=True)

    home_page_row_3_title = models.CharField(_("Titre de la troisième partie"), blank=True, max_length=510, null=True)
    home_page_row_3_p_1 = models.TextField(_("1er paragraphe de la troisième partie"), blank=True, null=True)
    home_page_row_3_p_2 = models.TextField(_("2eme paragraphe de la troisième partie"), blank=True, null=True)
    home_page_row_3_p_3 = models.TextField(_("3eme paragraphe de la troisième partie"), blank=True, null=True)

    def __str__(self):
        return "Settings databases"

    @classmethod
    def get_site_name(cls):
        try:
            return cls.objects.get().site_name
        except:
            return "Site name"

    @classmethod
    def get_header_settings(cls):
        try:
            return cls.objects.get().to_header_settings()
        except:
            return {
                "header_image": "",
                "header_background_image": "",
                "header_text_color": "#FFFFFF",
                "logo": "",
                "mainBgImage": "",
                "site_name": cls.get_site_name(),
            }

    def to_header_settings(self):
        return {
                "header_image": (settings.BACKEND_URL_ROOT + self.header_image.url)
                if self.header_image and self.header_image .url else "",
                "header_background_image": (settings.BACKEND_URL_ROOT + self.header_background_image.url)
                if self.header_background_image and self.header_background_image else "",
                "header_text_color": self.header_text_color,
                "logo": (settings.BACKEND_URL_ROOT + self.logo.url) if self.logo and self.logo.url else "",
                "mainBgImage": (settings.BACKEND_URL_ROOT + self.main_bg_image.url)
                if self.main_bg_image and self.main_bg_image.url else "",
                "site_name": SettingsDb.get_site_name(),
        }

    @classmethod
    def get_home_page_data(cls):
        try:
            return cls.objects.get().to_home_page_data()
        except:
            return {
                "empty": True
            }

    def to_home_page_data(self):
        return {
            "home_page_title_1": self.home_page_title_1,
            "home_page_title_2": self.home_page_title_2,
            "home_page_row_1_title": self.home_page_row_1_title,
            "home_page_row_1_p_1": self.home_page_row_1_p_1,
            "home_page_row_1_p_2": self.home_page_row_1_p_2,
            "home_page_row_1_p_3": self.home_page_row_1_p_3,
            "home_page_row_2_title": self.home_page_row_2_title,
            "home_page_row_2_p_1": self.home_page_row_2_p_1,
            "home_page_row_2_p_2": self.home_page_row_2_p_2,
            "home_page_row_2_p_3": self.home_page_row_2_p_3,
            "home_page_row_3_title": self.home_page_row_3_title,
            "home_page_row_3_p_1": self.home_page_row_3_p_1,
            "home_page_row_3_p_2": self.home_page_row_3_p_2,
            "home_page_row_3_p_3": self.home_page_row_3_p_3,
        }


# class ExecutedBackup(models.Model):
#     class Meta:
#         db_table = "executed_backup"
#
#     comment = models.TextField(default="")
#     createdAt = models.DateTimeField(_("Created at"), auto_now_add=True)
#     is_automatically = models.BooleanField(_("Is automatically"), default=True)
