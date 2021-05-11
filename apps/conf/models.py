from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.
class Configuration(models.Model):
    USER_MODEL = 'user'
    CLIENT_MODEL = 'client'
    GENERAL_MODEL = 'general'
    SCHEMA_MODEL = 'schema'
    MAIL_MODEL = 'mail'

    
    AVAILABLE_MODELS = (
        (USER_MODEL, _('Gebruiker')),
        (CLIENT_MODEL, _('Klant')),
        (GENERAL_MODEL, _('Algemeen')),
        (SCHEMA_MODEL, _('Schema Markup')),
        (MAIL_MODEL, _('Mail'))
    )

    TYPE_TEXT = 'text'
    TYPE_BOOLEAN = 'boolean'

    TYPES = [
        (TYPE_TEXT, _('Textvalue')),
        (TYPE_BOOLEAN , _('Booleanvalue')),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    key_name = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    value = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    conf_type = models.CharField(choices=AVAILABLE_MODELS, default=USER_MODEL, max_length=100)
    type = models.CharField(max_length=22, choices=TYPES, default=TYPE_TEXT)

    class Meta:
        verbose_name = _('Configuration')

    def __str__(self):
        return self.value

