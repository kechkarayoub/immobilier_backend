# -*- coding: utf-8 -*-
from backend import static_variables
from backend.utils import choices_format_to_tuple
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


class Funding(models.Model):
    class Meta:
        db_table = "funding"

    bank_email = models.EmailField(_("Email"), blank=True, max_length=255, null=True)
    bank_logo = models.ImageField(
        help_text=_("Logo de la banque."),
        null=False,
        upload_to=settings.IMAGES_FOLDER + 'funding/UsersImages'  # lien de l'image: /media/images/funding/UsersImages/*.*
    )
    bank_name = models.CharField(_("Nom de la banque"), blank=False, max_length=30)
    createdAt = models.DateTimeField(_("Créé le"), auto_now_add=True)
    free_field_label = models.CharField(_("Étiquette du champ libre"), blank=True, max_length=255, null=True)
    free_field_value = models.CharField(_("Valeur du champ libre"), blank=True, max_length=1024, null=True)

    def __str__(self):
        return str(self.id)
