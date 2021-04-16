from django.conf.urls import url
from .views import canvas_detailpage, get_detailpages, detailpages_overview, open_preview, toggle_activation_view, canvas_row_reorder, content_block_view, delete_ajax_page_modal, overview_page, add_page, edit_page, delete_page, page_reorder, overview_children_page, add_children_page, canvas_page, canvas_row, toggle_mainmenu_activation_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$'),overview_page,name="overviewpage"),
    url(_('^overview/children/(?P<pk>[0-9a-f-]+)$'),overview_children_page,name="overviewchildrenpage"),
    url(_('^add$'),add_page,name="addpage"),
    url(_('^add/children/(?P<pk>[0-9a-f-]+)$'),add_children_page,name="addchildrenpage"),
    url(_('^edit/(?P<pk>[0-9a-f-]+)$'),edit_page,name="editpage"),
    url(_('^toggle-mainmenu-activation/(?P<pk>[0-9a-f-]+)$'),toggle_mainmenu_activation_view,name="toggle-mainmenu-activation-view"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$'),toggle_activation_view,name="toggle-activation-view"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$'),delete_page,name="deletepage"),
    url(_('^delete/modal$'),delete_ajax_page_modal,name="deletemodalpage"),
    url(_('verander-pagina-order'), page_reorder, name="page-reorder"),
    url(_('^detailpages/(?P<pk>[0-9a-f-]+)$'), detailpages_overview, name="detailpages-overview"),
    url(_('^get_detailpages'), get_detailpages, name="get-detailpages"),
    url(_('^page-builder/canvas-row'),canvas_row,name="canvasrow"),
    url(_('^page-builder/(?P<pk>[0-9a-f-]+)$'),canvas_page,name="canvaspage"),
    url(_('^detailpage-builder/(?P<pk>[0-9a-f-]+)$'),canvas_detailpage,name="canvasdetailpage"),
    url(_('^page-builder/preview/(?P<canvas>[0-9a-f-]+)$'),open_preview,name="open-preview"),
    url(_('^page-builder/canvas-content$'), content_block_view, name="canvascontent"),
    url(_('^page-builder/verander-canvas-row-order'), canvas_row_reorder, name="canvas-row-reorder"),

]