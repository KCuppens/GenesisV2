from apps.conf.models import Configuration
from apps.base.utils import check_tables

def get_config(key_name):
    try:
        return ''
        if check_tables('conf_configuration'):
            config = Configuration.objects.only('value').filter(key_name=key_name).first()
            return config
        return ''
    except Configuration.DoesNotExist:
        return ""

