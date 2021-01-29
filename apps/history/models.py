from django.db import models

# Create your models here.
class History(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    action = models.CharField(null=True, blank=True, max_length=255)
    module = models.CharField(null=True, blank=True, max_length=55, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_index=True)