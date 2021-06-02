from django.conf.urls import url
from .views import export_users, toggle_activation_view, change_user_password, delete_ajax_group_modal, delete_ajax_user_modal, overview_user, add_user, edit_user, delete_user, my_profile, group_view, add_group_view, edit_group_view, delete_group_view, \
                   overview_reversion, revert_user
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$').strip(),overview_user,name="overviewuser"),
    url(_('^add$').strip(),add_user,name="adduser"),
    url(_('^edit/(?P<pk>\d+)$').strip(),edit_user,name="edituser"),
    url(_('^change-password/(?P<pk>\d+)$').strip(),change_user_password,name="changepassworduser"),
    url(_('^delete/(?P<pk>\d+)$').strip(),delete_user,name="deleteuser"),
    url(_('^delete/modal$').strip(),delete_ajax_user_modal,name="deletemodaluser"),
    url(_('^delete/toggle-activation/(?P<pk>\d+)$').strip(), toggle_activation_view, name="activate-user"),
    #url(_('^my-profile$'),my_profile,name="my-profile"),
    url(_('^group$').strip(),group_view,name="overviewgroup"),
    url(_('^group/add$').strip(),add_group_view,name="addgroup"),
    url(_('^group/edit/(?P<pk>\d+)$').strip(),edit_group_view,name="editgroup"),
    url(_('^group/delete/(?P<pk>\d+)$').strip(),delete_group_view,name="deletegroup"),
    url(_('^group/delete/modal$').strip(),delete_ajax_group_modal,name="deletemodalgroup"),

    url(_('^overview/reversion/$').strip(),overview_reversion,name="overviewreversionuser"),
    url(_('^revert/(?P<pk>[0-9a-f-]+)$').strip(),revert_user,name="revertuser"),
]