from django.apps import AppConfig


class BlocksConfig(AppConfig):
    name = 'apps.blocks'

    def ready(self):
    	import apps.blocks.signals
