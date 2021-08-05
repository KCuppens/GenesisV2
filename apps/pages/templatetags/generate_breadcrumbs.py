from apps.pages.models import Page
from django import forms, template
register = template.Library()
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _


@register.simple_tag
def generate_breadcrumbs(request, page):
    crumbs = []
    crumbs.append(page)
    homepage = Page.objects.filter(is_homepage=True, active=True, date_deleted=None).first()
    if page.parent:
        parent = page.parent
    else:
        parent = None
    while parent:
        crumbs.append(page.parent)
        parent = parent.parent
    crumbs.append(homepage)
    crumbs.reverse()
    return crumbs