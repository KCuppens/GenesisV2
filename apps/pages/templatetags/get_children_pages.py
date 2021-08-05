from apps.pages.models import Page
from django import forms, template
register = template.Library()
from django.db.models import Q
import datetime 
now = datetime.datetime.now()

@register.simple_tag
def get_children_pages(page):
    return page.children.filter(Q(date_expired__gte=now) | Q(date_expired__isnull=True), active=True, date_deleted=None, date_published__lte=now, in_main_menu=True) 