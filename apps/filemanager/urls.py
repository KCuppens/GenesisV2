from django.conf.urls import url
from .views import delete_thumbnail, delete_modal_thumbnail, show_thumbnails, media_document_index_view, download_media, create_directory, create_media_type, get_media_overview, edit_directory, delete_modal_directory, delete_directory, create_media_type, edit_media, delete_media, delete_modal_media, \
                   get_version_ajax_modal, get_delete_version_ajax_modal, \
                   select_version, delete_version, add_version_comment
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^media/document/index$').strip(),media_document_index_view,name="media-document-index"),
    url(_('^media/document/overview$').strip(),get_media_overview,name="media-overview"),
    url(_('^media/thumbnail/overview$').strip(),show_thumbnails,name="thumbnail-overview"),
    url(_('^media/create/directory$').strip(),create_directory,name="create-directory"),
    url(_('^media/add$').strip(),create_media_type,name="add-media"),
    url(_('^media/edit/directory$').strip(),edit_directory,name="edit-directory"),
    url(_('^media/delete/directory/(?P<pk>[0-9a-f-]+)$').strip(),delete_directory,name="delete-directory"),
    url(_('^media/delete/directory/modal$').strip(),delete_modal_directory,name="delete-modal-directory"),
    url(_('^media/create/mediatype$').strip(),create_media_type,name="create-media-type"),
    url(_('^media/edit$').strip(),edit_media,name="edit-media"),
    url(_('^media/download/(?P<pk>[0-9a-f-]+)$').strip(),download_media,name="download-media"),
    url(_('^media/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_media,name="delete-media"),
    url(_('^media/delete/modal$').strip(),delete_modal_media,name="delete-modal-media"),
    url(_('^media/delete/thumbnail/(?P<pk>[0-9a-f-]+)$').strip(),delete_thumbnail,name="delete-thumbnail"),
    url(_('^media/delete/thumbnail/modal$').strip(),delete_modal_thumbnail,name="delete-modal-thumbnail"),

    url(_('^version/modal/(?P<mode>[a-z]+)/$').strip(),get_version_ajax_modal,name="filemanagerversionmodal"),
    url(_('^version/modal/delete/(?P<mode>[a-z]+)/$').strip(),get_delete_version_ajax_modal,name="filemanagerdeleteversionmodal"),
    url(_('^version/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)$').strip(),select_version,name="filemanagerselectversion"),
    url(_('^version/delete/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)/$').strip(),delete_version,name="filemanagerdeleteversion"),
    url(_('^version/comment/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)/$').strip(),add_version_comment,name="filemanageraddversioncomment"),
]