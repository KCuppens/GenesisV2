from django.forms import ModelForm
from apps.conf.models import Configuration

class ConfigurationForm(ModelForm):
    class Meta:
        model = Configuration
        fields = ['value']