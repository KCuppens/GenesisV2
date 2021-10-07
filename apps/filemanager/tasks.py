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

@task(name="create_thumbnails", base=QueueOnce, once={'keys': ['size', 'instance_id', 'format'], 'graceful': True})
def create_thumbnails(thumbnail, size, instance_id, format):
    instance = Media.objects.filter(id=instance_id).first()
    if not requests.get(thumbnail):
        new_img = None
        media_url = str(settings.MEDIA_URL)
        media_root = str(settings.MEDIA_ROOT)
        filename = get_filename_without_extension(instance.filename)
        cloudfront = settings.AWS_CLOUDFRONT_DOMAIN
        origpath = '/media/image/orig/'
        image_path = '/media/image/' + str(format) + '/' + size + '/' + filename + '.' + str(format)
        if media_url.startswith('/'):
            media_url = media_url[1:]
        if not size == 'orig':
            image = requests.get(cloudfront + origpath + str(instance.filename))
            if image.status_code == 200:
                img = Image.open(BytesIO(image.content)) 
                size_split = size.split('x')
                size_width = size_split[0]
                size_height = size_split[1]
                if size_height and size_width:
                    new_img = img.resize((int(size_width), int(size_height)), resample=1)
                    if not os.path.exists(media_root + 'image/' + str(format) +'/' + size + '/'):
                        os.makedirs(media_root + 'image/' + str(format) +'/' + size + '/')
                    new_img.save(media_root + 'image/' + str(format) +'/' + size + '/' + filename + '.' + str(format) , str(format), optimize=True, quality=75)
                    response = upload_file(settings.AWS_IMAGE_BUCKET, media_url + 'image/' + str(format) +'/' + size + '/' + filename + '.' + str(format))
                    if os.path.exists(media_root + 'image/' + str(format) +'/' + size + '/' + filename + '.' + str(format)):
                        os.remove(media_root + 'image/' + str(format) +'/' + size + '/' + filename + '.' + str(format))
                    
                    if instance:
                        thumbnail = Thumbnail.objects.create(format=str(format), size=size, path=cloudfront +  image_path)
                        instance.thumbnails.add(thumbnail)
                        instance.save()
                    return 'created'
                else:
                    return _('Size not valid format eg. "400x400"')
            else:
                return ''
        else:
            return cloudfront + origpath + filename
    else:
        return 'exists'
