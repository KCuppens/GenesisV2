from django.forms import ModelForm
from apps.news.models import Article
from django.utils.translation import gettext_lazy as _
from django import forms 
from apps.base.widgets import MediaImageWidget

class ArticleForm(ModelForm):
    image = forms.CharField(label=_('Afbeelding'), widget=MediaImageWidget)
    class Meta:
        model = Article 
        fields = ['title', 'image', 'content', 'summary', 'meta_title', 'meta_description', 'meta_keywords', 'date_expired', 'date_published','active']
        labels = {
            'title': _('Titel*'),
            'content': _('Inhoud'),
            'summary': _('Samenvatting'),
            'meta_title': _('SEO Titel'),
            'meta_description': _('SEO Beschrijving'),
            'meta_keywords': _('SEO keywoorden'),
            'date_expired': _('Vervaldatum'),
            'date_published': _('Publicatiedatum'),
            'active': _('Actief?')
        }
        help_texts = {
            'meta_title': _('This title will only overwrite page title in the meta data for SEO purposes.'),
            'meta_keywords': _('These keywords will be written in the meta data of the browser for SEO purposes.'),
            'meta_description': _('This description will be written in the meta data of the browser for SEO purposes.'),
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super(ArticleForm, self).clean()
        errors = {}
        if cleaned_data.get('title') == '' or cleaned_data.get('title') == None:
            errors['title'] = _('Er moet altijd een titel zijn.')
        if errors:
            raise forms.ValidationError(errors)

        return self.cleaned_data