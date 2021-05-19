from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.news.models import Article,  NewsRevision, NewsVersion
from apps.pages.models import DetailPage, Canvas
import datetime
import json
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from apps.base import errors


@receiver(post_save, sender=Article)
def create_detailpage(sender, instance, created, **kwargs):
    """Create a detailpage for every article object"""
    if created:
        model_name = instance.__class__.__name__
        if not DetailPage.objects.filter(model=model_name, object_id__isnull=True, default=True).first():
            canvas_obj = Canvas.objects.create()
            DetailPage.objects.create(model=model_name, default=True, canvas=canvas_obj)
        
        if not DetailPage.objects.filter(model=model_name, object_id=instance.id, default=False).first():
            canvas_obj = Canvas.objects.create()
            DetailPage.objects.create(model=model_name, default=False, canvas=canvas_obj, object_id=instance.id)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def create_new_version(revision, serialized_instance):
    version = NewsVersion.objects.create(revision=revision,
                                      serialized_instance=serialized_instance,
                                      is_current=True)
    return version

@receiver(post_save, sender=Article)
def post_revision_commit(sender, instance, created, **kwargs):
    if created:
        try:
            revision = NewsRevision.objects.create(current_instance=instance)
        except Exception as e:
            raise errors.RegistrationError(_(str(e)))
        dict_to = model_to_dict(instance)
        response = json.dumps(dict_to, default=myconverter)
        try:
            version = create_new_version(revision, response)
        except Exception as e:
            raise errors.RevisionManagementError(_(str(e)))
    else:
        if NewsRevision.objects.filter(current_instance=instance).exists():
            revision = NewsRevision.objects.get(current_instance=instance)
            dict_to = model_to_dict(instance)
            response = json.dumps(dict_to, default=myconverter)
            if not NewsVersion.objects.filter(revision=revision, serialized_instance=response):
                try:
                    version = create_new_version(revision, response)
                except Exception as e:
                    raise errors.RevisionManagementError(_(str(e)))
            else:
                version = revision.versions.get(serialized_instance=response)
                try:
                    if not instance.not_new_object:
                        version.date_created = datetime.datetime.now()
                except:
                    pass
                version.is_current = True
                version.save()
