"""GenesisV2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.sitemaps.views import sitemap
from apps.front.sitemap import PageSitemap
sitemaps = {
    'page': PageSitemap,
}
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(_('dashboard/'), include('apps.dashboard.urls'), name='dashboard'),
    path(_('dashboard/configuratie/'), include('apps.conf.urls'), name='configuration'),
    path(_('dashboard/gebruiker/'), include('apps.user.urls'), name='user'),
    path(_('dashboard/modules/'), include('apps.modules.urls'), name='modules'),
    path(_('dashboard/translations/'), include('apps.translation.urls'), name='translation'),
    path(_('dashboard/pages/'), include('apps.pages.urls'), name='pages'),
    path(_('dashboard/blocks/'), include('apps.blocks.urls'), name='blocks'),
    path(_('dashboard/history/'), include('apps.history.urls'), name='history'),
    path(_('dashboard/news/'), include('apps.news.urls'), name='news'),
    path(_('dashboard/base/'), include('apps.base.urls'), name='base'),
    path(_('dashboard/media/'), include('apps.filemanager.urls'), name='filemanager'),
    path(_('dashboard/mail/'), include('apps.mail.urls'), name='mail'),
    path(_('dashboard/formbuilder/'), include('apps.formbuilder.urls'), name='form'),
    path(_('dashboard/logs/'), include('apps.logs.urls'), name='logs'),
    path(_('dashboard/data/'), include('apps.data.urls'), name='data'),
    path(_('dashboard/search/'), include('apps.search.urls'), name='search'),
    path(_('account/'), include('apps.user.account_urls'), name='user_dashboard'),

    path('', include('apps.front.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
