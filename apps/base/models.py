from django.db import models
import datetime 
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
User = get_user_model()
from django.utils.translation import ugettext as _
import uuid
from django.dispatch import receiver
try:
    from apps.history.models import History
except ImportError:  # pragma: no cover
    from apps.history.models import History


# Create your models here.
class SeoModel(models.Model):
    meta_title = models.CharField(null=True, max_length=55, blank=True, db_index=True, verbose_name=_('Meta title'))
    meta_keywords = models.TextField(null=True, max_length=255, blank=True, verbose_name=_('Meta keywords'))
    meta_description = models.TextField(null=True, blank=True, verbose_name=_('Meta description'))

    class Meta:
        abstract = True

class SortableModel(models.Model):
    position = models.IntegerField(blank=False, default=999999, db_index=True, verbose_name=_('Position'))

    class Meta:
        abstract = True

class BaseModel(models.Model):  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_published = models.DateTimeField(default=datetime.datetime.now(), blank=True, null=True, verbose_name=_('Publishingdate'))
    date_expired = models.DateTimeField(blank=True, null=True, verbose_name=_('Expiring date'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date of last update'))
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name=_('Delete date'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))

    def get_status(self):
        return self.active and (self.date_published <= now) and (self.date_expired == None or self.date_expired > now)

    class Meta:
        abstract = True

class AdminModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_author', null=True,blank=True, verbose_name=_('Author'))
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_edited_by',null=True, blank=True, verbose_name=_('Edited by'))
    deletable = models.BooleanField(default=True, verbose_name=_('Deletable'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(AdminModel, self).save(*args, **kwargs)

    @receiver(post_save)
    def create_history_record(sender, instance, **kwargs):
        apps = ['PageBlockElement','User','DashboardConfiguration','Session','Migration','History','Icon','Configuration','TranslationEntry','Thumbnail','DetailPage', 'MessageLog', 'FormPage', 'FormElement', 'FormElementOption','FormResult','FormResultField', 'Email']
        if not instance.__class__.__name__ in apps:
            if instance.edited_by:
                user = instance.edited_by 
            else:
                user = instance.author

            if kwargs.get('created'):
                message = _('Er is een {model} toegevoegd!').format(model=instance._meta.verbose_name.title())
                History.objects.create(action=message, module=instance.__class__.__name__, user=user)
            elif instance.date_deleted:
                message = _('Er is een {model} verwijderd').format(model=instance._meta.verbose_name.title())
                History.objects.create(action=message, module=instance.__class__.__name__, user=user)
            else:
                message = _('Er is een {model} geüpdate!').format(model=instance._meta.verbose_name.title())
                History.objects.create(action=message, module=instance.__class__.__name__, user=user)


