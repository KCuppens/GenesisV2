from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.filemanager.models import (
    Directory, 
    Media, 
    Thumbnail,
    DirectoryRevision as ModelRevision1, 
    DirectoryVersion as ModelVersion1,
    MediaRevision as ModelRevision2,
    MediaVersion as ModelVersion2,
)
from apps.filemanager.forms import DirectoryForm, MediaForm, MediaFileForm
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from apps.base.utils import has_perms
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from apps.filemanager.utils import (
    guess_mime_type, 
    guess_media_type, 
    get_filename,
    attach_has_versions,
    attach_version_type
)
import json
# Create your views here.
@staff_member_required(login_url=reverse_lazy('login'))
def media_document_index_view(request):
    return render(request, 'media/index.html', {

    })

@staff_member_required(login_url=reverse_lazy('login'))
def get_media_overview(request):
    # import pdb; pdb.set_trace()
    if request.method == "GET":
        type = request.GET.get('type', None)
        dir = request.GET.get('dir')
        search = request.GET.get('search')
        action = request.GET.get('action')
        if search:
            documents = Media.objects.filter(Q(name__contains=search)| Q(filename__contains=search)| Q(summary__contains=search), date_deleted=None)
            directories = Directory.objects.filter(Q(name__contains=search)| Q(summary__contains=search), date_deleted=None)
        elif type == 'directories':
            documents = None 
            if dir:
                directories = Directory.objects.filter(date_deleted=None, parent=dir)
            else:
                directories = Directory.objects.filter(date_deleted=None, parent__isnull=True)
        elif type and not type == 'directories':
            if dir:
                documents = Media.objects.filter(date_deleted=None, directory=dir, type=type)
            else:
                # documents = Media.objects.filter(date_deleted=None, type=type, directory__isnull=True)
                documents = Media.objects.filter(date_deleted=None, type=type)
            directories = None
        elif dir and action == 'go-level-up' and not dir == "None":
            dir_obj = Directory.objects.filter(id=dir).first()
            parent = dir_obj.parent 
            if parent:
                dir = parent.id
            else:
                dir = None
            if parent:
                documents = Media.objects.filter(date_deleted=None, directory=parent)
                directories = Directory.objects.filter(date_deleted=None, parent=parent)
            else:
                documents = Media.objects.filter(date_deleted=None, directory__isnull=True)
                directories = Directory.objects.filter(date_deleted=None, parent__isnull=True)
        elif dir and not dir == "None":
            documents = Media.objects.filter(date_deleted=None, directory=dir)
            directories = Directory.objects.filter(date_deleted=None, parent=dir)
        else:
            documents = Media.objects.filter(date_deleted=None, directory__isnull=True)
            directories = Directory.objects.filter(date_deleted=None, parent__isnull=True)
        types = Media.GET_TYPES
        context = {
            'documents': attach_has_versions(documents, 'media'),
            'directories': attach_has_versions(directories, 'directory'),
            'types': types,
            'search': search,
            'current_type': type,
            'current_dir': dir,
        }
        data = {
            'template': render_to_string('media/__partials/__overview.html', context=context, request=request),
        }
        return JsonResponse(data)

    
@staff_member_required(login_url=reverse_lazy('login'))
def create_directory(request):
    if request.method == "POST":
        dir = request.POST.get('dir')
        if not str(dir) == "None":
            dir = Directory.objects.get(id=dir)
            form = DirectoryForm(request.POST, initial={'parent': dir})
        else:
            form = DirectoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            
            return redirect('media-document-index')
        else:
            if dir:
                form = DirectoryForm(request.POST, initial={'parent': dir})
            else:
                form = DirectoryForm(request.POST)
            context = {
                'form': form,
            }
            data = {
                'template': render_to_string('media/__partials/__create_directory.html', context=context, request=request),
                'title': _('Create directory')
            }
            return JsonResponse(data)
    else:
        dir = request.GET.get('dir')
        if not dir == "None":
            dir = Directory.objects.get(id=dir)
        
        form = DirectoryForm(request.POST, initial={'parent': dir})
        context = {
            'form': form,
        }
        data = {
            'template': render_to_string('media/__partials/__create_directory.html', context=context, request=request),
            'title': _('Create directory')
        }
        return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def edit_directory(request):
    if request.method == "POST":
        dir = request.POST.get('dir')
    elif request.method == "GET":
        dir = request.GET.get('dir')
    directory = Directory.objects.get(id=dir)
    if directory:
        if request.method == "POST":
            form = DirectoryForm(request.POST, instance=directory)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                
                return redirect('media-document-index')
            else:
                context = {
                    'form': form,
                    'dir': dir
                }
                data = {
                    'template': render_to_string('media/__partials/__edit_directory.html', context=context, request=request),
                    'title': _('Edit directory')
                }
                return JsonResponse(data)
        else:
            form = DirectoryForm(instance=directory)
            context = {
                'form': form,
                'dir': dir
            }
            data = {
                'template': render_to_string('media/__partials/__edit_directory.html', context=context, request=request),
                'title': _('Edit directory')
            }
            return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def delete_modal_directory(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('dir', False)
        directory = Directory.objects.get(id=id)
        if directory:
            context = {
                'directory': directory
            }
            data = {
                'template': render_to_string('media/__partials/__delete_directory_modal.html', context=context, request=request),
                'title': _('Delete directory')
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url=reverse_lazy('login'))
def delete_directory(request,pk):
    has_perms(request, ["filemanager.delete_directory"], None, 'overviewpage')
    instance = Directory.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The directory has been succesfully deleted!'))
    return redirect('media-document-index')

@staff_member_required(login_url=reverse_lazy('login'))
def create_media_type(request):
    if request.method == "GET":
        dir = request.GET.get('dir')
        filemanager = request.GET.get('filemanager')
        context = {
            'dir': dir,
        }
        data = {
            'template': render_to_string('media/__partials/__upload_media.html', context=context, request=request),
            'title': _('Upload media')
        }
        return JsonResponse(data)
    if request.method == "POST":
        dir = request.GET.get('dir', False)
        filemanager = request.GET.get('filemanager', False)
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            mimetype = guess_mime_type(instance.file.name)
            mediatype = guess_media_type(mimetype[0])
            instance.filename = get_filename(instance.file)
            instance.filesize = instance.file.size
            instance.type = mediatype
            if dir and not dir == "None":
                directory = Directory.objects.get(id=dir)
                instance.directory = directory
            instance.save()
            
            context = {
                'form': form,
                'dir': dir,
            }
            data = {
                'template': render_to_string('media/__partials/__upload_media.html', context=context, request=request),
                'title': _('Upload media')
            }
            return JsonResponse(data)
        else:
            context = {
                'form': form,
                'dir': dir,

            }
            data = {
                'template': render_to_string('media/__partials/__upload_media.html', context=context, request=request),
                'title': _('Upload media')
            }
            return JsonResponse(data)
    else:
        dir = request.GET.get('dir')
        form = MediaFileForm(instance=directory)
        context = {
            'form': form,
            'dir': dir,
        }
        data = {
            'template': render_to_string('media/__partials/__upload_media.html', context=context, request=request),
            'title': _('Upload media')
        }
        return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def edit_media(request):
    if request.method == "POST":
        media = request.POST.get('media')
    elif request.method == "GET":
        media = request.GET.get('media')
    media_obj = Media.objects.get(id=media)
    if media_obj:
        if request.method == "POST":
            form = MediaForm(request.POST, instance=media_obj)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                
                return redirect('media-document-index')
            else:
                context = {
                    'form': form,
                    'media': media,
                }
                data = {
                    'template': render_to_string('media/__partials/__edit_media.html', context=context, request=request),
                    'title': _('Edit media')
                }
                return JsonResponse(data)
        else:
            form = MediaForm(instance=media_obj)
            context = {
                'form': form,
                'media': media,
            }
            data = {
                'template': render_to_string('media/__partials/__edit_media.html', context=context, request=request),
                'title': _('Edit media')
            }
            return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def delete_modal_media(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('media', False)
        media = Media.objects.get(id=id)
        if media:
            context = {
                'media': media
            }
            data = {
                'template': render_to_string('media/__partials/__delete_media_modal.html', context=context, request=request),
                'title': _('Delete media')
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url=reverse_lazy('login'))
def delete_media(request,pk):
    has_perms(request, ["filemanager.delete_media"], None, 'overviewmedia')
    instance = Media.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    if instance.thumbnails.exists():
        for thumbnail in instance.thumbnails.all():
            thumbnail.date_deleted = timezone.now()
            thumbnail.save()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The media has been succesfully deleted!'))
    return redirect('media-document-index')       

@staff_member_required(login_url=reverse_lazy('login'))
def download_media(request, pk):
    media = Media.objects.get(id=pk)

    filename = media.file.name.split('/')[-1]
    response = HttpResponse(media.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@staff_member_required(login_url=reverse_lazy('login'))
def show_thumbnails(request):
    pk = request.GET.get('pk', False)
    media = Media.objects.get(id=pk)
    context = {
        'thumbnails': media.thumbnails.filter(date_deleted=None)
    }
    data = {
        'template': render_to_string('media/__partials/__thumbnails_overview.html', context=context, request=request),
        'title': _('Thumbnail overview')
    }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def delete_modal_thumbnail(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('thumbnail', False)
        thumbnail = Thumbnail.objects.get(id=id)
        if thumbnail:
            context = {
                'thumbnail': thumbnail
            }
            data = {
                'template': render_to_string('media/__partials/__delete_thumbnail_modal.html', context=context, request=request),
                'title': _('Delete thumbnail')
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url=reverse_lazy('login'))
def delete_thumbnail(request,pk):
    has_perms(request, ["filemanager.delete_thumbnail"], None, 'media-document-index')
    instance = Thumbnail.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The thumbnail has been succesfully deleted!'))
    return redirect('media-document-index')   


@staff_member_required(login_url=reverse_lazy('login'))
def get_version_ajax_modal(request, mode):
    data = {}
    # import pdb;pdb.set_trace();
    id = request.POST.get('id', False)
    if mode == 'directory':
        reversion = ModelRevision1.objects.get(current_instance=Directory.objects.get(id=id))
        versions = ModelVersion1.objects.filter(revision=reversion).order_by("date_created")
    else:
        reversion = ModelRevision2.objects.get(current_instance=Media.objects.get(id=id))
        versions = ModelVersion2.objects.filter(revision=reversion).order_by("date_created")
    if versions:
        context = {
            'versions': attach_version_type(versions, mode)
        }
        data = {
            'template': render_to_string('media/__partials/version_modal.html', context=context, request=request),
            'title': _('Versions')
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def get_delete_version_ajax_modal(request, mode):
    data = {}
    id = request.POST.get('id', False)
    try:
        if mode == 'directory':
            version = ModelVersion1.objects.get(id=id)
            version.mode = mode
        else:
            version = ModelVersion2.objects.get(id=id)
            version.mode = mode
    except Exception as e:
        print('Error: ', e)
        version = None
    if version:
        context = {
            'version': version
        }
        data = {
            'template': render_to_string('media/__partials/delete_version_modal.html', context=context, request=request)
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def select_version(request, mode, pk):
    if mode == 'directory':
        try:
            version = ModelVersion1.objects.get(id=pk)
            model_obj = ModelRevision1.objects.get(versions__id=pk).current_instance
        except Exception as e:
            messages.add_message(request, messages.WARNING, _(str(e)))
            return redirect('media-document-index')
    else:
        try:
            version = ModelVersion2.objects.get(id=pk)
            model_obj = ModelRevision2.objects.get(versions__id=pk).current_instance
        except Exception as e:
            messages.add_message(request, messages.WARNING, _(str(e)))
            return redirect('media-document-index')

    version_dict = json.loads(version.serialized_instance)
    for attr, value in version_dict.items():
        if attr == 'documents':
            model_obj.documents.set(value)
            continue
        if attr == 'thumbnails':
            model_obj.thumbnails.set(value)
            continue
        if attr == 'file' or attr == 'directory':
            continue
        setattr(model_obj, attr, value)
    model_obj.not_new_object=1
    model_obj.save()
    messages.add_message(request, messages.SUCCESS, _('Versie succesvol gewijzigd'))
    return redirect('media-document-index')

@staff_member_required(login_url=reverse_lazy('login'))
def delete_version(request, mode, pk):
    redirect_obj = redirect('media-document-index')

    try:
        if mode == 'directory':
            version = ModelVersion1.objects.get(id=pk)
        else:
            version = ModelVersion2.objects.get(id=pk)
    except Exception as e:
        messages.add_message(request, messages.WARNING, _(str(e)))
        return redirect_obj
    if version.is_current:
        # redirect if is_current=True
        messages.add_message(request, messages.WARNING, _('U kunt de momenteel geselecteerde versie niet verwijderen!'))
        return redirect_obj
    version.delete()
    messages.add_message(request, messages.SUCCESS, _('De versie is succesvol verwijderd'))
    return redirect_obj

@staff_member_required(login_url=reverse_lazy('login'))
def add_version_comment(request, mode, pk):
    # import pdb;pdb.set_trace();
    # if mode == 'template':
    #     redirect_obj = redirect('overviewmailtemplate')
    # else:
    #     redirect_obj = redirect('overviewmailconfig')

    redirect_obj = redirect('media-document-index')

    try:
        if mode == 'directory':
            version = ModelVersion1.objects.get(id=pk)
        else:
            version = ModelVersion2.objects.get(id=pk)
    except Exception as e:
        messages.add_message(request, messages.WARNING, _(str(e)))
        return redirect_obj
    comment = request.POST.get('comment')
    if comment and comment != version.comment:
        version.comment = comment
        version.save()
        messages.add_message(request, messages.SUCCESS, _('De opmerking is succesvol opgeslagen!'))
    return redirect_obj