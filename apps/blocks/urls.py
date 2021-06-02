from django.conf.urls import url
from .views import delete_ajax_block_modal, overview_block, add_block, edit_block, delete_block, \
                    delete_ajax_block_category_modal, overview_blockcategories, add_block_category, edit_block_category, delete_blockcategory, toggle_activation_view, toggle_category_activation_view, \
                    get_version_ajax_modal, select_version, delete_version, \
                    add_version_comment, get_delete_version_ajax_modal, \
                    overview_reversion, revert_block
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$').strip(),overview_block,name="overviewblocks"),
    url(_('^add$').strip(),add_block,name="addblock"),
    url(_('^edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_block,name="editblock"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_activation_view, name="activate-blocks"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_block,name="deleteblock"),
    url(_('^delete/modal$').strip(),delete_ajax_block_modal,name="deletemodalblock"),

    url(_('^category/overview$').strip(),overview_blockcategories,name="overviewblock-categories"),
    url(_('^category/add$').strip(),add_block_category,name="addblock-category"),
    url(_('^category/edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_block_category,name="editblock-category"),
    url(_('^category/toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_category_activation_view, name="activate-blockcategories"),
    url(_('^category/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_blockcategory,name="deleteblock-category"),
    url(_('^category/delete/modal$').strip(),delete_ajax_block_category_modal,name="deletemodalblock-category"),

    url(_('^overview/reversion/$').strip(),overview_reversion,name="overviewreversionblock"),
    url(_('^revert/(?P<pk>[0-9a-f-]+)$').strip(),revert_block,name="revertblock"),

    url(_('^version/modal$').strip(),get_version_ajax_modal,name="blockversionmodal"),
    url(_('^version/deletemodal$').strip(),get_delete_version_ajax_modal,name="blockdeleteversionmodal"),
    url(_('^version/(?P<pk>[0-9a-f-]+)$').strip(),select_version,name="blockselectversion"),
    url(_('^version/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_version,name="blockdeleteversion"),
    url(_('^version/comment/(?P<pk>[0-9a-f-]+)$').strip(),add_version_comment,name="blockaddversioncomment"),
]