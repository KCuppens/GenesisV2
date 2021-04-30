from django.db import models
from apps.base.models import BaseModel, SeoModel, AdminModel
from django_extensions.db.fields import AutoSlugField
from django.db.models import Q
import datetime 
now = datetime.datetime.now()
# Create your models here.
class ArticleManager(models.Manager):
    def get_actives(self, sort_method, sort_order):
        if str(sort_order) == 'asc' and str(sort_method) == 'date':
            return self.filter(Q(date_expired__gte=now) | Q(date_expired__isnull=True), active=True, date_deleted=None, date_published__lte=now).order_by('date_published')
        elif str(sort_order) == 'desc' and str(sort_method) == 'date':
            return self.filter(Q(date_expired__gte=now) | Q(date_expired__isnull=True), active=True, date_deleted=None, date_published__lte=now).order_by('-date_published')
        elif str(sort_order) == 'asc' and str(sort_method) == 'name':
            return self.filter(Q(date_expired__gte=now) | Q(date_expired__isnull=True), active=True, date_deleted=None, date_published__lte=now).order_by('title')
        elif str(sort_order) == 'desc' and str(sort_method) == 'name':
            return self.filter(Q(date_expired__gte=now) | Q(date_expired__isnull=True), active=True, date_deleted=None, date_published__lte=now).order_by('-title')
        else:
            return self.filter(Q(date_expired__gte=now) | Q(date_expired__isnull=True), active=True, date_deleted=None, date_published__lte=now)


class Article(BaseModel, SeoModel, AdminModel):
    title = models.CharField(max_length=255, null=True, db_index=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    gallery = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title')
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    objects = ArticleManager()
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title