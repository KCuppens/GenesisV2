from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.pages.models import (
    Canvas, 
    Page, 
    PageBlock, 
    DetailPage,
    PageRevision as ModelRevision,
    PageVersion as ModelVersion
)
import datetime
import json
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from apps.base import errors



@receiver(post_save, sender=Page)
def create_canvas(sender, instance, created, **kwargs):
    """Create a canvas whenever a page object is created."""
    if created or not instance.canvas: 
        new_canvas = Canvas.objects.create()
        instance.canvas = new_canvas
        instance.save()

@receiver(post_save, sender=PageBlock)
def update_page_detail(sender, instance, created, **kwargs):
    """Update page to check if it has a block with detailpage"""
    
    if not created and instance.detailpage:
        page = instance.page
        module = instance.module
        if not module == 'Page':
            if not page.detailpage_models:
                page.detailpage_models = module
            elif page.detailpage_models and not module in page.detailpage_models:
                page.detailpage_models += ',' + module
            page.has_detailpage = True 
            page.save()

@receiver(post_save, sender=Canvas)
def update_detailpage_overridden(sender, instance, created, **kwargs):
    """Update detailpage with overridden based on canvas"""
    
    if not created:
        if instance.rows.count() > 0:
            detailpage = DetailPage.objects.filter(canvas=instance.id).first()
            if detailpage:
                detailpage.overridden = True 
                detailpage.save()
        else:
            detailpage = DetailPage.objects.filter(canvas=instance.id).first()
            if detailpage:
                detailpage.overridden = False 
                detailpage.save()

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def create_new_version(revision, serialized_instance):
    return ModelVersion.objects.create(revision=revision,
                                      serialized_instance=serialized_instance,
                                      is_current=True)

@receiver(post_save, sender=Page)
def post_pagerevision_commit(sender, instance, created, **kwargs):
    # import pdb;pdb.set_trace()
    if created:
        try:
            revision = ModelRevision.objects.create(current_instance=instance)
        except Exception as e:
            raise errors.RegistrationError(_(str(e)))
        dict_to = model_to_dict(instance)
        response = json.dumps(dict_to, default=myconverter)
        # try:
        #     version = create_new_version(revision, response)
        # except Exception as e:
        #     raise errors.RevisionManagementError(_(str(e)))
    else:
        if not kwargs.get('final_save'):
            return
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



