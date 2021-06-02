from apps.base.widgets import MediaImageWidget
import uuid

class PageMediaImageWidget(MediaImageWidget):
    template_name = 'pages/widgets/media_image_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['from_pages_app'] = True
        context['widget_unique_id'] = uuid.uuid4()
        return context


class PageMediaVideoWidget(MediaImageWidget):
    template_name = 'pages/widgets/media_video_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['from_pages_app'] = True
        context['widget_unique_id'] = uuid.uuid4()
        return context