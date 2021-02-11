from django.conf.urls.static import static # new
from django.conf import settings # new
from django.conf.urls import url
from apps.translation.views import index_view, update_translation

urlpatterns = [
    url('update-translation', update_translation, name='update-translation'),
    url('index-translation', index_view, name="index-translation"),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
