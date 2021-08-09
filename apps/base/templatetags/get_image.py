from django import forms, template
from apps.base.utils import generate_perma_url
register = template.Library()
from django.conf import settings


@register.simple_tag
def get_image(image):
    if settings.AWS_ACTIVE:
        if image.media_path:
            return image.media_path
        return 'not-found'
    else:
        path = str(image).split('/')
        if 'media' in path:
            index = path.index('media')
            url_path = '/' + '/'.join(path[index:])
            print(url_path)
            return url_path
        return 'not-found'