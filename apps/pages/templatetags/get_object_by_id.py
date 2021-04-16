from apps.pages.models import Page
from django import forms, template
register = template.Library()
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from apps.news.models import Article

@register.simple_tag
def get_object_by_id(request, object_id, model):
    object = eval(model).objects.filter(id=object_id).first()
    if object:
        return str(object) + ' - ' + str(object.id)
    return _('Default object')