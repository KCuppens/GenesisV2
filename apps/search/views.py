from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from apps.pages.models import Page 
from apps.user.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def search_admin_view(request):
    modules = {
        'Page': {
            'type': 'page',
            'title': _('Pagina\'s'),
            'model': 'Page'
        },
        'User': {
            'type': 'user',
            'title': _('Gebruikers'),
            'model': 'User'
        }
    }

    search = request.GET.get('search')
    type =  request.GET.get('type', 'all')
    items = []
    categories = {'all': 0}
    paginator = False 
    error_message = False 
    results = None
    if len(search) < 3:
        error_message = _('Gelieve minstens 3 karakters te gebruiken')
    else:
        page = request.GET.get('page')
        show_per_page = 25
        for entity, module in modules.items():
            if module['model'] == "Page":
                results = eval(module['model']).objects.filter(Q(page_title__contains=search)| Q(menu_title__contains=search), date_deleted=None)
            elif module['model'] == "User":
                results = eval(module['model']).objects.filter(Q(first_name__contains=search)| Q(last_name__contains=search) | Q(email__contains=search),date_deleted=None)

            if not entity in categories:
                categories[entity] = 0

            categories[entity] += len(results)
            if not type == 'all':
                if type == module['type']:
                    for result in results:
                        items.append(result)
            else:
                for result in results:
                    items.append(result)
                    
        categories['all'] = sum(categories.values())

        total_count = len(items)
        if total_count > show_per_page:
            items = items[(page - 1) * show_per_page: show_per_page]

        paginator = Paginator(items, show_per_page)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        
    return render(request, 'search/admin/index.html', {
        'modules': modules,
        'categories': categories.items(),
        'results': results,
        'error_message': error_message,
        'search': search,
        'type': type,
    })

def search_front_view(request):
    modules = {
        'Page': {
            'type': 'page',
            'title': _('Pagina\'s'),
            'model': 'Page'
        },
    }

    search = request.GET.get('search')
    type =  request.GET.get('type', 'all')
    items = []
    categories = {'all': 0}
    paginator = False 
    error_message = False 
    results = None
    if len(search) < 3:
        error_message = _('Gelieve minstens 3 karakters te gebruiken')
    else:
        page = request.GET.get('page')
        show_per_page = 25
        for entity, module in modules.items():
            if module['model'] == "Page":
                results = eval(module['model']).objects.filter(Q(page_title__contains=search)| Q(menu_title__contains=search), date_deleted=None)

            if not entity in categories:
                categories[entity] = 0

            categories[entity] += len(results)
            if not type == 'all':
                if type == module['type']:
                    for result in results:
                        items.append(result)
            else:
                for result in results:
                    items.append(result)
                    
        categories['all'] = sum(categories.values())

        total_count = len(items)
        if total_count > show_per_page:
            items = items[(page - 1) * show_per_page: show_per_page]

        paginator = Paginator(items, show_per_page)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        
    return render(request, 'search/front/index.html', {
        'modules': modules,
        'categories': categories.items(),
        'results': results,
        'error_message': error_message,
        'search': search,
        'type': type,
    })
