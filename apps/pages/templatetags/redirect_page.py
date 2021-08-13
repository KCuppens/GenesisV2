from apps.pages.models import Page
from django import forms, template
register = template.Library()
from django.template.loader import render_to_string
from django.db.models import Q
import datetime 
now = datetime.datetime.now()
from django.urls import reverse

@register.simple_tag
def redirect_page(id):
    if id:
        page = Page.objects.filter(id=id).first()
        return reverse('index', kwargs={'slug': page.full_slug})