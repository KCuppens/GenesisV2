from django import template
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


@register.simple_tag
def show_thumbnail(instance, size, format):
    if instance.image:
        extension = get_extension(instance.image)
        filename = get_filename_without_extension(get_filename(instance.image))
        cloudfront = settings.AWS_CLOUDFRONT_DOMAIN
        basepath = cloudfront + settings.AWS_MAIN_DIR 
        aws_active = settings.AWS_ACTIVE
        origpath = '/media/image/orig/'
        orig_webp_path = '/media/image/webp/'
        orig = get_filename(instance.image)
        media_root = str(settings.MEDIA_ROOT).replace('\\', '/')
        if extension == 'svg':
            if aws_active:
                return cloudfront + str(instance.image)
            else:
                return instance.image

        if format == "webp":
            webp_path = '/media/image/webp/' + size + '/' + filename + '.webp'
            if aws_active:
                img_obj = requests.head(basepath +  webp_path)
                if img_obj.status_code == 200:
                    return basepath + webp_path
                else:
                    new_img = None
                    if not size == 'orig':
                        image = requests.get(basepath + origpath + orig)
                        if image.status_code == 200:
                            img = Image.open(BytesIO(image.content)) 
                            size_split = size.split('x')
                            size_width = size_split[0]
                            size_height = size_split[1]
                            if size_height and size_width:
                                new_img = img.resize((int(size_width), int(size_height)), resample=1)
                                new_img = new_img.convert('RGB')
                                if not os.path.exists(media_root + 'image/webp/' + size + '/'):
                                    os.mkdir(media_root + 'image/webp/' + size + '/')
                                new_img.save(media_root + 'image/webp/' + size + '/' + filename + '.webp', 'webp', optimize=True, quality=75)
                                upload_file(settings.AWS_IMAGE_BUCKET, media_root + 'image/webp/' + size + '/' + filename + '.webp')
                                if os.path.exists(media_root + 'image/webp/' + size + '/' + filename + '.webp'):
                                    os.remove(media_root + 'image/webp/' + size + '/' + filename + '.webp')
                                
                                media_instance = Media.objects.filter(file__contains=basepath + origpath + orig).first()
                                if media_instance:
                                    thumbnail = Thumbnail.objects.create(format="webp", size=size, path=basepath +  webp_path)
                                    media_instance.thumbnails.add(thumbnail)
                                    media_instance.save()
                                return basepath + webp_path
                            else:
                                return _('Size not valid format eg. "400x400"')
                        else:
                            return ''
                    else:
                        return basepath + origpath + orig

            else:
                if os.path.exists(webp_path):
                    return webp_path
                elif not os.path.exists(webp_path):
                    new_img = None
                    if not size == 'orig':
                        img = Image.open(instance.image)
                        size_split = size.split('x')
                        size_width = size_split[0]
                        size_height = size_split[1]
                        if size_height and size_width:
                            new_img = img.resize((int(size_width), int(size_height)), resample=1)
                            if not os.path.exists(media_root + 'image/webp/' + size + '/'):
                                    os.mkdir(media_root + 'image/webp/' + size + '/')
                            new_img = new_img.convert('RGB')
                            new_img.save(media_root + 'image/webp/' + size + '/' + filename + '.webp', 'webp', optimize=True, quality=75)
                            thumbnail = Thumbnail.objects.create(format="webp", size=size, path=basepath +  webp_path)
                            
                            media_instance = Media.objects.filter(file__contains=basepath + origpath + orig).first()
                            if media_instance:
                                    thumbnail = Thumbnail.objects.create(format="webp", size=size, path=basepath +  webp_path)
                                    media_instance.thumbnails.add(thumbnail)
                                    media_instance.save()
                            media_instance.thumbnails.add(thumbnail)
                            media_instance.save()
                            return basepath + webp_path
                        else:
                            return _('Size not valid format eg. "400x400"')
                    else:
                        return basepath + origpath + orig
        elif format == 'png':
            png_path = '/media/image/png/' + size + '/' + filename + '.png'
            if aws_active:
                img_obj = requests.head(basepath +  png_path)
                if img_obj.status_code == 200:
                    return basepath + png_path
                else:
                    new_img = None
                    if not size == 'orig':
                        image = requests.get(basepath + origpath + orig, stream=True)
                        if image.status_code == 200:
                            img = Image.open(BytesIO(image.content)) 
                            size_split = size.split('x')
                            size_width = size_split[0]
                            size_height = size_split[1]
                            if size_height and size_width:
                                new_img = img.resize((int(size_width), int(size_height)), resample=1)
                                new_img = new_img.convert('RGB')
                                if not os.path.exists(media_root + 'image/png/' + size + '/'):
                                    os.mkdir(media_root + 'image/png/' + size + '/')
                                new_img.save(media_root + 'image/png/' + size + '/' + filename + '.png', 'png', optimize=True, quality=75)
                                upload_file(settings.AWS_IMAGE_BUCKET, media_root + 'image/png/' + size + '/' + filename + '.png')
                                if os.path.exists(media_root + 'image/png/' + size + '/' + filename + '.png'):
                                    os.remove(media_root + 'image/png/' + size + '/' + filename + '.png')
                                
                                media_instance = Media.objects.filter(file__contains=basepath + origpath + orig).first()
                                if media_instance:
                                    thumbnail = Thumbnail.objects.create(format="png", size=size, path=basepath +  png_path)
                                    media_instance.thumbnails.add(thumbnail)
                                    media_instance.save()
                                return basepath + png_path
                            else:
                                return _('Size not valid format eg. "400x400"')
                        else:
                            return ''
                    else:
                        return basepath + origpath + orig

            else:
                if os.path.exists(png_path):
                    return png_path
                elif not os.path.exists(png_path):
                    new_img = None
                    if not size == 'orig':
                        img = Image.open(instance.image)
                        size_split = size.split('x')
                        size_width = size_split[0]
                        size_height = size_split[1]
                        if size_height and size_width:
                            new_img = img.resize((int(size_width), int(size_height)), resample=1)
                            if not os.path.exists(media_root + 'image/png/' + size + '/'):
                                    os.mkdir(media_root + 'image/png/' + size + '/')
                            new_img = new_img.convert('RGB')
                            new_img.save(media_root + 'image/png/' + size + '/' + filename + '.png', 'png', optimize=True, quality=75)
                            thumbnail = Thumbnail.objects.create(format="png", size=size, path=basepath +  png_path)
                            
                            media_instance = Media.objects.filter(file__contains=basepath + origpath + orig).first()
                            if media_instance:
                                    thumbnail = Thumbnail.objects.create(format="png", size=size, path=basepath +  png_path)
                                    media_instance.thumbnails.add(thumbnail)
                                    media_instance.save()
                            media_instance.thumbnails.add(thumbnail)
                            media_instance.save()
                            return basepath + png_path
                        else:
                            return _('Size not valid format eg. "400x400"')
                    else:
                        return basepath + origpath + orig


    