from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from apps.base.utils import has_perms
from apps.pages.models import Page, Canvas, CanvasRow, PageBlock, DetailPage, PageBlockElement
from apps.blocks.models import Block, BlockCategory
from apps.pages.forms import PageForm, BlockForm, BlockElementForm
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render,get_object_or_404,redirect, reverse
from django.contrib import messages
from apps.pages.utils import generate_full_slug, generate_slug
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
import datetime
now = datetime.datetime.now()
@staff_member_required(login_url=reverse_lazy('login'))
def overview_page(request):
    has_perms(request, ["pages.view_page"], 'pages/index.html')

    search = request.GET.get('search')
    if search:
        pages = Page.objects.filter(Q(page_title__contains=search)| Q(menu_title__contains=search), date_deleted=None, parent__isnull=True)
    else:
        pages = Page.objects.filter(date_deleted=None, parent__isnull=True).order_by('position')

    
    return render(request,'pages/index.html', {"pages":pages, "search": search})

@staff_member_required(login_url=reverse_lazy('login'))
def overview_children_page(request, pk):
    has_perms(request, ["pages.view_page"], 'pages/index.html')
    page = Page.objects.get(pk=pk)
    if not page:
        return HttpResponseNotFound(_("Pagina niet gevonden"))
    pages = Page.objects.filter(parent=page, date_deleted=None)

    return render(request,'pages/children-index.html', {"pages":pages, "page": page})

@staff_member_required(login_url=reverse_lazy('login'))
def add_page(request):
    has_perms(request, ["pages.add_page"], None, 'overviewpage')
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.url_type == Page.URL_TYPE_GENERATED:
                generate_slug(instance)
            if not instance.url_type == Page.URL_TYPE_LINK_THROUGH:
                instance.full_slug = generate_full_slug(instance)
            instance.save()
            form.save_m2m()

            messages.add_message(request, messages.SUCCESS, _('The page has been succesfully added!'))

            return redirect('overviewpage')
    else:
        form = PageForm()

    return render(request, 'pages/add.html', {
        'form': form,
    })

@staff_member_required(login_url=reverse_lazy('login'))
def add_children_page(request, pk):
    has_perms(request, ["pages.add_page"], None, 'overviewpage')
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.url_type == Page.URL_TYPE_GENERATED:
                generate_slug(instance)
            if not instance.url_type == Page.URL_TYPE_LINK_THROUGH:
                instance.full_slug = generate_full_slug(instance)
            instance.save()

            messages.add_message(request, messages.SUCCESS, _('The page has been succesfully added!'))

            return redirect(reverse('overviewchildrenpage', kwargs={'pk': instance.parent.pk}))
    else:
        form = PageForm(
            initial= {
                'parent': pk
            }
        )

    return render(request, 'pages/add.html', {
        'form': form,
    })

@staff_member_required(login_url=reverse_lazy('login'))
def edit_page(request, pk):
    has_perms(request, ["pages.change_page"], None, 'overviewpage')
    instance = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        form = PageForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            generate_slug(instance)
            generate_full_slug(instance)
            instance.save()
            messages.add_message(request, messages.SUCCESS, _('The page has been succesfully changed!'))
            if instance.parent:
                return redirect(reverse('overviewchildrenpage', kwargs={'pk': instance.parent.pk}))
            return redirect('overviewpage')
    else:
        form = PageForm(instance=instance)

    return render(request, 'pages/edit.html', {
        'form': form,
        'page':instance
    })

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_mainmenu_activation_view(request, pk):
    has_perms(request, ["pages.change_page"], None, 'overviewpage')

    item = Page.objects.get(pk=pk)
    item.in_main_menu = not item.in_main_menu
    messages.add_message(request, messages.SUCCESS, _('De hoofdmenu status van de pagina is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewpage')

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_activation_view(request, pk):
    has_perms(request, ["pages.change_page"], None, 'overviewpage')

    item = Page.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de pagina is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewpage')

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_page_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        page = Page.objects.get(id=id)
        if page:
            context = {
                'page': page
            }
            data = {
                'template': render_to_string('pages/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_page(request,pk):
    has_perms(request, ["pages.delete_page"], None, 'overviewpage')
    instance = Page.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The page has been succesfully deleted!'))
    if instance.parent:
        return redirect(reverse('overviewchildrenpage', kwargs={'pk': instance.parent.pk}))
    return redirect('overviewpage')

@staff_member_required(login_url=reverse_lazy('login'))
def page_reorder(request):
    has_perms(request, ["pages.change_page"], None, 'overviewpage')
    items = request.POST.get('item', 'None')
    array = items.split('page[]=')
    ids = ''.join(array)
    ids = ids.split('&')
    position = 0

    for id in ids:
        if id.isnumeric():
            item = Page.objects.get(id=id)
            position += 1
            item.position = position
            item.save()
    

    return JsonResponse({}, status=200)



@staff_member_required(login_url=reverse_lazy('login'))
def canvas_page(request, pk):
    has_perms(request, ["pages.view_canvas"], 'overviewpage')
    page = Page.objects.get(pk=pk)
    return render(request,'canvas/index.html', {'page': page})

@staff_member_required(login_url=reverse_lazy('login'))
def canvas_detailpage(request, pk):
    has_perms(request, ["pages.view_canvas"], 'overviewpage')
    page = DetailPage.objects.get(pk=pk)

    return render(request,'canvas/detailpage-index.html', {'page': page})

@staff_member_required(login_url=reverse_lazy('login'))
def canvas_row(request):
    if request.is_ajax():
        canvas = request.POST.get('canvas', None)
        action = request.POST.get('action', None)
        row = request.POST.get('row', None)
        if canvas and action:
            canvas_obj = Canvas.objects.get(id=canvas)
            if action == 'add':
                canvas_obj.rows.add(CanvasRow.objects.create())
                canvas_obj.save()
            elif action == 'delete' and row:
                canvas_row = CanvasRow.objects.get(id=row)
                canvas_row.delete()
            elif action == "openmodal":
                page = int(request.GET.get('page', 1))
                detailpage = request.POST.get('detailpage', False)
                current_category = request.POST.get('category', None)
                if current_category and not current_category == 'alle':
                    category = BlockCategory.objects.filter(slug=current_category).first()
                search = request.POST.get('search', None)
                if search:
                    if not detailpage:
                        blocks = Block.objects.filter(detailpage_only=False, date_deleted=None, active=True, name__contains=search)
                    else:
                        blocks = Block.objects.filter(Q(detailpage_only=True)| Q(detailpage_only=False), date_deleted=None, active=True, name__contains=search)

                elif current_category == 'alle':
                    if not detailpage:
                        blocks = Block.objects.filter(detailpage_only=False, date_deleted=None, active=True)
                    else:
                        blocks = Block.objects.filter(Q(detailpage_only=True)| Q(detailpage_only=False), date_deleted=None, active=True)

                elif current_category:
                    if not detailpage:
                        blocks = Block.objects.filter(detailpage_only=False, date_deleted=None, active=True, category__id=category.id)
                    else:
                        blocks = Block.objects.filter(Q(detailpage_only=True)| Q(detailpage_only=False), date_deleted=None, active=True, category__id=category.id)

                elif search and current_category:
                    if not detailpage:
                        blocks = Block.objects.filter(detailpage_only=False, date_deleted=None, active=True, name__contains=search, category__id=category.id)
                    else:
                        blocks = Block.objects.filter(Q(detailpage_only=True)| Q(detailpage_only=False), date_deleted=None, active=True, name__contains=search, category__id=category.id)

                else:
                    if not detailpage:
                        blocks = Block.objects.filter(detailpage_only=False, date_deleted=None, active=True)
                    else:
                        blocks = Block.objects.filter(Q(detailpage_only=True)| Q(detailpage_only=False), date_deleted=None, active=True)

                categories = BlockCategory.objects.filter(date_deleted=None, active=True)
                paginator = Paginator(blocks, 12)
                has_next_page = False
                try:
                    blocks = paginator.page(page)
                except PageNotAnInteger:
                    blocks = paginator.page(1)
                except EmptyPage:
                    blocks = paginator.page(paginator.num_pages)

                if paginator.num_pages >= page:
                    has_next_page = True

                context = {
                    'blocks': blocks,
                    'categories': categories,
                    'canvas': canvas,
                    'row': row,
                    'current_category': current_category,
                    'search': search,
                    'has_next_page': has_next_page
                }
                data = {
                    'template': render_to_string('canvas/__partials/__blocks.html', context=context, request=request)
                }
                return JsonResponse(data)
            elif action == "addblock":
                item = request.POST.get('item', None)
                block = Block.objects.filter(id=item).first()
                row = CanvasRow.objects.filter(id=row).first()
                page_obj = Page.objects.filter(canvas=canvas_obj.id).first()
                page_block = PageBlock.objects.create(block=block, page=page_obj)
                row.block = page_block
                row.save()
            
        context = {
            'canvas': canvas_obj
        }
        data = {
            'template': render_to_string('canvas/__partials/__canvas_row.html', context=context, request=request)
        }
        return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def canvas_row_reorder(request):
    has_perms(request, ["pages.change_canvas"], 'overviewpage')
    items = request.POST.get('item', 'None')
    array = items.split('[]=')
    ids = ''.join(array)
    ids = ids.split('&')
    position = 0

    for id in ids:
        item = CanvasRow.objects.get(id=id)
        position += 1
        item.position = position
        item.save()
    

    return JsonResponse({}, status=200)

@staff_member_required(login_url=reverse_lazy('login'))
def content_block_view(request):
    block = request.POST.get('block', None)
    ajax = request.POST.get('ajax', None)
    action = request.POST.get('action', None)
    instance = PageBlock.objects.filter(id=block).first()
    if action == "createelement":
        element = PageBlockElement.objects.create()
        instance.block_elements.add(element)
        instance.save()
    if action == "saveelement":
        title = request.POST.get('title', '')
        image = request.POST.get('image', '')
        content = request.POST.get('content', '')
        subtitle = request.POST.get('subtitle', '')
        second_image = request.POST.get('second_image', '')
        block_elem = request.POST.get('block_elem')
        if block_elem:
            block_elem_obj = PageBlockElement.objects.filter(id=block_elem).first()
            if block_elem_obj:
                block_elem_obj.block_element_title = title 
                block_elem_obj.block_element_image = image 
                block_elem_obj.block_element_content = content 
                block_elem_obj.block_element_subtitle = subtitle
                block_elem_obj.block_element_image_second = second_image
                block_elem_obj.save()
    if action == 'deleteelement':
        block_elem = request.POST.get('block_elem')
        if block_elem:
            block_elem_obj = PageBlockElement.objects.filter(id=block_elem).first()
            if block_elem_obj:
                block_elem_obj.delete()
    if instance:
        if request.method == "POST" and not ajax:
            form = BlockForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.title = form.cleaned_data.get('title')
                instance.subtitle = form.cleaned_data.get('subtitle')
                instance.content = form.cleaned_data.get('content')
                instance.image = form.cleaned_data.get('image')
                instance.save()
                context = {
                    'message': _('Content succesfully changed'),
                    'form': form,
                    'block': block,
                    'instance': instance
                }
                data = {
                    'template': render_to_string('canvas/__partials/__content_form.html', context=context, request=request),
                    'success': True
                }
            else:
                context = {
                    'errors': form.errors,
                    'form': form,
                    'block': block,
                    'instance': instance
                }
                data = {
                    'template': render_to_string('canvas/__partials/__content_form.html', context=context, request=request),
                    'success': False
                }
        else:
            form = BlockForm(instance=instance)
            context = {
                'instance': instance,
                'form': form,
                'block': block,
                'instance': instance
            }
            data = {
                'template': render_to_string('canvas/__partials/__content_form.html', context=context, request=request),
                'success': False
            }
    return JsonResponse(data)

def open_preview(request, canvas):
    canvas = Canvas.objects.filter(id=canvas).first()
    return render(request, 'canvas/preview.html', {'canvas': canvas})

def detailpages_overview(request, pk):
    return render(request, 'detailpages/overview.html', {'pk': pk})

def get_detailpages(request):
    if request.is_ajax():
        pk = request.POST.get('pk')
        page_nr = request.POST.get('page', 1)
        page_obj = Page.objects.filter(id=pk).first()

        categories = page_obj.detailpage_models.split(',')
        category = request.POST.get('category', categories[0])
        default = DetailPage.objects.filter(model=category, default=True).first()
        detailpages = DetailPage.objects.filter(model=category, default=False).order_by('-id')

        has_next_page = False

        paginator = Paginator(detailpages, 12)
        try:
            pages = paginator.page(page_nr)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        
        if paginator.num_pages >= page_nr:
            has_next_page = True

        context = {
            'categories': categories,
            'current_category': category,
            'default': default,
            'detailpages': pages,
            'has_next_page': has_next_page,
            'pk': pk
        }
        data = {
            'template': render_to_string('detailpages/__partials/__overview.html', context=context, request=request),
        }
        return JsonResponse(data)