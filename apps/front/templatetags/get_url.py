from apps.pages.models import Page
from django.urls import reverse
from django import forms, template
register = template.Library()

@register.simple_tag
def get_url(page):
    if page.url_type == Page.URL_TYPE_LINK_THROUGH:
        return page.linkthrough 
    else:
        return reverse('index', kwargs={'slug': page.full_slug})