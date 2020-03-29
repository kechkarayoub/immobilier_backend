# -*- coding: utf-8 -*-
from backend.static_variables import TYPES
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from item.models import Item
import datetime


YEARMONTH_INPUT_FORMATS = (
    '%m-%Y', '%m/%Y', # '2006-10', '10/2006'
)


class GroupClient(models.Model):
    class Meta:
        db_table = "group_client"

    group_name = models.CharField(_("Nom du groupe"), blank=False, default="", max_length=30)
    is_active = models.BooleanField(_("Est active"), default=True)
    reminder_payment_email_footer_line1 = models.CharField(
        _("1ere line du footer de l'email"), blank=True, default="Cordialement,", max_length=765, null=True
    )
    reminder_payment_email_footer_line2 = models.CharField(
        _("2eme line du footer de l'email"), blank=True, default="Jalil ELMAHBOUBI", max_length=765, null=True
    )
    reminder_payment_email_message1 = models.TextField(
        _("Paragraphe 1 de l'email de rappel de paiment"), blank=False,
        default="Veuillez payer votre loyer le 1er du mois. Si vous payer par Interac, veuillez utiliser le courriel"
                " suivant: Jalil.elmahboubi@gmail.com",
        help_text="Utiliser 'br/' à l'intérieur de <> pour retourner à la ligne.", null=False
    )
    reminder_payment_email_message2 = models.TextField(
        _("Paragraphe 2 de l'email de rappel de paiment"), blank=True,
        default="Une pénalité de 25.00$ sera ajouter après le 5 de chaque mois. \r\n Une pénalité de 125$ et demande "
                "de résiliation de votre bail si le retard dépasse 3 semaines.",
        help_text="Utiliser 'br/' à l'intérieur de <> pour retourner à la ligne.", null=True
    )
    reminder_payment_email_message3 = models.TextField(
        _("Paragraphe 3 de l'email de rappel de paiment"), blank=True, default="",
        help_text="Utiliser 'br/' à l'intérieur de <> pour retourner à la ligne.", null=True
    )
    reminder_payment_email_object = models.CharField(
        _("Sujet de l'email de rappel de paiment"), blank=False,
        default="Rappelle: Paiement du loyer", max_length=765, null=False
    )

    def __str__(self):
        return self.group_name
    @classmethod
    def get_reminder_email_data(cls):
        try:
            return cls.objects.get().to_reminder_email_data()
        except:
            return {
                "object": "Rappelle: Paiement du loyer",
                "message_1": "Veuillez payer votre loyer le 1er du mois. Si vous payer par Interac, veuillez utiliser"
                             " le courriel suivant: Jalil.elmahboubi@gmail.com",
                "message_2": "Une pénalité de 25.00$ sera ajouter après le 5 de chaque mois. \r\n Une pénalité de 125$ "
                             "et demande de résiliation de votre bail si le retard dépasse 3 semaines.",
                "message_3": "",
                "footer_1": "Cordialement,",
                "footer_2": "Jalil ELMAHBOUBI",
            }

    def to_reminder_email_data(self):
        return {
            "object": self.reminder_payment_email_object,
            "message_1": self.reminder_payment_email_message1,
            "message_2": self.reminder_payment_email_message2,
            "message_3": self.reminder_payment_email_message3,
            "footer_1": self.reminder_payment_email_footer_line1,
            "footer_2": self.reminder_payment_email_footer_line2,
        }


class Client(models.Model):
    class Meta:
        db_table = "client"

    address = models.CharField(_("Adresse"), blank=True, max_length=510, null=True)
    apartment = models.CharField(_("Appartement"), blank=True, max_length=255, null=True)
    createdAt = models.DateTimeField(_("Créé le"), auto_now_add=True)
    email = models.EmailField(_("Email"), null=True)
    first_name = models.CharField(_("Prénom"), blank=False, max_length=30)
    group_client = models.ForeignKey(GroupClient, on_delete=models.CASCADE, related_name="clients", null=True)
    is_active = models.BooleanField(_("Est active"), default=True)
    last_name = models.CharField(_("Nom"), blank=False, max_length=30)
    phone = models.CharField(_("Téléphone"), blank=True, default="", max_length=20)
    type = models.CharField(_("Type"), blank=True, choices=TYPES, default="locataire", max_length=20)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.full_name()


class YearMonthField(models.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid year and month.'),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super(YearMonthField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats

    def clean(self, value, hh):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return format(value, '%m/%Y')
        if isinstance(value, datetime.date):
            return format(value, '%m/%Y')
        for fmt in self.input_formats or YEARMONTH_INPUT_FORMATS:
            try:
                date = datetime.datetime.strptime(value, fmt)
                return format(date, '%m/%Y')
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])


