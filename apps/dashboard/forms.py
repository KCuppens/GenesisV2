from django import forms
from apps.dashboard.models import DashboardConfiguration
from django.utils.translation import ugettext_lazy as _

class DashboardConfigurationForm(forms.ModelForm):
    class Meta:
        model = DashboardConfiguration
        fields = ('active','title', 'method', 'param1', 'sort','order', 'template', 'default', 'icon')
        labels = {
            'active': _('Active'), 
            'title': _('Title'),
            'method': _('Method'),
            'param1': _('Param 1'),
            'sort': _('Sorting method'),
            'order': _('Order method'),
            'template': _('Template'),
            'default': _('Default?'),
            'icon': _('Icoon')
        }