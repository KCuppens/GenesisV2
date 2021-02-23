from django.conf.urls import url
from .views import media_document_index_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^media/document/index$'),media_document_index_view,name="media-document-index"),
]