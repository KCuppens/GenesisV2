from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.pages.models import Page, Canvas, CanvasRow, PageBlock, PageBlockElement
from apps.formbuilder.models import Form
from apps.pages.utils import check_if_homepage_exists
from apps.base.widgets import MediaImageWidget
from apps.pages.widgets import PageMediaImageWidget, PageMediaVideoWidget

DATE_INPUT_FORMATS = ('%Y-%m-%d %H-%i',)

class PageForm(forms.ModelForm):
    parent = forms.ModelChoiceField(required=False, queryset=Page.objects.filter(date_deleted=None))
    image = forms.CharField(label=_('Afbeelding'), widget=MediaImageWidget, required=False)
    # date_expired = forms.DateTimeField(input_formats=DATE_INPUT_FORMATS)
    class Meta:
        model = Page
        fields = ('in_main_menu', 'image', 'is_homepage', 'page_title', 'menu_title','url_type','slug','linkthrough','parent','meta_title','meta_keywords','meta_description','date_published','date_expired','active', 'is_deletable')
        labels = {
            'is_homepage': _('Is it the homepage?'),
            'in_main_menu': _('Show in main menu'),
            'page_title': _('Page title*'),
            'menu_title': _('Menu title*'),
            'url_type': _('Type of route/slug*'),
            'slug': _('Route/slug*'),
            'linkthrough': _('Doorlink*'),
            'parent': _('Parent page'),
            'meta_title': _('Meta title'),
            'meta_keywords': _('Meta keywords'),
            'meta_description': _('Meta description'),
            'date_published': _('Publishing date'),
            'date_expired': _('Expiring date'),
            'active': _('Active'),
            'is_deletable': _('Is it deletable?'),
        }
        help_texts = {
            'page_title': _('This title will be shown on the website and in the metadata.'),
            'menu_title': _('This title will only be shown on links in the chosen menu.'),
            'meta_title': _('This title will only overwrite page title in the meta data for SEO purposes.'),
            'meta_keywords': _('These keywords will be written in the meta data of the browser for SEO purposes.'),
            'meta_description': _('This description will be written in the meta data of the browser for SEO purposes.'),
        }
        widgets = {
            'is_deletable': forms.CheckboxInput()
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super(PageForm, self).clean()
        errors = {}
        if self.cleaned_data.get('is_homepage') and check_if_homepage_exists(self.instance):
            errors['is_homepage'] = _('You already have a homepage.')
        if self.cleaned_data.get('menu_title') == '' or self.cleaned_data.get('menu_title') == None:
            errors['menu_title'] = _('Please enter a menu title')
        if self.cleaned_data.get('page_title') == '' or self.cleaned_data.get('page_title') == None:
            errors['page_title'] = _('Please enter a page title')
        if errors:
            raise forms.ValidationError(errors)

        return self.cleaned_data

class BlockForm(forms.ModelForm):
    # image = forms.CharField(required=False, widget=MediaImageWidget)
    # image_second = forms.CharField(required=False, widget=MediaImageWidget)
    image = forms.CharField(required=False, widget=PageMediaImageWidget)
    image_second = forms.CharField(required=False, widget=PageMediaImageWidget)
    video = forms.CharField(required=False, widget=PageMediaVideoWidget)
    form = forms.ModelChoiceField(required=False, queryset=Form.objects.filter(date_deleted=None, active=True))
    class Meta:
        model = PageBlock
        fields = {'title', 'content', 'form', 'image', 'subtitle', 'image_second', 'url', 'url_text', 'video', 'embed', 'sort', 'limit', 'sort_order', 'paginated', 'detailpage'}
        labels = {
            'title': _('Titel'),
            'content': _('Inhoud'),
            'image': _('Afbeelding'),
            'subtitle': _('Subtitel'),
            'image_second': _('Tweede afbeelding'),
            'url': _('URL'),
            'url_text': _('Tekst voor url'),
            'video': _('Video'),
            'embed': _('Embed'),
            'sort': _('Sorteer methode'),
            'limit': _('Limiet'),
            'sort_order': _('Sorteer volgorde'),
            'paginated': _('Paginatie'),
            'detailpage': _('Detailpagina'),
            'form': _('Formulier')
        }
    
class BlockElementForm(forms.ModelForm):
    block_element_image = forms.CharField(label=_('Blok afbeelding'), required=False, widget=MediaImageWidget)
    block_element_image_second = forms.CharField(label=_('Blok tweede afbeelding'), required=False, widget=MediaImageWidget)
    class Meta:
        model = PageBlockElement
        fields = {'block_element_title', 'block_element_image', 'block_element_content', 'block_element_subtitle', 'block_element_image_second'}
        labels = {
            'block_element_title': _('Blok titel'),
            'block_element_image': _('Blok afbeelding'),
            'block_element_content': _('Blok inhoud'),
            'block_element_subtitle': _('Blok subtitel'),
            'block_element_image_second': _('Blok tweede afbeelding'),
        }