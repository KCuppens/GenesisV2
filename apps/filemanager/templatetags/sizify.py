from django import forms, template
register = template.Library()
from apps.filemanager.utils import get_size

@register.simple_tag
def sizify(value):
    if value:
        return get_size(value)
    return ''