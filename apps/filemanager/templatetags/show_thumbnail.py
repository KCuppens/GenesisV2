from django import template
from django.db.models import base
register = template.Library()
import glob, os
from PIL import Image
from django.conf import settings
from apps.filemanager.models import Thumbnail, Media
from django.utils.translation import ugettext_lazy as _
from apps.filemanager.utils import get_filename_without_extension, get_extension, get_filename
from apps.filebase.file import upload_file
import requests 
from io import BytesIO
from django.db import models
from apps.filemanager.tasks import create_thumbnails


def get_filename_str(filepath):
    path = filepath.split('/')
    filename = path[-1]
    return filename


@register.simple_tag
def show_thumbnail(instance, size, format):
    # if instance.image:
    #     filename = get_filename_without_extension(get_filename(instance.image))
    #     cloudfront = settings.AWS_CLOUDFRONT_DOMAIN
    #     basepath = cloudfront + settings.AWS_MAIN_DIR 
    #     thumbnail = basepath + '/media/image/' + str(format) + '/' + size + '/' + filename + '.' + str(format)
    #     create_thumbnails(thumbnail, size, instance, format)
    #     return thumbnail

    if isinstance(instance, Media):
        media_instance = Media.objects.filter(file__contains=settings.AWS_MAIN_DIR + instance.image).first()
    elif isinstance(instance, str):
        filename = get_filename_str(instance)
        media = Media.objects.filter(filename=filename).first()
    elif isinstance(instance, models.fields.files.ImageFieldFile):
        filename = get_filename_str(str(instance))
        media = Media.objects.filter(filename=filename).first()
        if not media:
            return str(instance)
    else:
        filename = get_filename(instance)
        media = Media.objects.filter(filename=filename).first()
    
    if media.file:
        filename = get_filename_without_extension(get_filename(media.file))
        cloudfront = settings.AWS_CLOUDFRONT_DOMAIN
        basepath = cloudfront + settings.AWS_MAIN_DIR 
        thumbnail = basepath + '/media/image/' + str(format) + '/' + size + '/' + filename + '.' + str(format)
        create_thumbnails.delay(thumbnail, size, media.id, format)
        return thumbnail
    