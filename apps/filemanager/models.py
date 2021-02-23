from django.db import models
from apps.base.models import BaseModel, AdminModel
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
import datetime
from pathlib import Path
import mimetypes
import os
now = datetime.datetime.now()
# Create your models here.
class Directory(BaseModel, AdminModel):
    GET_TYPES = [
            ('image', _('Images')),
            ('audio', _('Audio')),
            ('file', _('File')),
            ('video', _('Video'))
    ]

    def get_icon(type):
        icons = {
            ('image', 'image'),
            ('audio', 'volume-2'),
            ('file', 'file'),
            ('video', 'video')
        }

        if not type in icons:
            return None
        return icons[type]


    name = models.CharField(max_length=255, db_index=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    summary = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=GET_TYPES, default='image', blank=True)
    parent = models.ForeignKey("self", blank=True, on_delete=models.CASCADE, related_name="children", null=True)
    documents = models.ManyToManyField('media', blank=True, related_name="directory_documents")
    depth = models.IntegerField(default=0)

    def get_parent(self):
        return self.parent

    def has_parent(self):
        if self.parent:
            return self.parent

    def __str__(self):
        return self.name
    

class Media(BaseModel, AdminModel):
    TYPE_IMAGE = 'image'
    TYPE_FILE = 'file'
    TYPE_VIDEO = 'video'
    TYPE_AUDIO = 'audio'

    BASE_DIR = Path(__file__).resolve().parent.parent

    PREFIX = 'genesis_media__'

    GET_TYPES = [
            (TYPE_IMAGE, _('Image')),
            (TYPE_FILE, _('File')),
            (TYPE_VIDEO, _('Video')),
            (TYPE_AUDIO, _('Image')),
        ]

    def get_max_file_size():
        return '20M'

    def get_valid_image_mime_types():
        return [
            ('png', 'image/png'),
            ('jpe', 'image/jpeg'),
            ('jpeg', 'image/jpeg'),
            ('jpg', 'image/jpeg'),
            ('gif', 'image/gif'),
            ('bmp', 'image/bmp'),
            ('webp', 'image/webp'),
            ('svg', 'image/svg+xml')
        ]
    
    def get_valid_video_mime_types():
        return [
            ('mp4', 'video/mp4'),
            ('qt', 'application/octet-stream'),
            ('mov', 'video/quicktime')
        ]

    def get_valid_audio_mime_types():
        return [
            ('mp3', ['audio/mpeg', 'audio/mp3', 'audio/x-mp3', 'audio/x-mpeg', 'audio/x-mpg']),
            ('wav', ['audio/wav', 'audio/vnd.wave', 'audio/x-wav'])
        ]

    def get_valid_file_mime_types():
        return [
            ('txt', 'text/plain'),
            ('zip', 'application/zip'),
            ('rar', 'application/x-rar-compressed'),
            ('pdf', 'application/pdf'),
            ('doc', 'application/msword'),
            ('dot', 'application/msword'),
            ('rtf', 'application/rtf'),
            ('xls', 'application/vnd.ms-excel'),
            ('ppt', 'application/vnd.ms-powerpoint'),
            ('docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
            ('xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('pptx', 'application/vnd.ms-powerpoint'),
            ('odt', 'application/vnd.oasis.opendocument.text'),
            ('ods', 'application/vnd.oasis.opendocument.spreadsheet'),
        ]

    def get_valid_mime_types(self):
        return [
            self.get_valid_image_mime_types(),
            self.get_valid_video_mime_types(),
            self.get_valid_audio_mime_types(),
            self.get_valid_file_mime_types()
        ]

    def get_feather_file_icon():
        return [
            ('txt', ('file')),
            ('png', ('image')),
            ('jpe', ('image')),
            ('jpeg', ('image')),
            ('jpg', ('image')),
            ('gif', ('image')),
            ('bmp', ('image')),
            ('svg', ('image')),
            ('webp', ('image')),
            ('zip', ('archive')),
            ('rar', ('archive')),
            ('pdf', ('file-plus')),
            ('doc', ('file-plus')),
            ('dot', ('file-plus')),
            ('rtf', ('file-plus')),
            ('xls', ('file-plus')),
            ('ppt', ('file-plus')),
            ('docx', ('file-plus')),
            ('xlsx', ('file-plus')),
            ('pptx', ('file-plus')),
            ('odt', ('file-plus')),
            ('ods', ('file-plus')),
            ('mp4', ('film')),
            ('mov', ('film')),
            ('mp3', ('volume-2')),
            ('wav', ('volume-2')),
        ]

    def guess_mime_type():
        return mimetypes.MimeTypes().guess_type(self.get_absolute_path())

    def guess_icon():
        filename, file_extension = os.path.splitext(self.filename)

        if file_extension in self.get_feather_file_icon():
            return self.get_feather_file_icon()[file_extension]

        return 'file-plus'

    def guess_media_type(mime):
        if mime in self.get_valid_image_mime_types():
            return self.TYPE_IMAGE
        elif mime in self.get_valid_video_mime_types():
            return self.TYPE_VIDEO
        elif mime in self.get_valid_file_mime_types():
            return self.TYPE_FILE
        elif mime in self.get_valid_audio_mime_types():
            return self.TYPE_AUDIO

    def get_relative_path():
        return self.get_upload_dir() + '/' + self.path 

    def get_absolute_path():
        if not self.path:
            return None 
        return self.get_upload_root_dir() + '/' + self.path

    def get_upload_root_dir():
        return self.BASE_DIR + '/media' + self.get_upload_dir()

    def get_upload_sub_dir():
        return self.id 

    def get_upload_dir():
        dir = self.type 
        if self.type == 'image':
            dir = dir + '/orig'
        return dir
    
    name = models.CharField(max_length=255, db_index=True, blank=True)
    filename = models.CharField(max_length=255, blank=True)
    path = models.CharField(max_length=255, blank=True) 
    directory = models.ForeignKey('media', on_delete=models.CASCADE, blank=True, null=True, related_name="media_directory")
    summary = models.TextField(blank=True, null=True)
    slug = AutoSlugField(populate_from='name')
    copyright = models.CharField(max_length=255, blank=True)
    keywords = models.CharField(max_length=255, db_index=True, blank=True)
    alt = models.CharField(max_length=255, blank=True) 
    type = models.CharField(max_length=255, blank=True, choices=GET_TYPES, default=TYPE_IMAGE) 
    searchable = models.BooleanField(default=False)
    file_size = models.IntegerField(default=0)
    metadata = models.TextField(null=True, blank=True)

    def get_metadata(self):
        return self.metadata

    def set_metadata(self, metadata):
        self.metadata = metadata 
