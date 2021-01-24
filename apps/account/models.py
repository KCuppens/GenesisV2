from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from internationalflavor.vat_number import VATNumberField
from django_countries.fields import CountryField
# Create your models here.

class InvoiceAddress(models.Model):
    street = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    box = models.CharField(max_length=255, null=True, blank=True)
    postal = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField()

    def get_full_address(self):
        address = ''
        if self.street:
            address += self.street + ' '
        if self.number:
            address += self.number + ' '
        if self.box:
            address += self.box + ' '
        if self.postal:
            address += self.postal + ' '
        if self.city:
            address += self.city + ' '
        if self.country:
            address += self.country.name
        return address


class DeliveryAddress(models.Model):
    street = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    box = models.CharField(max_length=255, null=True, blank=True)
    postal = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField()

    def get_full_address(self):
        address = ''
        if self.street:
            address += self.street + ' '
        if self.number:
            address += self.number + ', '
        if self.box:
            address += self.box + ' '
        if self.postal:
            address += self.postal + ' '
        if self.city:
            address += self.city + ', '
        if self.country:
            address += self.country.name
        return address