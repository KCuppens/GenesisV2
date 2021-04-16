from django import forms, template
register = template.Library()

@register.simple_tag
def module_type(modules, key):
    if not key == 'all':
        return modules[key]['type']
    return 'all'
    