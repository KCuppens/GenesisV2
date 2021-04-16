from django.shortcuts import render
from .export import Export
from apps.data.imp_ort import Import
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

# Create your views here.
def index_export_view(request):
    if request.method =="POST":
        checks = request.POST.getlist('export-check')
        names = request.POST.getlist('export')
        model = request.POST.get('model')
        field_list = Export.handle_form(checks, names, model)
        return Export.generate_xlsx(field_list, model)
        
    return render(request, 'data/export/index.html', {
        'models': Export.get_all_models
    })

def fields_overview(request):
    if request.is_ajax():
        data = {}
        model = request.GET.get('model', False)
        if model:
            fields = Export.get_all_fields_by_model(model)
            context = {
                'fields': fields,
                'model': model
            }
            data = {
                'template': render_to_string('data/export/fields.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

def index_import_view(request):
    if request.method == "POST":
        links = request.POST.getlist('links')
        value = request.POST.getlist('value')
    return render(request, 'data/import/index.html', {
        'models': Import.get_all_models
    })

def import_file_upload(request):
    if request.method == "POST":
        file = request.POST.get('importfile')
        model = request.POST.get('model')
        data = Import.get_headers_excel(file)
        fields = Import.get_all_fields_by_model(model)
        keydata = Import.get_first_data_row_excel(file)

        context = {
            'data': data,
            'keydata': keydata,
            'fields': fields,
            'model': model,
            'file': file
        }
        data = {
            'template': render_to_string('data/import/fields.html', context=context, request=request)
        }
        return JsonResponse(data)
    if request.method == "GET":
        model = request.GET.get('model', False)
        context = {
            'model': model
        }
        data = {
            'template': render_to_string('data/import/file-upload.html', context=context, request=request)
        }
        return JsonResponse(data)

def import_overview(request):
    if request.is_ajax():
        data = {}
        model = request.GET.get('model', False)
        if model:
            fields = Import.get_all_fields_by_model(model)
            context = {
                'fields': fields,
                'model': model
            }
            data = {
                'template': render_to_string('data/import/fields.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

def import_into_model(request):
    if request.method == "POST":
        value = request.POST.getlist('value')
        links = request.POST.getlist('links')
        file = request.POST.get('file')
        model = request.POST.get('model')
        required = Import.get_required_fields(model)
        links_without_language = []
        error = True
        for link in links:
            link = link.replace('_nl', '')
            link = link.replace('_fr', '')
            link = link.replace('_en', '')
            links_without_language.append(link)
        for req in required:
            if req in links_without_language:
                error = False
        
        if not error:
            excel = Import.get_excel_without_header(file)
            created_models = Import.model_importer(excel, value, links, model)

            message = _('Succesfully imported')
            context = {
                'message': message,
                'created_models': created_models
            }
            data = {
                'template': render_to_string('data/import/overview.html', context=context, request=request)
            }
            return JsonResponse(data)
        else:
            data = Import.get_headers_excel(file)
            fields = Import.get_all_fields_by_model(model)
            keydata = Import.get_first_data_row_excel(file)
            message = _('One of the required fields are missing') + ': ' + ''.join(required) 
            context = {
                'data': data,
                'keydata': keydata,
                'fields': fields,
                'model': model,
                'file': file,
                'message': message
            }
            data = {
                'template': render_to_string('data/import/fields.html', context=context, request=request)
            }
            return JsonResponse(data)
            

