# -*- coding: utf-8 -*-


from backend import static_variables
from backend.utils import choices_format_to_tuple
from django.db import models
from django.utils.translation import ugettext as _


class Contact(models.Model):
    class Meta:
        db_table = "contact"

    createdAt = models.DateTimeField(_("Créé le"), auto_now_add=True)
    email = models.EmailField(_("Email"), null=False)
    first_name = models.CharField(_("Prénom"), blank=False, max_length=30)
    last_name = models.CharField(_("Nom"), blank=False, max_length=30)
    message = models.TextField(_("Message"), blank=False, null=False)
    object = models.CharField(_("Sujet"), blank=False, max_length=30)
    phone = models.CharField(_("Téléphone"), blank=True, default="", max_length=20)


class ContactBuy(models.Model):
    class Meta:
        db_table = "contact_buy"

    bathrooms_number = models.CharField(
        _("Nombre de salles de bain"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.BATHROOMS_NUMBER),
        default='',
        max_length=10
    )
    bedrooms_number = models.CharField(
        _("Nombre de chambres"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.BEDROOMS_NUMBER),
        default='',
        max_length=10
    )
    building_type = models.CharField(
        _("Type de bâtiment"),
        default='',
        blank=True,
        max_length=50,
        choices=choices_format_to_tuple(static_variables.BUILDINGS_TYPES))
    city = models.CharField(
        _("Ville"),
        choices=choices_format_to_tuple(static_variables.CANADIAN_CITIES),
        default='',
        max_length=100
    )
    construction_age = models.CharField(
        _("L'âge du construction"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.CONSTRUCTION_AGE),
        default='',
        max_length=20
    )
    createdAt = models.DateTimeField(_("Créé le"), auto_now_add=True)
    email = models.EmailField(_("Email"), null=False)
    first_name = models.CharField(_("Prénom"), blank=False, max_length=30)
    has_dining_room = models.BooleanField(_("Salle à manger"), default=False)
    has_fireplace = models.BooleanField(_("Cheminée"), default=False)
    has_garage = models.BooleanField(_("Garage"), default=False)
    has_garden = models.BooleanField(_("Jardin"), default=False)
    has_swimming_pool = models.BooleanField(_("Piscine"), default=False)
    has_been_processed = models.BooleanField(_("A été traité"), default=True)
    last_name = models.CharField(_("Nom"), blank=False, max_length=30)
    lot_size_min = models.PositiveIntegerField(_("Taille minimale de la propriété(m²)"), default=0,)
    lot_size_max = models.PositiveIntegerField(_("Taille maximale de la propriété max(m²)"), default=0,)
    occupation_date = models.DateField(_("Date d'occupation"), null=True)
    other_characteristics = models.TextField(_("Autres caractéristiques"), blank=True, null=True)
    phone = models.CharField(_("Téléphone"), blank=True, default="", max_length=20)
    price_range = models.CharField(
        _("Intervalle de prix"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.PRICES_RANGES),
        default='',
        max_length=50
    )
    property_type = models.CharField(
        _("Type de la Propriété"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.PROPERTIES_TYPES),
        default='',
        max_length=50
    )
    status = models.CharField(
        _("Statut"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.ITEMS_STATUS),
        default='for_sale',
        max_length=20
    )


class ContactRent(models.Model):
    class Meta:
        db_table = "contact_rent"

    bathrooms_number = models.CharField(
        _("Nombre de salles de bain"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.BATHROOMS_NUMBER),
        default='',
        max_length=10
    )
    bedrooms_number = models.CharField(
        _("Nombre de chambres"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.BEDROOMS_NUMBER),
        default='',
        max_length=10
    )
    building_type = models.CharField(
        _("Type de bâtiment"),
        default='',
        blank=True,
        max_length=50,
        choices=choices_format_to_tuple(static_variables.BUILDINGS_TYPES))
    city = models.CharField(
        _("Ville"),
        choices=choices_format_to_tuple(static_variables.CANADIAN_CITIES),
        default='',
        max_length=100
    )
    construction_age = models.CharField(
        _("L'âge du construction"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.CONSTRUCTION_AGE),
        default='',
        max_length=20
    )
    createdAt = models.DateTimeField(_("Créé le"), auto_now_add=True)
    email = models.EmailField(_("Email"), null=False)
    first_name = models.CharField(_("Prénom"), blank=False, max_length=30)
    has_dining_room = models.BooleanField(_("Salle à manger"), default=False)
    has_fireplace = models.BooleanField(_("Cheminée"), default=False)
    has_garage = models.BooleanField(_("Garage"), default=False)
    has_garden = models.BooleanField(_("Jardin"), default=False)
    has_swimming_pool = models.BooleanField(_("Piscine"), default=False)
    has_been_processed = models.BooleanField(_("A été traité"), default=True)
    last_name = models.CharField(_("Nom"), blank=False, max_length=30)
    lot_size_min = models.PositiveIntegerField(_("Taille minimale de la propriété(m²)"), default=0,)
    lot_size_max = models.PositiveIntegerField(_("Taille maximale de la propriété(m²)"), default=0,)
    occupation_date = models.DateField(_("Date d'occupation"), null=True)
    other_characteristics = models.TextField(_("Autres caractéristiques"), blank=True, null=True)
    phone = models.CharField(_("Téléphone"), blank=True, default="", max_length=20)
    price_range = models.CharField(
        _("Intervalle de prix"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.PRICES_RANGES),
        default='',
        max_length=50
    )
    property_type = models.CharField(
        _("Type de la Propriété"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.PROPERTIES_TYPES),
        default='',
        max_length=50
    )
    status = models.CharField(
        _("Statut"),
        blank=True,
        choices=choices_format_to_tuple(static_variables.ITEMS_STATUS),
        default='for_sale',
        max_length=20
    )
