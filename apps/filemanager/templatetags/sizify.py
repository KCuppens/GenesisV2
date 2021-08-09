from django import forms, template
register = template.Library()
from apps.filemanager.utils import get_size
from apps.filebase.file import get_file_size
from django.conf import settings

@register.simple_tag
def sizify(value):
    if settings.AWS_ACTIVE:
        file_size = get_file_size(settings.AWS_IMAGE_BUCKET, str(value))
        if file_size:
            return get_size(file_size)
        return '' 
    else:
        return get_size(value.size)