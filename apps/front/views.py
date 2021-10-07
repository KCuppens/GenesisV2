from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import render, reverse
from apps.pages.models import Page 
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.http import JsonResponse
from apps.news.models import Article 
from apps.pages.models import DetailPage
from django.core.cache import cache
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

def page_view(request, slug):
    cache_key = 'get_current_page_{}'.format(slug)
    lock_key = 'Lock:{}'.format(cache_key)
    cache_value = cache.get(cache_key)
    if cache_value is not None:
        page = cache_value
    else:
        try:
            with r.lock(lock_key, timeout=60, blocking_timeout=0):  
                if slug == '':
                    page = Page.objects.filter(slug=slug, active=True, date_deleted=None).prefetch_related('canvas__rows__block').first()
                else:
                    page = Page.objects.filter(full_slug=slug, active=True, date_deleted=None).prefetch_related('canvas__rows__block').first()
                    if not page:
                        page = Page.objects.filter(slug=slug, active=True, date_deleted=None).prefetch_related('canvas__rows__block').first()
        except redis.exceptions.LockError:  
            raise Exception('ColdCacheException')   
        
        cache.set(cache_key, page, int(24 * 60 * 60))  # cache for 4 hours 
    template_name = None
    if page:
        Head(request).override_by_object(page)
    if page and page.url_type == Page.URL_TYPE_LINK_THROUGH:
        return redirect(page.linkthrough)
    elif page:
        template_name = 'front/index.html'
    else:
        raise Http404(_("Pagina bestaat niet"))
    return render(request, template_name, {
        'page': page,
    })

def page_detail_view(request, model, pk, slug):
    cache_key_object = 'get_current_object_{}'.format(slug)
    cache_key_detail = 'get_current_detail_{}'.format(pk)
    lock_key = 'Lock:{}'.format(cache_key_object + '_' + cache_key_detail)
    cache_value_object = cache.get(cache_key_object)
    cache_value_detail = cache.get(cache_key_detail)
    if cache_value_object is not None and cache_value_detail is not None:
        object = cache_value_object
        detailpage = cache_value_detail
    else:
        try:
            with r.lock(lock_key, timeout=60, blocking_timeout=0):  
                object = eval(model.capitalize()).objects.filter(slug=slug).first()
                detailpage = DetailPage.objects.filter(pk=pk).first()
        except redis.exceptions.LockError:  
            raise Exception('ColdCacheException')   
        
        cache.set(cache_key_object, object, int(24 * 60 * 60)) 
        cache.set(cache_key_detail, detailpage, int(24 * 60 * 60))
    Head(request).override_by_object(object)
    if not object or not detailpage:
        raise Http404(_('Detailpagina bestaat niet'))

    return render(request, 'front/detail.html', {'object': object, 'detailpage': detailpage})

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)