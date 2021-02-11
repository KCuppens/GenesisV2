from apps.modules.models import ModulePage
from django import forms, template
register = template.Library()

@register.simple_tag
def get_active_module_pages(module):
    return ModulePage.objects.filter(module=module)

