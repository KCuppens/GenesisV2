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
        fields = ('active','name', 'route', 'models', 'appname','urlpicker','is_superuser')
        labels = {
            'active': _('Active'), 
            'name': _('Name'),
            'route': _('Route'),
            'models': _('Model'),
            'app_name': _('Appname'),
            'urlpicker': _('URLPicker'),
            'is_superuser': _('Is superuser'), 
        }


class TabForm(forms.ModelForm):
    modules = forms.ModelMultipleChoiceField(queryset=Module.objects.filter(date_deleted=None), required=False)
    class Meta:
        model = Tab
        fields = ('active', 'name', 'icon','modules','is_superuser')
        labels = {
            'active': _('Actief'),
            'name': _('Name'),
            'icon': _('Icoon'),
            'modules': _('Modules'),
            'is_superuser': _('Is superuser'), 
        }