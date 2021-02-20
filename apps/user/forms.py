from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from apps.conf.utils import get_config
from .fields import HoneyPotField, PasswordField, UsersEmailField
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
User = get_user_model()

class UserForm(forms.ModelForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Enter Your First Name'),"class":"form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Enter Your Last Name'),"class":"form-control"}))
    username = forms.CharField(label="Username", required=True, widget=forms.TextInput(attrs={'placeholder': _('Username'),"class":"form-control"}))

    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': _('Email')}))

    is_active = forms.BooleanField(initial=True,widget=forms.CheckboxInput(attrs={"class":"new-control-input","id":"is_active"}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(date_deleted=None),widget=forms.SelectMultiple(attrs={"class":"selectpicker", "data-actions-box":"true"}))

    is_staff = forms.BooleanField(initial=True, required=False,widget=forms.CheckboxInput(attrs={"class":"new-control-input","id":"is_staff"}))    
      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].required = False

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserForm, self).clean()
        validate = True
        if self.cleaned_data.get('username') or self.cleaned_data.get('email'):
            user_username_exists = User.objects.filter(username=self.cleaned_data.get('username'), date_deleted__isnull=False).first()
            user_email_exists = User.objects.filter(email=self.cleaned_data.get('email'), date_deleted__isnull=False).first()

            if user_email_exists or user_username_exists:
                if user_email_exists:
                    user_email_exists.date_deleted = None
                    user_email_exists.save()
                    validate = False
                elif user_username_exists:
                    user_username_exists.data_deleted = None
                    user_username_exists.save()
                    validate = False
        if(validate):
            errors = {}
            if cleaned_data.get('email') == '' or cleaned_data.get('email') == None:
                errors['email'] = _('Please enter a emailaddress.')
            if cleaned_data.get('username') == "" or cleaned_data.get('username') == None:
                errors['username'] = _('Please enter a username.')
            if cleaned_data.get('firstname') == "" or cleaned_data.get('first_name') == None:
                errors['first_name'] = _('Please enter a firstname.')
            if cleaned_data.get('lastname') == "" or cleaned_data.get('last_name') == None:
                errors['last_name'] = _('Please enter a lastname.')
            if errors:
                raise forms.ValidationError(errors)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email',
        'groups','is_active','is_staff')
        labels = {
            'username': _('Username'),
            'first_name': _('Firstname'),
            'last_name': _('Lastname'),
            'email': _('Email'),
            'groups': _('Groups'),
            'is_active': _('Is active'),
            'is_staff': _('Is staff')
        }

class UserChangePasswordForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '******'})
    )

    class Meta:
        model = User
        fields = ['password']

    
        
class GroupForm(forms.ModelForm):
    #So only name is shown
    def permission_string(self):
        return self.name
    Permission.__str__ = permission_string
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':_('Enter Group Name'),'class':'form-control'}))
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(), 
        required=False,
        widget=forms.CheckboxSelectMultiple() 
    )

    class Meta:
        model = Group
        fields = ('name', 'permissions')
        labels = {
            'name': _('Name'),
            'permissions': _('Permissions'),
        }
