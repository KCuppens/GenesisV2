from django.forms import ModelChoiceField

class IconField(ModelChoiceField):
    def label_from_instance(self, obj):
        return '<span class="{icon}"></span> - {name}'.format(icon=obj.icon, name=obj.name)
