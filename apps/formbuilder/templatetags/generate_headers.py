from apps.formbuilder.models import FormPage, FormElement
from django import forms, template
from django.template.loader import render_to_string
register = template.Library()

@register.simple_tag
def generate_headers(request, object, page):
    headers = []
    for result in object:
        for field in result.entries.all():
            if not field.field.label in headers:
                if int(field.page) == page.id and not field.field.type == 'submit_button':
                    if field.field.label == 'None':
                        headers.append("")
                    else:
                        headers.append(field.field.label)
    return headers