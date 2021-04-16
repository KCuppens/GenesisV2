from django import forms, template
register = template.Library()

@register.simple_tag
def module_title(modules, key):
    return modules[key]['title']
    