from django.conf.urls.static import static # new
from django.conf import settings # new
from django.conf.urls import url
from apps.translation.views import index_view, update_translation, import_translation, export_translation, import_file_translation

urlpatterns = [
    url('update-translation', update_translation, name='update-translation'),
    url('index-translation', index_view, name="index-translation"),
    url('import-translation', import_translation, name="import-translation"),
    url('import-file-translation', import_file_translation, name="import-file-translation"),
    url('export-translation', export_translation, name="export-translation"),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
