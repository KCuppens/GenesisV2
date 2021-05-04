from django.forms import widgets
from tags_input import admin as tags_input_admin
from tags_input.widgets import TagsInputWidget
from apps.blocks.models import Block
from django.conf import settings
from django import urls
from django.template.loader import render_to_string
from django import forms
from collections import OrderedDict
from apps.filemanager.models import Media


class URLPickerWidget(widgets.TextInput):
    template_name = 'widgets/url_picker.html'

class MediaFileWidget(widgets.TextInput):
    template_name = 'widgets/media_file_widget.html'

class MediaImageWidget(widgets.TextInput):
    template_name = 'widgets/media_image_widget.html'

class MediaAudioWidget(widgets.TextInput):
    template_name = 'widgets/media_audio_widget.html'

class MediaVideoWidget(widgets.TextInput):
    template_name = 'widgets/media_video_widget.html'

class MultipleImageWidget(widgets.TextInput):
    template_name = 'widgets/multiple_media_image_widget.html'

class MultipleFileWidget(widgets.TextInput):
    template_name = 'widgets/multiple_media_file_widget.html'
