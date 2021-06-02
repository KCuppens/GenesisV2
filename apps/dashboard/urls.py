from django.conf.urls import url
from django.urls import path, include
from django.utils.translation import ugettext as _
from apps.dashboard.views import reorder_dashboard, dashboard_view, overview_dashboard, add_dashboard, edit_dashboard, toggle_dashboard_activation_view, delete_dashboard, delete_ajax_dashboard_modal, \
                                 overview_reversion, revert_dashboard
urlpatterns = [
    #dashboard urls
    url(r'^$', dashboard_view, name='dashboard'),
    #apps urls
    url(_('^overview$').strip(),overview_dashboard,name="overviewdashboard"),
    url(_('^add$').strip(),add_dashboard,name="adddashboard"),
    url(_('^edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_dashboard,name="editdashboard"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_dashboard_activation_view, name="activate-dashboard"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_dashboard,name="deletedashboard"),
    url(_('^delete/modal$').strip(),delete_ajax_dashboard_modal,name="deletemodaldashboard"),
    url(_('^dashboard/reorder').strip(), reorder_dashboard, name="dashboard-reorder"),

    url(_('^overview/reversion/$').strip(),overview_reversion,name="overviewreversiondashboard"),
    url(_('^revert/(?P<pk>[0-9a-f-]+)$').strip(),revert_dashboard,name="revertdashboard"),
]