from django.forms import ModelForm
from apps.conf.models import Configuration

class ConfigurationValueForm(ModelForm):
    class Meta:
        model = Configuration
        fields = ['value']

class ConfigurationForm(ModelForm):
    class Meta:
        model = Configuration
        fields = ['value','key_name', 'title', 'description', 'conf_type', 'type']