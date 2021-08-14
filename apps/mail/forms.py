from django import forms
from apps.mail.models import MailTemplate
from django.utils.translation import ugettext_lazy as _

class MailTemplateForm(forms.ModelForm):
    class Meta:
        model = MailTemplate
        fields = ('active','key_name', 'title', 'subject', 'image','content_html', 'attachments')
        labels = {
            'active': _('Active'), 
            'key_name': _('Keyname'),
            'title': _('Title'),
            'subject': _('Subject'),
            'image': _('Image'),
            'content_html': _('Content HTML'),
            'attachments': _('Attachment'),
        }
    
    def clean(self, *args, **kwargs):
        cleaned_data = super(MailTemplateForm, self).clean()

        errors = {}
        mailtemplate = MailTemplate.objects.filter(key_name=self.cleaned_data.get('key_name')).first()
        mailtemplate_exists = False
        if mailtemplate and mailtemplate.id == self.instance.id:
            mailtemplate_exists = True
        if self.cleaned_data.get('key_name') == '' or self.cleaned_data.get('key_name') == None or mailtemplate_exists:
            errors['key_name'] = _('Please enter a unique keyname')
        if self.cleaned_data.get('title') == '' or self.cleaned_data.get('title') == None:
            errors['title'] = _('Please enter a title')
        if errors:
            raise forms.ValidationError(errors)

        return self.cleaned_data
