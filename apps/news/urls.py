from django.conf.urls import url
from .views import delete_ajax_article_modal, overview_article, add_article, edit_article, delete_article, delete_ajax_article_modal, toggle_article_activation_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$').strip(),overview_article,name="overviewarticle"),
    url(_('^add$').strip(),add_article,name="addarticle"), 
    url(_('^edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_article,name="editarticle"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_article_activation_view, name="activate-article"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_article,name="deletearticle"),
    url(_('^delete/modal$').strip(),delete_ajax_article_modal,name="deletemodalarticle"),
]