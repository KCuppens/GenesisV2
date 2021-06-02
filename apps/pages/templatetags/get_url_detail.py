from apps.pages.models import Page
from django import forms, template
register = template.Library()
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from apps.pages.models import DetailPage
from apps.news.models import Article

@register.simple_tag
def get_url_detail(object_id, model):
    detailpage = DetailPage.objects.filter(model=model, object_id=object_id, default=False, overridden=True).first()
    object = eval(model).objects.filter(id=object_id).first()
    if not detailpage:
        detailpage = DetailPage.objects.filter(model=model, default=True).first()
    if not object or not detailpage:
        return '#' 
    return '/detail/' + model.lower() + '/' + str(detailpage.id) + '/' + object.slug 