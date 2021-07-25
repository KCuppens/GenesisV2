from apps.pages.models import Page
from apps.filemanager.models import Media
from django import forms, template
register = template.Library()
from django.conf import settings

@register.simple_tag
def show_video(instance):
    if settings.AWS_ACTIVE:
        return settings.AWS_CLOUDFRONT_DOMAIN + settings.AWS_MAIN_DIR + str(instance.video)
    else:
        return str(instance.video) 