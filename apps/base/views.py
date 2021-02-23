from django.shortcuts import render
from apps.modules.models import Module
from apps.pages.models import Page
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponsePermanentRedirect, Http404

# Create your views here.
def getURLPicker(request):
    if request.is_ajax():
        action = request.POST.get('action', '')
        modules = Module.objects.filter(urlpicker=True, date_deleted=None, active=True)
        if action == '' or action == 'Page':
            pages = Page.objects.filter(date_deleted=None, active=True)

            context = {
                'page_active': True,
                'modules': modules,
                'items': pages,
                'current_module': 'Page'
            }
            data = {
                'template': render_to_string('urlpicker/urlpicker.html', context=context, request=request)
            }
            return JsonResponse(data)


def permaURL(request):
    
    module = request.GET.get('module')
    id = request.GET.get('id')

    if module == 'page':
        page = Page.objects.get(id=id)
        if not page:
            raise Http404
        else:
            if page.full_slug:
                url = page.full_slug 
            else:
                url = page.slug

            return HttpResponsePermanentRedirect('/' + request.LANGUAGE_CODE + '/' + url) 