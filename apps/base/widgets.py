from django.forms import widgets

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
    template_name = 'widgets/multiple_image_widget.html'