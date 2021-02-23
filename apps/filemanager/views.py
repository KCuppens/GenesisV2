from django.shortcuts import render
from apps.filemanager.models import Directory, Media
# Create your views here.
def media_document_index_view(request):
    directory_id = request.GET.get('directory_id', False)
    if directory_id:
        current_directory = Directory.objects.filter(id=directory_id).first()
    else:
        current_directory = False
    documents = Media.objects.filter(id=directory_id)
    directories = Directory.objects.filter(id=directory_id)
    types = Directory.GET_TYPES

    return render(request, 'media/index.html', {
        'documents': documents,
        'directories': directories,
        'current_directory': current_directory,
        'types': types
    })