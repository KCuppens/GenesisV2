from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MailConfig(AppConfig):
    name = 'apps.mail'

    def ready(self):
        from apps.mail.signals import (
        	email_queued,
        	post_mailtemplaterevision_commit,
        	post_mailconfigrevision_commit
        )
