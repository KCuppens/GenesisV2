from django.conf.urls import url
from django.urls import path, include
from apps.conf.views import overview_conf, add_conf, edit_conf, delete_conf, delete_ajax_conf_modal, save_conf
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(_('^overview$'),overview_conf,name="overviewconf"),
    url(_('^add$'),add_conf,name="addconf"),
    url(_('^save$'),save_conf,name="saveconf"),
    url(_('^edit/(?P<pk>[0-9a-f-]+)$'),edit_conf,name="editconf"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$'),delete_conf,name="deleteconf"),
    url(_('^delete/modal$'),delete_ajax_conf_modal,name="deletemodalconf"),
]