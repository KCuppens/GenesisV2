from django.shortcuts import render
from apps.modules.models import Module
from apps.pages.models import Page
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponsePermanentRedirect, Http404, HttpResponse
from apps.filemanager.models import Directory, Media
from apps.news.models import Article
from django.db.models import Q

# Create your views here.
def getURLPicker(request):
    if request.is_ajax():
        action = request.POST.get('action', '')
        modules = Module.objects.filter(urlpicker=True, date_deleted=None, active=True)
        if action == '' or action == 'Page':
            pages = Page.objects.filter(date_deleted=None, active=True)

            context = {
                'modules': modules,
                'items': pages,
                'current_module': 'Page'
            }
            data = {
                'template': render_to_string('urlpicker/urlpicker.html', context=context, request=request)
            }
            return JsonResponse(data)
        elif action == 'Article':
            articles = Article.objects.filter(date_deleted=None, active=True)
            context = {
                'modules': modules,
                'items': articles,
                'current_module': 'Article'
            }
            data = {
                'template': render_to_string('urlpicker/urlpicker.html', context=context, request=request)
            }
            return JsonResponse(data)


def get_filemanager(request):
    tinyMCE = request.GET.get('tinyMCE', None)
    if request.is_ajax() or tinyMCE:
        if request.method == "POST":
            mediatype = request.POST.get('type')
            selecttype = request.POST.get('selecttype')
            is_multiple_media_image = request.POST.get('is_multiple_media_image')
            target_elem_uuid = request.POST.get('target_elem_uuid')
        elif request.method == "GET":
            mediatype = request.GET.get('type')
            selecttype = request.GET.get('selecttype')
            is_multiple_media_image = request.GET.get('is_multiple_media_image')
            target_elem_uuid = None
        dir = request.GET.get('dir')
        search = request.GET.get('search')
        action = request.GET.get('action')
        if search:
            documents = Media.objects.filter(Q(name__contains=search)| Q(summary__contains=search), date_deleted=None, type=mediatype).order_by('-date_published')
            directories = Directory.objects.filter(Q(name__contains=search)| Q(summary__contains=search), date_deleted=None)
        elif dir and action == 'go-level-up' and not dir == "None":
            dir_obj = Directory.objects.filter(id=dir).first()
            parent = dir_obj.parent 
            if parent:
                dir = parent.id
            else:
                dir = None
            if parent:
                documents = Media.objects.filter(date_deleted=None, directory=parent, type=mediatype).order_by('-date_published')
                directories = Directory.objects.filter(date_deleted=None, parent=parent)
            else:
                documents = Media.objects.filter(date_deleted=None, directory__isnull=True, type=mediatype).order_by('-date_published')
                directories = Directory.objects.filter(date_deleted=None, parent__isnull=True)
        elif dir and not dir == "None":
            documents = Media.objects.filter(date_deleted=None, directory=dir, type=mediatype).order_by('-date_published')
            directories = Directory.objects.filter(date_deleted=None, parent=dir)
        else:
            documents = Media.objects.filter(date_deleted=None, directory__isnull=True, type=mediatype).order_by('-date_published')
            directories = Directory.objects.filter(date_deleted=None, parent__isnull=True)
        context = {
            'documents': documents,
            'directories': directories,
            'search': search,
            'current_type': mediatype,
            'current_dir': dir,
            'selecttype':selecttype,
            'is_multiple_media_image': is_multiple_media_image,
            'target_elem_uuid': target_elem_uuid,
            'tinyMCE': tinyMCE
        }
        data = {
            'template': render_to_string('filemanager/filemanager.html', context=context, request=request)
        }
        if tinyMCE:
            data = render_to_string('filemanager/filemanager.html', context=context, request=request)
            return HttpResponse(data)
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
    elif module == 'news':
        article = Article.objects.get(id=id)
        if not article:
            raise Http404
        else:
            return HttpResponsePermanentRedirect('/' + request.LANGUAGE_CODE + '/' + article.slug + '/' + article.pk)