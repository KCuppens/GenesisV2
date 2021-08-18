from apps.pages.models import Page
from django import forms, template
register = template.Library()
from django.template.loader import render_to_string
from django.conf import settings

@register.simple_tag
def return_language_redirect(lng, path):
    default = settings.LANGUAGE_CODE
    nr_slashes = path.count('/')
    if lng == default:
        new_path = path[3:]
        return new_path
    else:
        if nr_slashes == 2:
            return '/' + lng + path
        else:
            new_path = path[3:]
            return  '/' + lng + new_path
