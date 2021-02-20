from apps.pages.models import Page
from django import forms, template
register = template.Library()

@register.simple_tag
def children_page_count(page):
    return Page.objects.filter(parent=page, date_deleted=None).count()