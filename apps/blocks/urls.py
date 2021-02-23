from django.conf.urls import url
from .views import delete_ajax_block_modal, overview_block, add_block, edit_block, delete_block, \
                    delete_ajax_block_category_modal, overview_blockcategories, add_block_category, edit_block_category, delete_blockcategory, toggle_activation_view, toggle_category_activation_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$'),overview_block,name="overviewblocks"),
    url(_('^add$'),add_block,name="addblock"),
    url(_('^edit/(?P<pk>\d+)$'),edit_block,name="editblock"),
    url(_('^toggle-activation/(?P<pk>\d+)$'), toggle_activation_view, name="activate-blocks"),
    url(_('^delete/(?P<pk>\d+)$'),delete_block,name="deleteblock"),
    url(_('^delete/modal$'),delete_ajax_block_modal,name="deletemodalblock"),

    url(_('^category/overview$'),overview_blockcategories,name="overviewblock-categories"),
    url(_('^category/add$'),add_block_category,name="addblock-category"),
    url(_('^category/edit/(?P<pk>\d+)$'),edit_block_category,name="editblock-category"),
    url(_('^category/toggle-activation/(?P<pk>\d+)$'), toggle_category_activation_view, name="activate-blockcategories"),
    url(_('^category/delete/(?P<pk>\d+)$'),delete_blockcategory,name="deleteblock-category"),
    url(_('^category/delete/modal$'),delete_ajax_block_category_modal,name="deletemodalblock-category"),
]