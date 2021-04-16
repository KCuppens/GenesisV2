from apps.pages.models import Page
from django import forms, template
register = template.Library()
from django.template.loader import render_to_string

@register.simple_tag
def render_block_page(request, block, object = None):
    context = {
        'block': block,
        'object': object
    }
    if block.block.template:
        template = render_to_string('blocks/templates/' + str(block.block.template) + '.html', context=context, request=request)
        return template
    return ''