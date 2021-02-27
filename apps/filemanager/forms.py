from django import forms
from apps.filemanager.models import Directory, Media
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
User = get_user_model()
from apps.feathericons.fields import IconField
from apps.filemanager.utils import guess_mime_type, guess_media_type

class DirectoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(required=False, queryset=Directory.objects.filter(date_deleted=None))
    class Meta:
        model = Directory
        fields = ('name', 'summary', 'parent')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(DirectoryForm, self).clean()
        errors = {}
        if self.cleaned_data.get('name') == '' or self.cleaned_data.get('name') == None:
            errors['name'] = _('Please enter a directory name.')
        
        if errors:
            raise forms.ValidationError(errors)

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('name', 'summary', 'copyright', 'keywords', 'alt', 'metadata')

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('file',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(MediaFileForm, self).clean()

        errors = {}
        
        if errors:
            raise forms.ValidationError(errors)
