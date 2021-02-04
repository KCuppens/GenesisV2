from django.db import models
import datetime 
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
User = get_user_model()
from django.utils.translation import ugettext as _

from django.dispatch import receiver
try:
    from apps.history.models import History
except ImportError:  # pragma: no cover
    from apps.history.models import History


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

    def save(self, *args, **kwargs):
        super(AdminModel, self).save(*args, **kwargs)

    @receiver(post_save)
    def create_history_record(sender, instance, **kwargs):
        apps = ['User','DashboardConfiguration','Session','Migration']
        if not instance.__class__.__name__ in apps:
            if kwargs.get('created'):
                message = _('Er is een %s toegevoegd!').format(s=instance._meta.verbose_name.title())
                History.objects.create(action=message, module=instance.__class__.__name__, user=instance.edited_by)
            elif instance.date_deleted:
                message = _('Er is een %s verwijderd').format(s=instance._meta.verbose_name.title())
                History.objects.create(action=message, module=instance.__class__.__name__, user=instance.edited_by)
            else:
                message = _('Er is een %s geüpdate!').format(s=instance._meta.verbose_name.title())
                History.objects.create(action=message, module=instance.__class__.__name__, user=instance.edited_by)


