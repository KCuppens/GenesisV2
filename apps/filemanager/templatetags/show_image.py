from apps.pages.models import Page
from apps.filemanager.models import Media
from django import forms, template
register = template.Library()
from django.conf import settings

@register.simple_tag
def show_image(instance):
    if settings.AWS_ACTIVE:
        return settings.AWS_CLOUDFRONT_DOMAIN + settings.AWS_MAIN_DIR + str(instance.image)
    else:
        return str(instance.image)