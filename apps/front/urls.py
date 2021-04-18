from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.conf.urls import url
from apps.front.views import page_view, page_detail_view
from apps.search.views import search_front_view
from apps.news.views import get_articles, get_article_detail
from django.utils.translation import ugettext as _

urlpatterns = [
    #ajax blocks funcions
    url(_('get-articles').strip(), get_articles, name="get-articles"),
    url(_('get-article-detail').strip(), get_article_detail, name="get-article-detail"),

    url(_('^search$').strip(),search_front_view,name="search-front"),
    url('detail/(?P<model>[-\w]+)/(?P<pk>[0-9a-f-]+)/(?P<slug>[-\w]+)/$', page_detail_view, name="detail"),
    url(r'^$', page_view, name="index", kwargs={'slug': ''}),
    url(r'^(?P<slug>[-\w]+)/$', page_view, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)