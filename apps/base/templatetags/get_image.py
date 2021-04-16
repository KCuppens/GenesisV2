from django import forms, template
from apps.base.utils import generate_perma_url
register = template.Library()


@register.simple_tag
def get_image(image):
    path = str(image).split('/')
    if 'media' in path:
        index = path.index('media')
        url_path = '/' + '/'.join(path[index:])
        return url_path
    return 'not-found'


