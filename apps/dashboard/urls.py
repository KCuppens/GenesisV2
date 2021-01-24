from django.conf.urls import url
from django.urls import path, include
from .views import test
app_name = 'dashboard'
urlpatterns = [
    #priority
    url(r'^configuration/$', test, name='test'),
    #dashboard urls

    #apps urls

]