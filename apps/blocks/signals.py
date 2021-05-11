from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.blocks.models import (
    Block, 
    BlocksRevision as ModelRevision, 
    BlocksVersion as ModelVersion
)
import datetime
import json
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from apps.base import errors

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def create_new_version(revision, serialized_instance):
    return ModelVersion.objects.create(revision=revision,
                                      serialized_instance=serialized_instance,
                                      is_current=True)

@receiver(post_save, sender=Block)
def post_formrevision_commit(sender, instance, created, **kwargs):
    # import pdb; pdb.set_trace()
    if created:
        try:
            revision = ModelRevision.objects.create(current_instance=instance)
        except Exception as e:
            raise errors.RegistrationError(_(str(e)))
        dict_to = model_to_dict(instance)
        response = json.dumps(dict_to, default=myconverter)
        try:
            version = create_new_version(revision, response)
        except Exception as e:
            raise errors.RevisionManagementError(_(str(e)))
    else:
        if ModelRevision.objects.filter(current_instance=instance).exists():
            revision = ModelRevision.objects.get(current_instance=instance)
            dict_to = model_to_dict(instance)
            response = json.dumps(dict_to, default=myconverter)
            if not ModelVersion.objects.filter(revision=revision, serialized_instance=response):
                try:
                    version = create_new_version(revision, response)
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