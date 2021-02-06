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

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(_('dashboard/overzicht/'), include('apps.dashboard.urls'), name='dashboard'),
    path(_('dashboard/configuratie/'), include('apps.conf.urls'), name='configuration'),
    path(_('dashboard/gebruiker/'), include('apps.user.urls'), name='user'),
    path(_('account/'), include('apps.user.account_urls'), name='user_dashboard'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
