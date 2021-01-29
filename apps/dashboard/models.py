from django.db import models
# Create your models here.
class DashboardConfiguration(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False, null=True, blank=True)
    #modules