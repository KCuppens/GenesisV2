from django.conf.urls import url
from .views import content_block_view, delete_ajax_page_modal, overview_page, add_page, edit_page, delete_page, page_reorder, overview_children_page, add_children_page, canvas_page, canvas_row
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$'),overview_page,name="overviewpage"),
    url(_('^overview/children/(?P<pk>\d+)$'),overview_children_page,name="overviewchildrenpage"),
    url(_('^add$'),add_page,name="addpage"),
    url(_('^add/children/(?P<pk>\d+)$'),add_children_page,name="addchildrenpage"),
    url(_('^edit/(?P<pk>\d+)$'),edit_page,name="editpage"),
    url(_('^delete/(?P<pk>\d+)$'),delete_page,name="deletepage"),
    url(_('^delete/modal$'),delete_ajax_page_modal,name="deletemodalpage"),
    url(_('verander-pagina-order'), page_reorder, name="page-reorder"),
    url(_('^page-builder/canvas-row'),canvas_row,name="canvasrow"),
    url(_('^page-builder/(?P<pk>\d+)$'),canvas_page,name="canvaspage"),
    url(_('^page-builder/canvas-content$'), content_block_view, name="canvascontent")
]