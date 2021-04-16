from django import template
from apps.front.head import Head
register = template.Library()

@register.simple_tag
def get_head(request, keyname):
    head = Head(request)
    if keyname == 'author':
        return head.get_author()
    elif keyname == 'title':
        return head.get_title()
    elif keyname == 'keywords':
        return head.get_keywords()
    elif keyname == 'description':
        return head.get_description()