import warnings

from django.conf import settings
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError
from django.core.mail.utils import DNS_NAME
from django.template import engines as template_engines
from apps.conf.utils import get_config

from django.utils.module_loading import import_string

import datetime


def get_backend(alias='default'):
    return get_available_backends()[alias]


def get_available_backends():
    """ Returns a dictionary of defined backend classes. For example:
    {
        'default': 'django.core.mail.backends.smtp.EmailBackend',
        'locmem': 'django.core.mail.backends.locmem.EmailBackend',
    }
    """
    backends = settings.BACKENDS

    if backends:
        return backends

    backend = settings.EMAIL_BACKEND
    if backend:
        warnings.warn('Please use the new "BACKENDS" settings',
                      DeprecationWarning)

        backends['default'] = backend
        return backends

    # Fall back to Django's EMAIL_BACKEND definition
    backends['default'] = getattr(
        settings, 'EMAIL_BACKEND',
        'django.core.mail.backends.smtp.EmailBackend')

    # If EMAIL_BACKEND is set to use mail
    # and EMAIL_BACKEND is not set, fall back to SMTP
    if 'apps.mail.backends.EmailBackend' in backends['default']:
        backends['default'] = 'django.core.mail.backends.smtp.EmailBackend'

    return backends


def get_cache_backend():
    if hasattr(settings, 'CACHES'):
        if "mail_backend" in settings.CACHES:
            return caches["post_office"]
        else:
            # Sometimes this raises InvalidCacheBackendError, which is ok too
            try:
                return caches["default"]
            except InvalidCacheBackendError:
                pass
    return None

def get_batch_size():
    return str(get_config('BATCH_SIZE'))


def get_threads_per_process():
    return 5


def get_default_priority():
    return 'medium'


def get_log_level():
    return '2'


def get_sending_order():
    return ['-priority']


def get_template_engine():
    using = settings.TEMPLATE_ENGINE
    return template_engines[using]

def get_max_retries():
    return 0


def get_retry_timedelta():
    return datetime.timedelta(minutes=15)

CONTEXT_FIELD_CLASS = 'jsonfield.JSONField'
context_field_class = import_string(CONTEXT_FIELD_CLASS)