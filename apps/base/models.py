from django.db import models
import datetime 
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class SeoModel(models.Model):
    meta_title = models.CharField(null=True, max_length=55, blank=True, db_index=True)
    meta_keywords = models.TextField(null=True, max_length=255, blank=True)
    meta_description = models.TextField(null=True, blank=True)

class SortableModel(models.Model):
    position = models.IntegerField(blank=False, default=999999, db_index=True)

class BaseModel(models.Model):  
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    date_expired = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

class AdminModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_author', null=True,blank=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_edited_by',null=True, blank=True)
    deletable = models.BooleanField(default=True)