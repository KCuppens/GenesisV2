from django import forms, template
register = template.Library()

@register.simple_tag
def module_title_without_key(modules, item):
    class_name = item.__class__.__name__
    module = modules[class_name]
    return module['title']
    