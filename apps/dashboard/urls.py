from django.conf.urls import url
from django.urls import path, include
from apps.dashboard.views import DashboardView
app_name = 'dashboard'
urlpatterns = [
    #dashboard urls
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    #apps urls

]