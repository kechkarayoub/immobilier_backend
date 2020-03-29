# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class LinkCategory(models.Model):
    class Meta:
        db_table = "link_category"

    label = models.CharField(_("Étiquette"), blank=False, max_length=510, null=False)

    def __str__(self):
        return str(self.id)


class UsefulLink(models.Model):
    class Meta:
        db_table = "useful_link"

    label = models.CharField(_("Étiquette"), blank=False, max_length=510, null=False)
    url = models.CharField(_("Url"), blank=False, max_length=510, null=False)
    category = models.ForeignKey(
        LinkCategory,
        db_index=True,
        help_text=_("Catégorie du lien"),
        on_delete=models.CASCADE,
        related_name="links"
    )

    def __str__(self):
        return str(self.id)
