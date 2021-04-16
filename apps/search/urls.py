from django.conf.urls import url
from apps.search.views import search_admin_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^search$'),search_admin_view,name="search-admin"),
]