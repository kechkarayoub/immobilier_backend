# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext as _


class SocialLink(models.Model):
    class Meta:
        db_table = "social_link"

    FA_ICONS = (
        ("", "Select"),
        ("facebook", "Facebook"),
        ("google-plus", "G+"),
        ("instagram", "Instagram"),
        ("linkedin", "Linkedin"),
        ("twitter", "Twitter"),
        ("youtube", "Youtube"),
    )
    fa_icon = models.CharField(_("Fa icon"), blank=False, default="", choices=FA_ICONS, max_length=20)
    is_active = models.BooleanField(_("Est active"), default=True)
    label = models.CharField(_("Étiquette"), blank=False, max_length=30)
    url = models.CharField(_("Url"), blank=False, default="", max_length=120)
