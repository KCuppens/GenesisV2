from django.conf.urls import url
from .views import getURLPicker, permaURL, get_filemanager
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^urlpicker$').strip(),getURLPicker,name="getURLPicker"),
    url(_('^filemanager$').strip(),get_filemanager,name="get_filemanager"),
    url(_('^perma/url/(?P<module>[-\w]+)/(?P<pk>[0-9a-f-]+)$').strip(),permaURL,name="permaURL"),
]