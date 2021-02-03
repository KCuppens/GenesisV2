from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.account.models import DeliveryAddress, InvoiceAddress
from django.utils.translation import gettext_lazy as _
from internationalflavor.vat_number import VATNumberField
from django_countries.fields import CountryField
# Create your models here.
    
class User(AbstractUser):
    USER_TYPE_PERSONAL = 'personal'
    USER_TYPE_PRIVATE = 'private'

    USER_TYPES = (
        (USER_TYPE_PERSONAL, _('Particulier')),
        (USER_TYPE_PRIVATE, _('Handelaar'))
    )    

    user_type = models.CharField(choices=USER_TYPES, default=USER_TYPE_PERSONAL, max_length=100)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    birthdate = models.DateTimeField(null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="user/images/")

    front_client = models.BooleanField(default=True, null=True, blank=True)

    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_vat = VATNumberField(countries=['NL','BE'], null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE, null=True, blank=True)
    invoice_address = models.ForeignKey(InvoiceAddress, on_delete=models.CASCADE, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)
    #permissions
    #country
    #address
    #own_website
    
    #facebook_url
    #twitter_url
    #youtube_url
    #instagram_url

    class Meta:
        verbose_name = _('Gebruiker')
        verbose_name_plural = _('Gebruikers')

    def get_full_name(self):
        """ Return the email."""
        return self.email

    def get_short_name(self):
        """ Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    def activate(self):
        self.is_active = True
        self.save()
