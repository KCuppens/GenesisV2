from django.conf.urls import url
from .views import (
	delete_ajax_article_modal, 
	overview_article, add_article, 
	edit_article, delete_article, 
	delete_ajax_article_modal, 
	toggle_article_activation_view, 
	get_version_ajax_article_modal,
    get_delete_version_ajax_article_modal,
	select_version,
	delete_version,
	add_version_comment,
    overview_reversion,
    revert_article
)
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$').strip(),overview_article,name="overviewarticle"),
    url(_('^add$').strip(),add_article,name="addarticle"), 
    url(_('^edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_article,name="editarticle"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_article_activation_view, name="activate-article"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_article,name="deletearticle"),
    url(_('^delete/modal$').strip(),delete_ajax_article_modal,name="deletemodalarticle"),
    url(_('^overview/reversion/$').strip(),overview_reversion,name="overviewreversionarticle"),
    url(_('^revert/(?P<pk>[0-9a-f-]+)$').strip(),revert_article,name="revertarticle"),

    url(_('^version/modal$').strip(),get_version_ajax_article_modal,name="versionmodalarticle"),
    url(_('^version/modal/delete$').strip(),get_delete_version_ajax_article_modal,name="deleteversionmodalarticle"),
    url(_('^version/(?P<pk>[0-9a-f-]+)$').strip(),select_version,name="selectversion"),
    url(_('^version/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_version,name="deleteversion"),
    url(_('^version/comment/(?P<pk>[0-9a-f-]+)$').strip(),add_version_comment,name="addversioncomment"),
]