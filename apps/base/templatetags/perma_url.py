from django import forms, template
from apps.base.utils import generate_perma_url
register = template.Library()


@register.simple_tag
def get_perma_url(locale, module, id):
    return generate_perma_url(locale, module, id)


