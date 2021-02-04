from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from apps.conf.utils import get_config
from .fields import HoneyPotField, PasswordField, UsersEmailField
from django.contrib.auth.models import Group, Permission

from .models import User
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreationForm(forms.ModelForm):

    error_messages = {
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    email = UsersEmailField(label=_('Email Address'), max_length=255)
    password1 = PasswordField(label=_('Password'))
    password2 = PasswordField(
        label=_('Password Confirmation'),
        help_text=_('Enter the same password as above, for verification.'))

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_email(self):

        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = not get_config('USERS_VERIFY_EMAIL')
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(label=_('Password'), help_text=_(
        'Raw passwords are not stored, so there is no way to see '
        'this user\'s password, but you can change the password '
        'using <a href=\"password/\">this form</a>.'))

    class Meta:
        model = get_user_model()
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial['password']


class RegistrationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    """
    tos = forms.BooleanField(
        label=_('I have read and agree to the Terms of Service'),
        widget=forms.CheckboxInput,
        error_messages={
            'required': _('You must agree to the terms to register')
        })


class RegistrationFormHoneypot(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a honeypot field
    for Spam Prevention
    """
    accept_terms = HoneyPotField()










class UserEditForm(forms.ModelForm):
    
    profession = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':_('Enter Your First Name'),"class":"form-control"}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':_('Enter Your Last Name'),"class":"form-control"}))
    username = forms.CharField(label="Username",widget=forms.TextInput(attrs={'placeholder': 'Username',"class":"form-control"}))

class UserEditForm(forms.ModelForm):
    
    profession = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Enter Your First Name'),"class":"form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Enter Your Last Name'),"class":"form-control"}))
    username = forms.CharField(label="Username",widget=forms.TextInput(attrs={'placeholder': _('Username'),"class":"form-control"}))

    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={"class":"form-control"}))

    is_active = forms.BooleanField(initial=True,widget=forms.CheckboxInput(attrs={"class":"custom-control-input","id":"is_active"}))
    front_client = forms.BooleanField(initial=True,widget=forms.CheckboxInput(attrs={"class":"custom-control-input","id":"front_client"}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(date_deleted=None),widget=forms.CheckboxSelectMultiple())

    is_staff = forms.BooleanField(initial=True, required=False,widget=forms.CheckboxInput(attrs={"class":"custom-control-input","id":"is_staff"}))

    is_staff = forms.BooleanField(initial=True, required=False,widget=forms.CheckboxInput())
    user_type=forms.ChoiceField(choices=User.USER_TYPES,widget=forms.Select(attrs={"class":"form-control form-control-lg"}))
    company_vat=forms.ChoiceField(choices=["NL","BE"],widget=forms.Select(attrs={"class":"form-control form-control-lg"}))
    birthdate=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    phone=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].required = False


    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email','phone','birthdate','profession',
        'groups','is_active','is_staff','user_type','company_name','company_vat','front_client')

    
        
class GroupForm(forms.ModelForm):
    name = forms.CharField(required=True,widget=forms.TextInput(
                                   attrs={'placeholder':_('Enter Group Name'),'class':'form-control'}))
                                   attrs={'placeholder': _('Enter Group Name'),'class':'form-control'}))
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple() 
    )

    class Meta:
        model = Group
        fields = ('name', 'permissions')
