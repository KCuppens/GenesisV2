from django.db import models

# Create your models here.
class Icon(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)