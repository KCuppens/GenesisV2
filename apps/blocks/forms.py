from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.blocks.models import Block, BlockCategory
from apps.base.widgets import MediaImageWidget

class BlockForm(forms.ModelForm):
    image = forms.CharField(widget=MediaImageWidget)
    class Meta:
        model = Block
        fields = ('name', 'image', 'category', 'active', 'date_published', 'date_expired','col_size')
        labels = {
            'name': _('Name'),
            'image': _('Block image'),
            'category': _('Category'),
            'active': _('Active?'),
            'date_published': _('Publicatiedatum'),
            'date_expired': _('Vervaldatum'),
            'col_size': _('Kolom grootte')
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

