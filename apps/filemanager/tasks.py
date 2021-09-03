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
from celery.decorators import task
from celery_once import QueueOnce

@task(name="create_thumbnails", base=QueueOnce, once={'keys': ['instance_id'], 'graceful': True})
def create_thumbnails(thumbnail, size, instance, format):
    instance = Media.objects.filter(id=instance_id).first()
    if not requests.head(thumbnail):
        new_img = None
        media_url = str(settings.MEDIA_URL)
        filename = get_filename_without_extension(get_filename(instance.image))
        cloudfront = settings.AWS_CLOUDFRONT_DOMAIN
        basepath = cloudfront + settings.AWS_MAIN_DIR 
        origpath = '/media/image/orig/'
        orig = get_filename(instance.image)
        image_path = '/media/image/' + str(format) + '/' + size + '/' + filename + '.' + str(format)
        if media_url.startswith('/'):
            media_url = media_url[1:]
        if not size == 'orig':
            image = requests.head(basepath + origpath + orig)
            if image.status_code == 200:
                img = Image.open(BytesIO(image.content)) 
                size_split = size.split('x')
                size_width = size_split[0]
                size_height = size_split[1]
                if size_height and size_width:
                    new_img = img.resize((int(size_width), int(size_height)), resample=1)
                    if not os.path.exists(media_url + 'image/' + str(format) +'/' + size + '/'):
                        os.mkdir(media_url + 'image/' + str(format) +'/' + size + '/')
                    new_img.save(media_url + 'image/' + str(format) +'/' + size + '/' + filename + '.' + str(format) , str(format), optimize=True, quality=75)
                    upload_file(settings.AWS_IMAGE_BUCKET, media_url + 'image/' + str(format) +'/' + size + '/' + filename + '.' + str(format))
                    if os.path.exists(media_url + 'image/' + str(format) +'/' + size + '/' + filename + '.' + str(format)):
                        os.remove(media_url + 'image/' + str(format) +'/' + size + '/' + filename + '.' + str(format))
                    
                    media_instance = Media.objects.filter(file__contains=basepath + origpath + orig).first()
                    if media_instance:
                        thumbnail = Thumbnail.objects.create(format=str(format), size=size, path=basepath +  image_path)
                        media_instance.thumbnails.add(thumbnail)
                        media_instance.save()
                    return basepath + image_path
                else:
                    return _('Size not valid format eg. "400x400"')
            else:
                return ''
        else:
            return basepath + origpath + orig
            