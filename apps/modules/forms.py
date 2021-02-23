from django import forms
from apps.modules.models import Module, Tab, ModulePage
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
User = get_user_model()
from apps.feathericons.fields import IconField

class ModulePageForm(forms.ModelForm):
    class Meta:
        model = ModulePage
        fields = ('name', 'route', 'show_nav')

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('active','name', 'route', 'models', 'appname','urlpicker')
        labels = {
            'active': _('Active'), 
            'name': _('Name'),
            'route': _('Route'),
            'models': _('Model'),
            'app_name': _('Appname'),
            'urlpicker': _('URLPicker')
        }


class TabForm(forms.ModelForm):
    modules = forms.ModelMultipleChoiceField(queryset=Module.objects.filter(date_deleted=None), required=False)
    class Meta:
        model = Tab
        fields = ('name', 'icon','modules')
        labels = {
            'name': _('Name'),
            'icon': _('Icoon'),
            'modules': _('Modules')
        }