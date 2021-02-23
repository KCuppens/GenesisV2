from django.shortcuts import render,get_object_or_404,redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, resolve_url
from apps.conf.utils import get_config
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from apps.base.utils import has_perms
from apps.blocks.models import Block, BlockCategory
from apps.blocks.forms import BlockForm, BlockCategoryForm
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory


@staff_member_required(login_url='/nl/account/login')
def overview_block(request):
    blocks = Block.objects.filter(date_deleted=None)
    has_perms(request, ["blocks.add_block"], 'blocks/index.html')
    
    return render(request,'blocks/index.html', {"blocks":blocks})

@staff_member_required(login_url='/nl/account/login')
def add_block(request):
    has_perms(request, ["blocks.add_block"], None, 'overviewblock')
    if request.method == 'POST':
        form = BlockForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The block has been succesfully added!'))
            return redirect('overviewblocks')
    else:
        form = BlockForm()

    return render(request, 'blocks/add.html', {
        'form': form,
    })

@staff_member_required(login_url='/nl/account/login')
def edit_block(request, pk):
    has_perms(request, ["blocks.change_block"], None, 'overviewblock')
    instance = get_object_or_404(Block, pk=pk)
    if request.method == 'POST':
        form = BlockForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The block has been succesfully changed!'))

            return redirect('overviewblocks')
    else:
        form = BlockForm(instance=instance)

    return render(request, 'blocks/edit.html', {
        'form': form,
        'item': instance
    })

@staff_member_required(login_url='/nl/account/login')
def toggle_activation_view(request, pk):
    has_perms(request, ["blocks.change_block"], None, 'overviewblocks')

    item = Block.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de tab is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewblocks')

@staff_member_required(login_url='/nl/account/login')
def delete_ajax_block_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        block = Block.objects.get(id=id)
        if block:
            context = {
                'block': block
            }
            data = {
                'template': render_to_string('blocks/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

        
@staff_member_required(login_url='/nl/account/login')
def delete_block(request,pk):
    has_perms(request, ["blocks.delete_block"], None, 'overviewblock')
    instance = Block.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The block has been succesfully deleted!'))
    return redirect('overviewblocks')


@staff_member_required(login_url='/nl/account/login')
def overview_blockcategories(request):
    categories = BlockCategory.objects.filter(date_deleted=None)
    has_perms(request, ["blocks.add_blockcategory"], 'blocks/index.html')
    
    return render(request,'blockcategory/index.html', {"categories":categories})

@staff_member_required(login_url='/nl/account/login')
def add_block_category(request):
    has_perms(request, ["blocks.add_blockcategory"], None, 'overviewblocks')
    if request.method == 'POST':
        form = BlockCategoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS, _('The block category has been succesfully added!'))
            return redirect('overviewblock-categories')
    else:
        form = BlockCategoryForm()

    return render(request, 'blockcategory/add.html', {
        'form': form,
    })

@staff_member_required(login_url='/nl/account/login')
def edit_block_category(request, pk):
    has_perms(request, ["blocks.change_blockcategory"], None, 'overviewblocks')
    instance = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        form = BlockCategoryForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS, _('The blockcategory has been succesfully changed!'))
            return redirect('overviewblock-categories')
    else:
        form = BlockCategoryForm(instance=instance)

    return render(request, 'blockcategory/edit.html', {
        'form': form,
        'item': instance,
    })

@staff_member_required(login_url='/nl/account/login')
def toggle_category_activation_view(request, pk):
    has_perms(request, ["blocks.change_blockcategory"], None, 'overviewblock-categories')

    item = BlockCategory.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de categorie is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewblock-categories')

@staff_member_required(login_url='/nl/account/login')
def delete_ajax_block_category_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        blockcategory = BlockCategory.objects.get(id=id)
        if blockcategory:
            context = {
                'blockcategory': blockcategory
            }
            data = {
                'template': render_to_string('blockcategory/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

        
@staff_member_required(login_url='/nl/account/login')
def delete_blockcategory(request,pk):
    has_perms(request, ["blocks.delete_blockcategory"], None, 'overviewblock-categories')
    instance = BlockCategory.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The block category has been succesfully deleted!'))
    return redirect('overviewblock-categories')


