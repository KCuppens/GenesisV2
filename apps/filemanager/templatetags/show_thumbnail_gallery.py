from apps.pages.models import Page
from apps.filemanager.models import Media
from django import forms, template
register = template.Library()
from PIL import Image
import glob, os
from PIL import Image
from django.conf import settings
from apps.filemanager.models import Thumbnail
from django.utils.translation import ugettext_lazy as _
from apps.filemanager.utils import get_filename_without_extension
import requests 

from io import BytesIO


@register.simple_tag
def show_thumbnail_gallery(instance, size, format):
    media_instance = Media.objects.filter(file__contains=instance).first()
    base_path = settings.MEDIA_ROOT + 'image'
    media_path = settings.MEDIA_URL + 'image'
    filename = get_filename_without_extension(media_instance.filename)
    if format == "webp":
        if media_instance and os.path.exists(base_path + '/webp/' + size + '/' + filename + '.webp'):
            return media_path + '/webp/' + size + '/' + filename + '.webp'
        elif media_instance and not os.path.exists(base_path + '/webp/' + size + '/' + filename + '.webp'):
            new_img = None
            if not size == 'orig':
                img = Image.open(media_instance.file)
                size_split = size.split('x')
                size_width = size_split[0]
                size_height = size_split[1]
                if size_height and size_width:
                    new_img = img.resize((int(size_width), int(size_height)), resample=1)
                    if not os.path.exists(base_path + '/webp/' + size + '/'):
                        os.mkdir(base_path + '/webp/' + size + '/')
                    new_img = new_img.convert('RGB')
                    new_img.save(base_path + '/webp/' + size + '/' + filename + '.webp', 'webp', optimize=True, quality=75)
                    thumbnail = Thumbnail.objects.create(format="webp", size=size, path=media_path + '/webp/' + size + '/' + filename + '.webp')
                    media_instance.thumbnails.add(thumbnail)
                    media_instance.save()
                    return media_path + '/webp/' + size + '/' + filename + '.webp'
                else:
                    return _('Size not valid format eg. "400x400"')
            else:
                return media_instance.file
        else:
            pass
            #default image
    elif format == "png":
        if media_instance and os.path.exists(base_path + '/png/' + size + '/' + filename + '.png'):
            return media_path + '/png/' + size + '/' + filename + '.png'
        elif media_instance and not os.path.exists(base_path + '/png/' + size + '/' + filename + '.png'):
            new_img = None
            if not size == 'orig':
                img = Image.open(media_instance.file)
                size_split = size.split('x')
                size_width = size_split[0]
                size_height = size_split[1]
                if size_height and size_width:
                    new_img = img.resize((int(size_width), int(size_height)), resample=1)
                    if not os.path.exists(base_path + '/png/' + size + '/'):
                        os.mkdir(base_path + '/png/' + size + '/')
                    new_img = new_img.convert('RGB')
                    new_img.save(base_path + '/png/' + size + '/' + filename + '.png', 'png', optimize=True, quality=75)
                    thumbnail = Thumbnail.objects.create(format="png", size=size, path=media_path + '/png/' + size + '/' + filename + '.png')
                    media_instance.thumbnails.add(thumbnail)
                    media_instance.save()
                    return media_path + '/png/' + size + '/' + filename + '.png'
                else:
                    return _('Size not valid format eg. "400x400"')
            else:
                return media_instance.file
        else:
            pass
            #default image
    