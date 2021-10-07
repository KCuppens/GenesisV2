from django import template
from django.conf import settings
register = template.Library()
from apps.conf.models import Configuration
from django.core.cache import cache
import redis  
r = redis.Redis(host='localhost', port=6379, db=0)

@register.simple_tag
def get_setting(request, keyname):
    cache_key = 'get_current_setting_{}'.format(keyname)
    lock_key = 'Lock:{}'.format(cache_key)
    cache_value = cache.get(cache_key)
    if cache_value is not None:
        return cache_value
    else:
        try:
            with r.lock(lock_key, timeout=60, blocking_timeout=0): 
                setting = Configuration.objects.filter(key_name=keyname).first()
        except redis.exceptions.LockError:  
            raise Exception('ColdCacheException') 
        if setting:
            cache.set(cache_key, setting.value, int(24 * 60 * 60))  # cache for 4 hours  
    if setting:
        return setting.value