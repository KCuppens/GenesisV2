from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Configuration(models.Model):
    USER_MODEL = 'user'
    CLIENT_MODEL = 'client'
    
    AVAILABLE_MODELS = (
        (USER_MODEL, _('Gebruiker')),
        (CLIENT_MODEL, _('Klant'))
    )
    key_name = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    value = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    conf_type = models.CharField(choices=AVAILABLE_MODELS, default=USER_MODEL, max_length=100)

