from apps.base.widgets import MultipleImageWidget

class NewsMultipleImageWidget(MultipleImageWidget):

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['from_news_app'] = True
        return context