from apps.pages.models import Page
from apps.news.models import Article
from django import forms, template
register = template.Library()
from django.utils.translation import ugettext_lazy as _
import json
@register.simple_tag
def display_gallery(object):
    gallery = []
    if object.gallery:
        for value in json.loads(object.gallery):
            gallery.append(value['value'])
    return gallery