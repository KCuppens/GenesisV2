from django import forms
from apps.formbuilder.models import Form, FormPage
from django.utils.translation import ugettext_lazy as _

class FormbuilderForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ('active','name', 'success_type', 'success_action', 'success_url','success_message', 'send_mail', 'mail_recipient_name', 'mail_recipient_email', 'mail_admin', 'mail_sender_name', 'mail_sender_email', 'mail_sender_visitor', 'mail_visitor', 'mail_visitor_sender_name', 'mail_visitor_sender_email', 'store_results')
        labels = {
            'active': _('Active'), 
            'name': _('Name'),
            'success_type': _('Success type'),
            'success_action': _('Success action'),
            'success_url': _('Success URL'),
            'success_message': _('Success message'),
            'send_mail': _('Send admin email'),
            'mail_recipient_name': _('Ontvanger naam'),
            'mail_recipient_email': _('Ontvanger email'),
            'mail_admin': _('Admin email'),
            'mail_sender_name': _('Sender name'),
            'mail_sender_email': _('Sender email'),
            'mail_sender_visitor': _('Send visitor email'),
            'mail_visitor': _('Visitor email'),
            'mail_visitor_sender_name': _('Sender name'),
            'mail_visitor_sender_email': _('Sender email'),
            'store_results': _('Store results'),
        }

class FormPageForm(forms.ModelForm):
    class Meta:
        model = FormPage
        fields = {'name',}
        labels = {
            'name': _('Name')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(FormPageForm, self).clean()
        errors = {}
        if self.cleaned_data.get('name') == '' or self.cleaned_data.get('name') == None:
            errors['name'] = _('You have to enter a name.')

        if self.cleaned_data.get('success_action') == '' and self.cleaned_data.get('success_url') == '' and self.cleaned_data.get('success_message') == '':
            errors['success_action'] = _('Please atleast use one success type.')
            errors['success_url'] = _('Please atleast use one success type.')
            errors['success_message'] = _('Please atleast use one success type.')

        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data
