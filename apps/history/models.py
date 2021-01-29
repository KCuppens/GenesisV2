from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class History(models.Model):
    action = models.CharField(null=True, blank=True, max_length=255)
    module = models.CharField(null=True, blank=True, max_length=55, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_index=True)