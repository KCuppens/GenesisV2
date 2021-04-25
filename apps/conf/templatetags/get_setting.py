from django import template
register = template.Library()
from apps.conf.models import Configuration

@register.simple_tag
def get_setting(request, keyname):
    setting = Configuration.objects.filter(key_name=keyname).first()
    if setting:
        return setting.value
    return '' 