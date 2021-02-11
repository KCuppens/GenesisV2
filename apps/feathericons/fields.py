from django.forms import ModelChoiceField
from apps.feathericons.models import Icon
from django.utils.html import mark_safe

class IconField(ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super(IconField, self).__init__(queryset=Icon.objects.all(),*args, **kwargs)

    
