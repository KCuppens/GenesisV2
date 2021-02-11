from __future__ import absolute_import
import logging
import os

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def svg(filename):

    svg_dir = 'static/admin/img/feather/'

    path = None

    if svg_dir:
        svg_path = os.path.join(svg_dir, '{filename}.svg'.format(
            filename=filename))

        if os.path.isfile(svg_path):
            path = svg_path
    else:
        path = finders.find(os.path.join('svg', '{filename}.svg'.format(
            filename=filename)), all=True)

    if not path:
        message = "SVG '{filename}.svg' not found".format(filename=filename)

        # Raise exception if DEBUG is True, else just log a warning.
        return ''

    # Sometimes path can be a list/tuple if there's more than one file found
    if isinstance(path, (list, tuple)):
        path = path[0]

    with open(path) as svg_file:
        svg = mark_safe(svg_file.read())

    return svg

