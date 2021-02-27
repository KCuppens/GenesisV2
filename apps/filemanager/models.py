from django.db import models
from apps.base.models import BaseModel, AdminModel
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from apps.filemanager.utils import base_media_path
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

    

    def guess_mime_type():
        return mimetypes.MimeTypes().guess_type(self.get_absolute_path())

    def guess_icon():
        filename, file_extension = os.path.splitext(self.filename)

        if file_extension in self.get_feather_file_icon():
            return self.get_feather_file_icon()[file_extension]

        return 'file-plus'

    def guess_media_type(mime):
        if mime in get_valid_image_mime_types():
            return self.TYPE_IMAGE
        elif mime in get_valid_video_mime_types():
            return self.TYPE_VIDEO
        elif mime in get_valid_file_mime_types():
            return self.TYPE_FILE
        elif mime in get_valid_audio_mime_types():
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
    file = models.FileField(upload_to=base_media_path)
    directory = models.ForeignKey('directory', on_delete=models.CASCADE, blank=True, null=True, related_name="media_directory")
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
