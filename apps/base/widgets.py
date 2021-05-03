from django.forms import widgets
from tags_input import admin as tags_input_admin
from tags_input.widgets import TagsInputWidget
from apps.blocks.models import Block
from django.conf import settings
from django import urls
from django.template.loader import render_to_string
from django import forms
from collections import OrderedDict

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

class MultipleImageWidget(TagsInputWidget):
    template_name = 'widgets/multiple_media_image_widget.html'
    input_type="select"
    
    def render(self, name, value, attrs=None, choices=(), renderer=None):
        print("##########", value)
        context = self.build_attrs(attrs, name=name)
        context['on_add_tag'] = self.on_add_tag
        context['on_remove_tag'] = self.on_remove_tag
        context['on_change_tag'] = self.on_change_tag

        context['STATIC_URL'] = settings.STATIC_URL
        context['mapping'] = self.mapping
        context['autocomplete_url'] = urls.reverse(
            'tags_input:autocomplete',
            kwargs=dict(
                app=self.mapping['app'],
                model=self.mapping['model'],
                fields='-'.join(self.mapping['fields']),
            ),
        )
        if value:
            fields = self.mapping['fields']
            join_func = self.mapping['join_func']

            ids = []
            for v in value:
                if isinstance(v, int):
                    ids.append(v)

            values_map = OrderedDict(map(
                join_func,
                self.mapping['queryset']
                .filter(pk__in=ids)
                .values('pk', *fields)
                .order_by('pk')
            ))

            values = []
            for v in value:
                if isinstance(v, int):
                    values.append(values_map[v])
                else:
                    values.append(v)

            context['values'] = ', '.join(values)

        return render_to_string(self.template_name, context)


class MultipleFileWidget(TagsInputWidget):
    template_name = 'widgets/media_file_widget.html'
    input_type="select"
    
    def render(self, name, value, attrs=None, choices=(), renderer=None):
        context = self.build_attrs(attrs, name=name)
        context['on_add_tag'] = self.on_add_tag
        context['on_remove_tag'] = self.on_remove_tag
        context['on_change_tag'] = self.on_change_tag

        context['STATIC_URL'] = settings.STATIC_URL
        context['mapping'] = self.mapping
        context['autocomplete_url'] = urls.reverse(
            'tags_input:autocomplete',
            kwargs=dict(
                app=self.mapping['app'],
                model=self.mapping['model'],
                fields='-'.join(self.mapping['fields']),
            ),
        )

        if value:
            fields = self.mapping['fields']
            join_func = self.mapping['join_func']

            ids = []
            for v in value:
                if isinstance(v, int):
                    ids.append(v)

            values_map = OrderedDict(map(
                join_func,
                self.mapping['queryset']
                .filter(pk__in=ids)
                .values('pk', *fields)
                .order_by('pk')
            ))

            values = []
            for v in value:
                if isinstance(v, int):
                    values.append(values_map[v])
                else:
                    values.append(v)

            context['values'] = ', '.join(values)

        return render_to_string(self.template_name, context)


