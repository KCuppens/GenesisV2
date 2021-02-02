from django.db import models
from apps.base.models import BaseModel, AdminModel
from django_extensions.db.fields import AutoSlugField
from apps.feathericons.fields import IconField
# Create your models here.
class Module(BaseModel, AdminModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    route = models.CharField(max_length=255, null=True, blank=True)
    models = models.CharField(max_length=255, null=True, blank=True)
    appname = models.CharField(max_length=255, null=True, blank=True)

class Tab(BaseModel, AdminModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    icon = IconField()