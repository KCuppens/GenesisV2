from django.dispatch import Signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.filemanager.models import (
	Directory,
	Media,
	DirectoryRevision as ModelRevision1, 
	DirectoryVersion as ModelVersion1,
	MediaRevision as ModelRevision2,
	MediaVersion as ModelVersion2,
)
import datetime
import json
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from django.db import models
from apps.base import errors

def myconverter(o):
    # import pdb; pdb.set_trace()
    if isinstance(o, datetime.datetime):
        return o.__str__()
    try:
        # if o is filefield then it'll return url
        if o.url:
            return o.url
    except:
        pass


def create_new_version1(revision, serialized_instance):
    return ModelVersion1.objects.create(revision=revision,
                                      serialized_instance=serialized_instance,
                                      is_current=True)

def create_new_version2(revision, serialized_instance):
    return ModelVersion2.objects.create(revision=revision,
                                      serialized_instance=serialized_instance,
                                      is_current=True)

@receiver(post_save, sender=Directory)
def post_directoryrevision_commit(sender, instance, created, **kwargs):
    # import pdb; pdb.set_trace()
    if created:
        try:
            revision = ModelRevision1.objects.create(current_instance=instance)
        except Exception as e:
            raise errors.RegistrationError(_(str(e)))
        dict_to = model_to_dict(instance)
        response = json.dumps(dict_to, default=myconverter)
        try:
            version = create_new_version1(revision, response)
        except Exception as e:
            raise errors.RevisionManagementError(_(str(e)))
    else:
        if ModelRevision1.objects.filter(current_instance=instance).exists():
            revision = ModelRevision1.objects.get(current_instance=instance)
            dict_to = model_to_dict(instance)
            response = json.dumps(dict_to, default=myconverter)
            if not ModelVersion1.objects.filter(revision=revision, serialized_instance=response):
                try:
                    version = create_new_version1(revision, response)
                except Exception as e:
                    raise errors.RevisionManagementError(_(str(e)))
            else:
                version = revision.versions.get(serialized_instance=response)
                try:
                    if not instance.not_new_object:
                        version.date_created = datetime.datetime.now()
                    version.is_current = True
                except:
                	pass
                version.save()


@receiver(post_save, sender=Media)
def post_mediarevision_commit(sender, instance, created, **kwargs):
    # import pdb; pdb.set_trace()
    if created:
        try:
            revision = ModelRevision2.objects.create(current_instance=instance)
        except Exception as e:
            raise errors.RegistrationError(_(str(e)))
        dict_to = model_to_dict(instance)
        response = json.dumps(dict_to, default=myconverter)
        try:
            version = create_new_version2(revision, response)
        except Exception as e:
            raise errors.RevisionManagementError(_(str(e)))
    else:
        if ModelRevision2.objects.filter(current_instance=instance).exists():
            revision = ModelRevision2.objects.get(current_instance=instance)
            dict_to = model_to_dict(instance)
            response = json.dumps(dict_to, default=myconverter)
            if not ModelVersion2.objects.filter(revision=revision, serialized_instance=response):
                try:
                    version = create_new_version2(revision, response)
                except Exception as e:
                    raise errors.RevisionManagementError(_(str(e)))
            else:
                version = revision.versions.get(serialized_instance=response)
                try:
                    if not instance.not_new_object:
                        version.date_created = datetime.datetime.now()
                    version.is_current = True
                except:
                	pass
                version.save()