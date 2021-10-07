from django import template
from django.db.models import base
register = template.Library()
import glob, os
from PIL import Image
from django.conf import settings
from apps.filemanager.models import Thumbnail, Media
from apps.pages.models import PageBlockElement
from django.utils.translation import ugettext_lazy as _
from apps.filemanager.utils import get_filename_without_extension, get_extension, get_filename, get_filename_manager
from apps.filebase.file import upload_file
import requests 
from io import BytesIO
from django.db import models
from apps.filemanager.tasks import create_thumbnails 
from django.core.cache import cache
import redis  
r = redis.Redis(host='localhost', port=6379, db=0)
    
@register.simple_tag
def show_thumbnail(instance, size, format):
    if isinstance(instance, str):
        cache_key = 'get_current_media_{}_{}_{}'.format(instance, size, format)
    elif isinstance(instance, models.fields.files.ImageFieldFile):
        filename = get_filename(str(instance))
        media = Media.objects.filter(filename=filename).first()
        if media:
            cache_key = 'get_current_media_{}_{}_{}'.format(media.id, size, format)
        else:
            cache_key = 'get_current_media_{}_{}_{}'.format(str(instance), size, format)
    else:
        cache_key = 'get_current_media_{}_{}_{}'.format(instance.id, size, format)
    lock_key = 'Lock:{}'.format(cache_key)
    cache_value = cache.get(cache_key)
    if cache_value is not None:
        media = cache_value
    else:
        try:
            with r.lock(lock_key, timeout=60, blocking_timeout=0):
                # if not isinstance(instance, str):
                #     media = Media.objects.filter(file__contains=instance.image).first()
                if isinstance(instance, str):
                    filename = get_filename(instance)
                    media = Media.objects.filter(filename=filename).first()
                elif isinstance(instance, models.fields.files.ImageFieldFile):
                    filename = get_filename(str(instance))
                    media = Media.objects.filter(filename=filename).first()
                    if not media:
                        return str(instance)
                elif hasattr(instance, 'image'):
                    media = Media.objects.filter(file__contains=instance.image).first()
                else:
                    filename = get_filename(instance)
                    media = Media.objects.filter(filename=filename).first()
                    if not media:
                        return str(instance)
        except redis.exceptions.LockError:  
            raise Exception('ColdCacheException')

        cache.set(cache_key, media, int(24 * 60 * 60))  # cache for 4 hours 
    
    if media and media.file:
        filename = get_filename_without_extension(media.filename)
        basepath = settings.AWS_CLOUDFRONT_DOMAIN
        thumbnail = basepath + '/media/image/' + str(format) + '/' + size + '/' + filename + '.' + str(format)
        create_thumbnails.delay(thumbnail, size, media.id, format)
        return thumbnail
    else:
        return ''
