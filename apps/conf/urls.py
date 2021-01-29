from django.conf.urls import url
from django.urls import path, include
from apps.conf.views import ConfigurationListView, ConfigurationEditView
from django.utils.translation import ugettext_lazy as _

app_name = 'config'
urlpatterns = [
    url(_('^overzicht$'), ConfigurationListView.as_view(), name='configuration'),
    url(_('^aanpassen$'), ConfigurationEditView.as_view(), name='configuration-edit'),
]