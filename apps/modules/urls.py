from django.conf.urls import url
from .views import delete_ajax_tab_modal, overview_tab, add_tab, edit_tab, delete_tab, reorder_tab, \
                    delete_ajax_modules_modal, overview_modules, add_modules, edit_modules, delete_modules, delete_modules_page, toggle_activation_view, toggle_tab_activation_view, reorder_module
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^tab/overview$').strip(),overview_tab,name="overviewtab"),
    url(_('^tab/add$').strip(),add_tab,name="addtab"),
    url(_('^tab/toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_tab_activation_view, name="activate-tabs"),
    url(_('^tab/edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_tab,name="edittab"),
    url(_('^tab/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_tab,name="deletetab"),
    url(_('^tab/reorder').strip(), reorder_tab, name="tab-reorder"),
    url(_('^tab/delete/modal$').strip(),delete_ajax_tab_modal,name="deletemodaltab"),

    url(_('^overview$').strip(),overview_modules,name="overviewmodules"),
    url(_('^add$').strip(),add_modules,name="addmodules"),
    url(_('^edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_modules,name="editmodules"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_activation_view, name="activate-modules"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_modules,name="deletemodules"),
    url(_('^delete/modulepages/(?P<pk>[0-9a-f-]+)$').strip(),delete_modules_page,name="deletepagemodules"),
    url(_('^reorder').strip(), reorder_module, name="module-reorder"),
    url(_('^delete/modal$').strip(),delete_ajax_modules_modal,name="deletemodalmodules"),
]