from django.db import models
from django.utils.html import mark_safe

# Create your models here.
class Icon(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.name
