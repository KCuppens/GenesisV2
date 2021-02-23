from django.forms import widgets

class URLPickerWidget(widgets.TextInput):
    template_name = 'widgets/url_picker.html'