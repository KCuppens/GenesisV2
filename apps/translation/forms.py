from apps.base.widgets import MediaFileWidget
from django import forms
from django.utils.translation import ugettext_lazy as _

class ImportFileForm(forms.Form):
    file = forms.CharField(widget=MediaFileWidget)