from django import forms, template
register = template.Library()

@register.simple_tag
def type_var(key, count, modules, type):
    active = False
    if not key == 'all':
        if modules[key]['type']:
            active = True 
    else:
        if type == 'all':
            active = True 
    return active
    