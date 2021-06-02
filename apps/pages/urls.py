from django.conf.urls import url
from .views import canvas_detailpage, get_detailpages, detailpages_overview, open_preview, toggle_activation_view, canvas_row_reorder, content_block_view, delete_ajax_page_modal, overview_page, add_page, edit_page, delete_page, page_reorder, overview_children_page, add_children_page, canvas_page, canvas_row, toggle_mainmenu_activation_view,\
                   get_version_ajax_modal, select_version, delete_version, \
                   add_version_comment, get_delete_version_ajax_modal,\
                   pageblockelement_reorder, overview_reversion, restore_page
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$').strip(),overview_page,name="overviewpage"),
    url(_('^overview/children/(?P<pk>[0-9a-f-]+)$').strip(),overview_children_page,name="overviewchildrenpage"),
    url(_('^add$').strip(),add_page,name="addpage"),
    url(_('^add/children/(?P<pk>[0-9a-f-]+)$').strip(),add_children_page,name="addchildrenpage"),
    url(_('^edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_page,name="editpage"),
    url(_('^toggle-mainmenu-activation/(?P<pk>[0-9a-f-]+)$').strip(),toggle_mainmenu_activation_view,name="toggle-mainmenu-activation-view"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(),toggle_activation_view,name="toggle-activation-view"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_page,name="deletepage"),
    url(_('^delete/modal$').strip(),delete_ajax_page_modal,name="deletemodalpage"),
    url(_('verander-pagina-order').strip(), page_reorder, name="page-reorder"),
    url(_('^detailpages/(?P<pk>[0-9a-f-]+)$').strip(), detailpages_overview, name="detailpages-overview"),
    url(_('^get_detailpages').strip(), get_detailpages, name="get-detailpages"),
    url(_('^page-builder/canvas-row').strip(),canvas_row,name="canvasrow"),
    url(_('^page-builder/(?P<pk>[0-9a-f-]+)$').strip(),canvas_page,name="canvaspage"),
    url(_('^detailpage-builder/(?P<pk>[0-9a-f-]+)$').strip(),canvas_detailpage,name="canvasdetailpage"),
    url(_('^page-builder/preview/(?P<canvas>[0-9a-f-]+)$').strip(),open_preview,name="open-preview"),
    url(_('^page-builder/canvas-content$').strip(), content_block_view, name="canvascontent"),
    url(_('^page-builder/verander-canvas-row-order').strip(), canvas_row_reorder, name="canvas-row-reorder"),
    url(_('^page-builder/pageblockelement_reorder').strip(), pageblockelement_reorder, name="pageblockelement_reorder"),
    url(_('^overview/reversion/$').strip(),overview_reversion,name="overviewreversionpage"),
    url(_('^restore/(?P<pk>[0-9a-f-]+)$').strip(),restore_page,name="restorepage"),

    url(_('^version/modal$').strip(),get_version_ajax_modal,name="pageversionmodal"),
    url(_('^version/deletemodal$').strip(),get_delete_version_ajax_modal,name="pagedeleteversionmodal"),
    url(_('^version/(?P<pk>[0-9a-f-]+)$').strip(),select_version,name="pageselectversion"),
    url(_('^version/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_version,name="pagedeleteversion"),
    url(_('^version/comment/(?P<pk>[0-9a-f-]+)$').strip(),add_version_comment,name="pageaddversioncomment"),
]