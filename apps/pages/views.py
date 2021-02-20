from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from apps.base.utils import has_perms
from apps.pages.models import Page, Canvas, CanvasRow, CanvasColBlock, CanvasCol, PageBlock
from apps.blocks.models import Block, BlockCategory
from apps.pages.forms import PageForm, BlockForm
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from apps.pages.utils import generate_full_slug, generate_slug
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@staff_member_required(login_url='/account/login')
def overview_page(request):
    has_perms(request, ["pages.view_page"], 'pages/index.html')

    search = request.GET.get('search',)
    if search:
        pages = Page.objects.filter(Q(page_title__contains=search)| Q(menu_title__contains=search), date_deleted=None, parent__isnull=True)
    else:
        pages = Page.objects.filter(date_deleted=None, parent__isnull=True).order_by('position')

    
    return render(request,'pages/index.html', {"pages":pages, "search": None})

@staff_member_required(login_url='/account/login')
def overview_children_page(request, pk):
    has_perms(request, ["pages.view_page"], 'pages/index.html')
    page = Page.objects.get(pk=pk)
    if not page:
        return HttpResponseNotFound(_("Pagina niet gevonden"))
    pages = Page.objects.filter(parent=page, date_deleted=None)

    return render(request,'pages/children-index.html', {"pages":pages, "page": page})

@staff_member_required(login_url='/account/login')
def add_page(request):
    has_perms(request, ["pages.add_page"], None, 'overviewpage')
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            generate_slug(instance)
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

@staff_member_required(login_url='/account/login')
def add_children_page(request, pk):
    has_perms(request, ["pages.add_page"], None, 'overviewpage')
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            generate_slug(instance)
            instance.full_slug = generate_full_slug(instance)
            instance.save()

            messages.add_message(request, messages.SUCCESS, _('The page has been succesfully added!'))

            return redirect('overviewpage')
    else:
        form = PageForm(
            initial= {
                'parent': pk
            }
        )

    return render(request, 'pages/add.html', {
        'form': form,
    })

@staff_member_required(login_url='/account/login')
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

            return redirect('overviewpage')
    else:
        form = PageForm(instance=instance)

    return render(request, 'pages/edit.html', {
        'form': form,
        'page':instance
    })

@staff_member_required(login_url='/account/login')
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

        
@staff_member_required(login_url='/account/login')
def delete_page(request,pk):
    has_perms(request, ["pages.delete_page"], None, 'overviewpage')
    instance = Page.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The page has been succesfully deleted!'))
    return redirect('overviewpage')

@staff_member_required(login_url='/account/login')
def page_reorder(request):
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
            print(item.position)
    

    return JsonResponse({}, status=200)

@staff_member_required(login_url='/account/login')
def canvas_page(request, pk):
    has_perms(request, ["pages.view_canvas"], 'overviewpage')
    page = Page.objects.get(pk=pk)

    return render(request,'canvas/index.html', {'page': page})

@staff_member_required(login_url='/account/login')
def canvas_row(request):
    if request.is_ajax():
        canvas = request.POST.get('canvas', None)
        action = request.POST.get('action', None)
        row = request.POST.get('row', None)
        colblock = request.POST.get('colblock', None)
        if canvas and action:
            canvas_obj = Canvas.objects.get(id=canvas)
            if action == 'add':
                canvas_obj.rows.add(CanvasRow.objects.create())
                canvas_obj.save()
            elif action == 'delete' and row:
                canvas_row = CanvasRow.objects.get(id=row)
                if canvas_row.colblock:
                    if canvas_row.colblock.cols:
                        for col in canvas_row.colblock.cols.all():
                            col.delete()
                        canvas_row.colblock.delete()
                canvas_row.delete()
            elif action == 'addcolumn' and colblock:
                canvas_row = CanvasRow.objects.get(id=row)
                if colblock == "6-6":
                    col_1 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_6)
                    col_2 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_6)
                    colblock = CanvasColBlock.objects.create()
                    colblock.cols.add(col_1)
                    colblock.cols.add(col_2)
                    colblock.save()
                    canvas_row.colblock = colblock
                    canvas_row.save()
                elif colblock == "4-4-4":
                    col_1 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_4)
                    col_2 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_4)
                    col_3 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_4)
                    colblock = CanvasColBlock.objects.create()
                    colblock.cols.add(col_1)
                    colblock.cols.add(col_2)
                    colblock.cols.add(col_3)
                    colblock.save()
                    canvas_row.colblock = colblock
                    canvas_row.save()
                elif colblock == "3-3-3-3":
                    col_1 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_3)
                    col_2 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_3)
                    col_3 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_3)
                    col_4 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_3)
                    colblock = CanvasColBlock.objects.create()
                    colblock.cols.add(col_1)
                    colblock.cols.add(col_2)
                    colblock.cols.add(col_3)
                    colblock.cols.add(col_4)
                    colblock.save()
                    canvas_row.colblock = colblock
                    canvas_row.save()
                elif colblock == "8-4":
                    col_1 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_8)
                    col_2 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_4)
                    colblock = CanvasColBlock.objects.create()
                    colblock.cols.add(col_1)
                    colblock.cols.add(col_2)
                    colblock.save()
                    canvas_row.colblock = colblock
                    canvas_row.save()
                elif colblock == "4-8":
                    col_1 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_4)
                    col_2 = CanvasCol.objects.create(col_size=CanvasCol.TYPE_COL_8)
                    colblock = CanvasColBlock.objects.create()
                    colblock.cols.add(col_1)
                    colblock.cols.add(col_2)
                    colblock.save()
                    canvas_row.colblock = colblock
                    canvas_row.save()
            elif action == "openmodal":
                colsize = request.POST.get('colsize', None)
                col = request.POST.get('col', None)
                page = request.GET.get('page', 1)
                current_category = request.POST.get('category', None)
                if current_category and not current_category == 'alle':
                    category = BlockCategory.objects.filter(slug=current_category).first()
                search = request.POST.get('search', None)
                if search:
                    blocks = Block.objects.filter(col_size=colsize, date_deleted=None, active=True, name__contains=search)
                elif current_category == 'alle':
                    blocks = Block.objects.filter(col_size=colsize, date_deleted=None, active=True)
                elif current_category:
                    blocks = Block.objects.filter(col_size=colsize, date_deleted=None, active=True, category__id=category.id)
                elif search and current_category:
                    blocks = Block.objects.filter(col_size=colsize, date_deleted=None, active=True, name__contains=search, category__id=category.id)
                else:
                    blocks = Block.objects.filter(col_size=colsize, date_deleted=None, active=True)
                categories = BlockCategory.objects.filter(date_deleted=None, active=True)

                paginator = Paginator(blocks, 12)

                try:
                    blocks = paginator.page(page)
                except PageNotAnInteger:
                    blocks = paginator.page(1)
                except EmptyPage:
                    blocks = paginator.page(paginator.num_pages)
                context = {
                    'col': col,
                    'blocks': blocks,
                    'categories': categories,
                    'canvas': canvas,
                    'current_category': current_category,
                    'colsize': colsize,
                    'search': search
                }
                data = {
                    'template': render_to_string('canvas/__partials/__blocks.html', context=context, request=request)
                }
                return JsonResponse(data)
            elif action == "addblock":
                col = request.POST.get('col', None)
                item = request.POST.get('item', None)
                block = Block.objects.filter(id=item).first()
                col = CanvasCol.objects.filter(id=col).first()
                page_block = PageBlock.objects.create(block=block)
                col.block = page_block
                col.save()
            
        context = {
            'canvas': canvas_obj
        }
        data = {
            'template': render_to_string('canvas/__partials/__canvas_row.html', context=context, request=request)
        }
        return JsonResponse(data)

@staff_member_required(login_url='/account/login')
def content_block_view(request):
    block = request.POST.get('block', None)
    instance = PageBlock.objects.filter(id=block).first()
    print(instance)
    if instance:
        if request.method == "POST":
            form = BlockForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                print(form.cleaned_data)
                instance = form.save(commit=False)
                instance.title = form.cleaned_data.get('title')
                instance.subtitle = form.cleaned_data.get('subtitle')
                instance.content = form.cleaned_data.get('content')
                instance.image = form.cleaned_data.get('image')
                instance.save()
                print(instance)
                print(instance.title)
                context = {
                    'message': _('Content succesfully changed'),
                    'form': form,
                    'block': block
                }
                data = {
                    'template': render_to_string('canvas/__partials/__content_form.html', context=context, request=request)
                }
                return JsonResponse(data)
            else:
                context = {
                    'errors': form.errors,
                    'form': form,
                    'block': block
                }
                data = {
                    'template': render_to_string('canvas/__partials/__content_form.html', context=context, request=request)
                }
                return JsonResponse(data)
        else:
            form = Blockform(instance=instance)
            context = {
                'instance': instance,
                'form': form,
                'block': block
            }
            data = {
                'template': render_to_string('canvas/__partials/__content_form.html', context=context, request=request),
            }
            return JsonResponse(data)
    data = {}
    return JsonResponse(data)
