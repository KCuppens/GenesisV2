from apps.pages.models import Page
from apps.filemanager.models import Media
from django import forms, template
register = template.Library()
from django.conf import settings

@register.simple_tag
def show_file(instance):
    if settings.AWS_ACTIVE:
        return settings.AWS_CLOUDFRONT_DOMAIN + str(instance.media_path)
    else:
        return str(instance.file)