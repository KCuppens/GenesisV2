from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.blocks.models import Block, BlockCategory
from apps.base.widgets import MediaImageWidget

class BlockForm(forms.ModelForm):
    image = forms.CharField(widget=MediaImageWidget)
    class Meta:
        model = Block
        fields = ('name', 'template', 'image', 'category', 'active', 'date_published', 'date_expired','col_size', 'has_title', 'has_subtitle', 'has_form', 'has_content', 'detailpage_only', 'has_module', 'has_image', 'has_image_second', 'has_url', 'has_url_text', 'has_video', 'has_embed', 'has_sort_method', 'has_limit', 'has_sort_order', 'has_pagination', 'has_detailpage')
        labels = {
            'name': _('Name'),
            'image': _('Block image'),
            'category': _('Category'),
            'active': _('Active?'),
            'date_published': _('Publicatiedatum'),
            'date_expired': _('Vervaldatum'),
            'col_size': _('Kolom grootte'),
            'has_title': _('Bevat een titel'),
            'has_subtitle': _('Bevat een subtitel'),
            'has_content': _('Bevat een inhoud'), 
            'has_image': _('Bevat een afbeelding'),
            'has_image_second': _('Bevat een tweede afbeelding'),
            'has_url': _('Bevat een url'),
            'has_url_text': _('Bevat een tekst url'),
            'has_video': _('Bevat een video'),
            'has_embed': _('Bevat een embed'),
            'has_sort_method': _('Bevat een sorteer methode'),
            'has_limit': _('Bevat een limiet'),
            'has_sort_order': _('Bevat een sorteer volgorde'),
            'has_pagination': _('Bevat een paginatie'),
            'has_module': _('Bevat een module'),
            'has_detailpage': _('Bevat een detailpagina'),
            'has_form': _('Bevat een formulier'),
            'template': _('Template name'),
            'detailpage_only': _('Alleen detailpagina block?')
        }

class BlockCategoryForm(forms.ModelForm):
    class Meta:
        model = BlockCategory
        fields = ('name', 'active', 'date_published', 'date_expired')
        labels = {
            'name': _('Name'),
            'date_published': _('Publishing date'),
            'date_expired': _('Expiring date'),
            'active': _('Active')
        }

