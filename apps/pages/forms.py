from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.pages.models import Page, Canvas, CanvasRow, CanvasCol, PageBlock
from apps.pages.utils import check_if_homepage_exists
class PageForm(forms.ModelForm):
    parent = forms.ModelChoiceField(required=False, queryset=Page.objects.filter(date_deleted=None))

    class Meta:
        model = Page
        fields = ('in_main_menu', 'is_homepage', 'page_title', 'menu_title','url_type','slug','parent','meta_title','meta_keywords','meta_description','date_published','date_expired','active')
        labels = {
            'in_main_menu': _('Is it the homepage?'),
            'in_main_menu': _('Show in main menu'),
            'page_title': _('Page title'),
            'menu_title': _('Menu title'),
            'url_type': _('Type of route/slug'),
            'slug': _('Route/slug'),
            'parent': _('Parent page'),
            'meta_title': _('Meta title'),
            'meta_keywords': _('Meta keywords'),
            'meta_description': _('Meta description'),
            'date_published': _('Publishing date'),
            'date_expired': _('Expiring date'),
            'active': _('Active')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(PageForm, self).clean()
        errors = {}
        if self.cleaned_data.get('is_homepage') and check_if_homepage_exists(self.instance):
            errors['is_homepage'] = _('You already have a homepage.')

        if errors:
            raise forms.ValidationError(errors)

class BlockForm(forms.ModelForm):
    class Meta:
        model = PageBlock
        fields = {'title', 'content', 'image', 'subtitle'}
        labels = {
            'title': _('Titel'),
            'content': _('Inhoud'),
            'image': _('Afbeelding'),
            'subtitle': _('Subtitel')
        }