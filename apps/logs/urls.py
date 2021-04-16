from django.conf.urls import url
from .views import delete_ajax_log_modal, overview_logs, delete_log
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$'),overview_logs,name="overviewlogs"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$'),delete_log,name="deletelogs"),
    url(_('^delete/modal$'),delete_ajax_log_modal,name="deletemodallogs"),
]