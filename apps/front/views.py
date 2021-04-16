from django.shortcuts import render, get_object_or_404
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

def page_view(request, slug):
    pages = Page.objects.filter(date_deleted=None, active=True)
    if slug == '':
        page = Page.objects.filter(slug=slug, active=True, date_deleted=None).first()
    else:
        page = Page.objects.filter(full_slug=slug, active=True, date_deleted=None).first()
    template_name = None
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
    object = eval(model.capitalize()).objects.filter(slug=slug).first()
    detailpage = DetailPage.objects.filter(pk=pk).first()
    if not object or not detailpage:
        raise Http404(_('Detailpagina bestaat niet'))

    return render(request, 'front/detail.html', {'object': object, 'detailpage': detailpage})

