from django.conf.urls import url
from .views import delete_ajax_tab_modal, overview_tab, add_tab, edit_tab, delete_tab, reorder_tab, \
                    delete_ajax_modules_modal, overview_modules, add_modules, edit_modules, delete_modules, delete_modules_page, toggle_activation_view, toggle_tab_activation_view, reorder_module, \
                    get_version_ajax_modal, select_version, \
                    delete_version, add_version_comment, get_delete_version_ajax_modal, \
                    overview_reversion, revert_module_item
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

    url(_('^overview/reversion/(?P<mode>[a-z]+)/$').strip(),overview_reversion,name="overviewreversionmodule"),
    url(_('^revert/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)/$').strip(),revert_module_item,name="revertmodule"),

    url(_('^version/modal/(?P<mode>[a-z]+)/$').strip(),get_version_ajax_modal,name="moduleversionmodal"),
    url(_('^version/modal/delete/(?P<mode>[a-z]+)/$').strip(),get_delete_version_ajax_modal,name="moduledeleteversionmodal"),
    url(_('^version/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)$').strip(),select_version,name="moduleselectversion"),
    url(_('^version/delete/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)$').strip(),delete_version,name="moduledeleteversion"),
    url(_('^version/comment/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)$').strip(),add_version_comment,name="moduleaddversioncomment"),
]