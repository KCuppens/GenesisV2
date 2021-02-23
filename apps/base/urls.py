from django.conf.urls import url
from .views import getURLPicker, permaURL
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^urlpicker$'),getURLPicker,name="getURLPicker"),
    url(_('^perma/url/(?P<module>[-\w]+)/(?P<pk>\d+)$'),permaURL,name="permaURL"),
]