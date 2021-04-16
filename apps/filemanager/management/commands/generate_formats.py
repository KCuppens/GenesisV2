from django.core.management.base import BaseCommand
from apps.filemanager.models import Media
from django.utils import timezone
from django.conf import settings
from apps.filemanager.utils import get_filename_without_extension
from PIL import Image
import glob, os

class Command(BaseCommand):
    help = 'Generate formats'

    def handle(self, *args, **kwargs):
        base_path = settings.MEDIA_ROOT + "image/orig/"
        if not os.path.exists(base_path + '/webp/'):
            os.makedirs(base_path + '/webp/')
        if not os.path.exists(base_path + '/png/'):
            os.makedirs(base_path + '/png/')

        images = Media.objects.filter(type="image", date_deleted=None, formats=False)

        for image in images:
            current_image = Image.open(image.file.name)
            filename = get_filename_without_extension(image.filename)
            current_image.convert("RGB")
            current_image.save(base_path + 'webp/' + filename + '.webp' , 'webp')
            image.webp_path = base_path + 'webp/' + filename + '.webp'
            current_image.save(base_path + 'png/' + filename + '.png' , 'png')
            image.png_path = base_path + 'png/' + filename + '.png'
            image.formats = True 
            image.save()
            
