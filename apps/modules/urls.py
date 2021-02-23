from django.conf.urls import url
from .views import delete_ajax_tab_modal, overview_tab, add_tab, edit_tab, delete_tab, \
                    delete_ajax_modules_modal, overview_modules, add_modules, edit_modules, delete_modules, delete_modules_page, toggle_activation_view, toggle_tab_activation_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^tab/overview$'),overview_tab,name="overviewtab"),
    url(_('^tab/add$'),add_tab,name="addtab"),
    url(_('^tab/toggle-activation/(?P<pk>\d+)$'), toggle_tab_activation_view, name="activate-tabs"),
    url(_('^tab/edit/(?P<pk>\d+)$'),edit_tab,name="edittab"),
    url(_('^tab/delete/(?P<pk>\d+)$'),delete_tab,name="deletetab"),
    url(_('^tab/delete/modal$'),delete_ajax_tab_modal,name="deletemodaltab"),

    url(_('^overview$'),overview_modules,name="overviewmodules"),
    url(_('^add$'),add_modules,name="addmodules"),
    url(_('^edit/(?P<pk>\d+)$'),edit_modules,name="editmodules"),
    url(_('^toggle-activation/(?P<pk>\d+)$'), toggle_activation_view, name="activate-modules"),
    url(_('^delete/(?P<pk>\d+)$'),delete_modules,name="deletemodules"),
    url(_('^delete/modulepages/(?P<pk>\d+)$'),delete_modules_page,name="deletepagemodules"),
    url(_('^delete/modal$'),delete_ajax_modules_modal,name="deletemodalmodules"),
]