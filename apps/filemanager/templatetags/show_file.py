from apps.pages.models import Page
from apps.filemanager.models import Media
from apps.filemanager.utils import get_filename
from django import forms, template
from apps.filemanager.models import Media
register = template.Library()
from django.conf import settings

@register.simple_tag
def show_file(instance):
    if isinstance(instance, str):
        return settings.AWS_CLOUDFRONT_DOMAIN + str(instance)
    elif isinstance(instance, Media):
        return settings.AWS_CLOUDFRONT_DOMAIN + settings.AWS_MAIN_DIR + str(instance.filename)
    else:
        return settings.AWS_CLOUDFRONT_DOMAIN + str(instance)