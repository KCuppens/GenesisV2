from apps.formbuilder.models import FormPage, FormElement
from django import forms, template
from django.template.loader import render_to_string
register = template.Library()

@register.simple_tag
def get_element_template(request, object):
    if object:
        context = {
            'field': object,
            'colsizes': FormElement.GET_COL_SIZES
        }
        return render_to_string('formconfigs/' + str(object.type) + '.html', context=context, request=request)