from django.apps import AppConfig


class FilemanagerConfig(AppConfig):
    name = 'apps.filemanager'

    def ready(self):
    	import apps.filemanager.signals
