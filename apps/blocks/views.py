from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
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
from apps.blocks.models import (
    Block, 
    BlockCategory,
    BlocksRevision as ModelRevision,
    BlocksVersion as ModelVersion
)
from apps.blocks.forms import BlockForm, BlockCategoryForm
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.db import transaction
import json


@staff_member_required(login_url=reverse_lazy('login'))
def overview_block(request):
    blocks = Block.objects.filter(date_deleted=None)
    has_perms(request, ["blocks.view_block"], None, 'dashboard')
    for block in blocks:
        try:
            revision = ModelRevision.objects.get(current_instance=block)
            versions = revision.versions.all()
            block.has_versions = bool(versions)
        except:
            continue
    
    return render(request,'blocks/index.html', {"blocks":blocks})

@staff_member_required(login_url=reverse_lazy('login'))
@transaction.atomic
def add_block(request):
    has_perms(request, ["blocks.add_block"], None, 'overviewblocks')
    if request.method == 'POST':
        form = BlockForm(request.POST, request.FILES)
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

@staff_member_required(login_url=reverse_lazy('login'))
@transaction.atomic
def edit_block(request, pk):
    # import pdb; pdb.set_trace()
    has_perms(request, ["blocks.change_block"], None, 'overviewblocks')
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

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_activation_view(request, pk):
    has_perms(request, ["blocks.change_block"], None, 'overviewblocks')

    item = Block.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de tab is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewblocks')

@staff_member_required(login_url=reverse_lazy('login'))
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

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_block(request,pk):
    has_perms(request, ["blocks.delete_block"], None, 'overviewblock')
    instance = Block.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The block has been succesfully deleted!'))
    return redirect('overviewblocks')


@staff_member_required(login_url=reverse_lazy('login'))
def overview_blockcategories(request):
    categories = BlockCategory.objects.filter(date_deleted=None)
    has_perms(request, ["blocks.add_blockcategory"], 'blocks/index.html')
    
    return render(request,'blockcategory/index.html', {"categories":categories})

@staff_member_required(login_url=reverse_lazy('login'))
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

@staff_member_required(login_url=reverse_lazy('login'))
def edit_block_category(request, pk):
    has_perms(request, ["blocks.change_blockcategory"], None, 'overviewblocks')
    instance = get_object_or_404(Block, pk=pk)
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

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_category_activation_view(request, pk):
    has_perms(request, ["blocks.change_blockcategory"], None, 'overviewblock-categories')

    item = BlockCategory.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de categorie is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewblock-categories')

@staff_member_required(login_url=reverse_lazy('login'))
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

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_blockcategory(request,pk):
    has_perms(request, ["blocks.delete_blockcategory"], None, 'overviewblock-categories')
    instance = BlockCategory.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The block category has been succesfully deleted!'))
    return redirect('overviewblock-categories')

@staff_member_required(login_url=reverse_lazy('login'))
def overview_reversion(request):
    blocks = Block.objects.filter(date_deleted__isnull=False)
    return render(request,'blocks/reversion-overview-index.html', {"blocks": blocks})

@staff_member_required(login_url=reverse_lazy('login'))
def revert_block(request, pk):
    try:
        block = Block.objects.get(id=pk)
        block.date_deleted = None
        block.save()
        messages.add_message(request, messages.SUCCESS, _('The Block has been succesfully reverted!'))
    except:
        messages.add_message(request, messages.WARNING, _('No such Block is available!'))
    
    return redirect('overviewreversionblock')

@staff_member_required(login_url=reverse_lazy('login'))
def get_version_ajax_modal(request):
    data = {}
    # import pdb;pdb.set_trace();
    id = request.POST.get('id', False)
    reversion = ModelRevision.objects.get(current_instance=Block.objects.get(id=id))
    versions = ModelVersion.objects.filter(revision=reversion).order_by("date_created")
    if versions:
        context = {
            'versions': versions
        }
        data = {
            'template': render_to_string('blocks/__partials/version_modal.html', context=context, request=request)
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def get_delete_version_ajax_modal(request):
    data = {}
    # import pdb;pdb.set_trace();
    id = request.POST.get('id', False)
    try:
        version = ModelVersion.objects.get(id=id)
    except:
        version = None
    if version:
        context = {
            'version': version
        }
        data = {
            'template': render_to_string('blocks/__partials/delete_version_modal.html', context=context, request=request)
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def select_version(request, pk):
    # import pdb;pdb.set_trace();
    version = ModelVersion.objects.get(id=pk)
    # article_version.is_current = True
    # article_version.save()

    version_dict = json.loads(version.serialized_instance)
    model_obj = ModelRevision.objects.get(versions__id=pk).current_instance
    for attr, value in version_dict.items():
        if attr == 'category':
            model_obj.category.set(value)
            continue
        setattr(model_obj, attr, value)
    model_obj.not_new_object=1
    model_obj.save()
    messages.add_message(request, messages.SUCCESS, _('Versie succesvol gewijzigd'))
    return redirect('overviewblocks')

@staff_member_required(login_url=reverse_lazy('login'))
def delete_version(request, pk):
    # import pdb;pdb.set_trace();
    version = ModelVersion.objects.get(id=pk)
    if version.is_current:
        # redirect if is_current=True
        messages.add_message(request, messages.WARNING, _('U kunt de momenteel geselecteerde versie niet verwijderen!'))
        return redirect('overviewblocks')
    version.delete()
    messages.add_message(request, messages.SUCCESS, _('De versie is succesvol verwijderd'))
    return redirect('overviewblocks')

@staff_member_required(login_url=reverse_lazy('login'))
def add_version_comment(request, pk):
    # import pdb;pdb.set_trace();
    version = ModelVersion.objects.get(id=pk)
    comment = request.POST.get('comment')
    if comment and comment != version.comment:
        version.comment = comment
        version.save()
        messages.add_message(request, messages.SUCCESS, _('De opmerking is succesvol opgeslagen!'))
    return redirect('overviewblocks')
