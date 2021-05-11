from django.apps import AppConfig


class FormbuilderConfig(AppConfig):
    name = 'apps.formbuilder' 

    def ready(self):
    	import apps.formbuilder.signals

