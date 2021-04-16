from apps.formbuilder.models import FormResult
from django import forms, template
from django.template.loader import render_to_string
register = template.Library()

@register.simple_tag
def get_form_entry_count(object):
    if object:
        results = FormResult.objects.filter(form=object.id, date_deleted=None)
        count = 0
        for result in results:
            if result.entries.exists():
                count = count + 1
        return count