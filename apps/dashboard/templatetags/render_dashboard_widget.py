from apps.pages.models import Page
from django import forms, template
register = template.Library()
from django.template.loader import render_to_string

@register.simple_tag
def render_dashboard_widget(request, widget):
    context = {
        'widget': widget
    }
    template = render_to_string('dashboard/dashboardtemplates/' + str(widget.template) + '.html', context=context, request=request)
    return template