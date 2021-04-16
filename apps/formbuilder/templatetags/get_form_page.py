from apps.formbuilder.models import FormPage
from django import forms, template
register = template.Library()

@register.simple_tag
def get_form_page(action, id):
    page = FormPage.objects.filter(id=id).first()
    if action == 'name':
        return page.name
    elif action == 'slug':
        return page.slug
    elif action == 'object':
        return page 