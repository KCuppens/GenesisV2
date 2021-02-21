from django.conf.urls import url
from .views import toggle_activation_view, change_user_password, delete_ajax_group_modal, delete_ajax_user_modal, overview_user, add_user, edit_user, delete_user, my_profile, group_view, add_group_view, edit_group_view, delete_group_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$'),overview_user,name="overviewuser"),
    url(_('^add$'),add_user,name="adduser"),
    url(_('^edit/(?P<pk>\d+)$'),edit_user,name="edituser"),
    url(_('^change-password/(?P<pk>\d+)$'),change_user_password,name="changepassworduser"),
    url(_('^delete/(?P<pk>\d+)$'),delete_user,name="deleteuser"),
    url(_('^delete/modal$'),delete_ajax_user_modal,name="deletemodaluser"),
    url(_('^delete/toggle-activation/(?P<pk>\d+)$'), toggle_activation_view, name="activate-user"),
    url(_('^my-profile$'),my_profile,name="my-profile"),
    url(_('^group$'),group_view,name="overviewgroup"),
    url(_('^group/add$'),add_group_view,name="addgroup"),
    url(_('^group/edit/(?P<pk>\d+)$'),edit_group_view,name="editgroup"),
    url(_('^group/delete/(?P<pk>\d+)$'),delete_group_view,name="deletegroup"),
    url(_('^group/delete/modal$'),delete_ajax_group_modal,name="deletemodalgroup"),
]