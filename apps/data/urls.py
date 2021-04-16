from django.conf.urls import url
from .views import index_import_view, index_export_view, fields_overview, import_file_upload, import_into_model
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^export/overview$'),index_export_view,name="overviewexport"),
    url(_('^export/overview/fields/ajax$'),fields_overview,name="fields-overview"),

    url(_('^import/overview$'),index_import_view,name="overviewimport"),
    url(_('^import/overview/fields/ajax$'),fields_overview,name="fields-import-overview"),
    url(_('^import/overview/file-upload/ajax$'),import_file_upload,name="file-upload-import-overview"),
    url(_('^import/overview/model-handling/ajax$'),import_into_model,name="import-into-model"),
]