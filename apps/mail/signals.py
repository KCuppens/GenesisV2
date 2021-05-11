from django.dispatch import Signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.mail.models import (
	MailTemplate,
	MailConfig,
	MailTemplateRevision as ModelRevision1, 
	MailTemplateVersion as ModelVersion1,
	MailConfigRevision as ModelRevision2,
	MailConfigVersion as ModelVersion2,
)
import datetime
import json
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from apps.base import errors

email_queued = Signal(providing_args=['emails'])
"""
This signal is triggered whenever one or more emails are pushed into its queue.
The Emails objects added to the queue are passed as list to the callback handler. 
It can be connected to any handler function using this signature:
Example:
    from django.dispatch import receiver
    from post_office.signal import email_queued
    @receiver(email_queued)
    def my_callback(sender, emails, **kwargs):
        print("Just added {} mails to the sending queue".format(len(emails)))
"""

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def create_new_version1(revision, serialized_instance):
    return ModelVersion1.objects.create(revision=revision,
                                      serialized_instance=serialized_instance,
                                      is_current=True)

def create_new_version2(revision, serialized_instance):
    return ModelVersion2.objects.create(revision=revision,
                                      serialized_instance=serialized_instance,
                                      is_current=True)

@receiver(post_save, sender=MailTemplate)
def post_mailtemplaterevision_commit(sender, instance, created, **kwargs):
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


@receiver(post_save, sender=MailConfig)
def post_mailconfigrevision_commit(sender, instance, created, **kwargs):
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