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
from apps.feathericons.models import Icon
from apps.modules.models import (
    Tab, 
    Module, 
    ModulePage,
    ModuleRevision as ModelRevision1,
    ModuleVersion as ModelVersion1,
    TabRevision as ModelRevision2,
    TabVersion as ModelVersion2
)
from apps.modules.forms import TabForm, ModuleForm, ModulePageForm
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.db import transaction
import json

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site

@staff_member_required(login_url=reverse_lazy('login'))
def overview_tab(request):
    has_perms(request, ["modules.view_tab"], None, 'overviewtab')
    tabs = Tab.objects.filter(date_deleted=None).order_by('position')

    for tab in tabs:
        try:
            revision = ModelRevision2.objects.get(current_instance=tab)
            versions = revision.versions.all()
            tab.has_versions = bool(versions)
        except:
            continue
    return render(request,'tabs/index.html', {"tabs":tabs})

@staff_member_required(login_url=reverse_lazy('login'))
@transaction.atomic
def add_tab(request):
    has_perms(request, ["modules.add_tab"], None, 'overviewtab')
    if request.method == 'POST':
        form = TabForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()

            messages.add_message(request, messages.SUCCESS, _('The tab has been succesfully added!'))

            return redirect('overviewtab')
    else:
        form = TabForm()

    return render(request, 'tabs/add.html', {
        'form': form,
    })

@staff_member_required(login_url=reverse_lazy('login'))
@transaction.atomic
def edit_tab(request, pk):
    has_perms(request, ["modules.change_tab"], None, 'overviewtab')
    instance = get_object_or_404(Tab, pk=pk)
    if request.method == 'POST':
        form = TabForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The tab has been succesfully changed!'))

            return redirect('overviewtab')
    else:
        form = TabForm(instance=instance)

    return render(request, 'tabs/edit.html', {
        'form': form,
        'tab':instance
    })

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_tab_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        tab = Tab.objects.get(id=id)
        if tab:
            context = {
                'tab': tab
            }
            data = {
                'template': render_to_string('tabs/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_tab_activation_view(request, pk):
    has_perms(request, ["modules.change_tab"], None, 'overviewtab')

    item = Tab.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de tab is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewtab')

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_tab(request,pk):
    has_perms(request, ["modules.delete_tab"], None, 'overviewtab')
    instance = Tab.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
    return redirect('overviewtab')

def reorder_tab(request):
    has_perms(request, ["modules.change_tab"], None, 'overviewtab')

    items = request.POST.get('item', 'None')
    array = items.split('[]=')
    ids = ''.join(array)
    ids = ids.split('&')
    position = 0 

    for id in ids:
        item = Tab.objects.get(id=id)
        position += 1
        item.position = position 
        item.save()
    data = {

    }
    return JsonResponse(data)


@staff_member_required(login_url=reverse_lazy('login'))
def overview_modules(request):
    has_perms(request, ["modules.view_module"], 'modules/index.html')
    modules = Module.objects.filter(date_deleted=None).order_by('position')
    for module in modules:
        try:
            revision = ModelRevision1.objects.get(current_instance=module)
            versions = revision.versions.all()
            module.has_versions = bool(versions)
        except:
            continue
    return render(request,'modules/index.html', {"modules":modules})

@staff_member_required(login_url=reverse_lazy('login'))
@transaction.atomic
def add_modules(request):
    has_perms(request, ["modules.add_module"], None, 'overviewmodules')
    ModulePageFormSet = modelformset_factory(ModulePage, form=ModulePageForm)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        formset = ModulePageFormSet(request.POST, request.FILES, queryset=ModulePage.objects.none())
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The module has been succesfully added!'))
            for form in formset.cleaned_data:
                try:
                    route = form['route']
                    show_nav = form['show_nav']
                    name = form['name']
                    page = ModulePage(module=instance, route=route, show_nav=show_nav, name=name)
                    page.save()
                except Exception as e:
                    break
            return redirect('overviewmodules')
    else:
        form = ModuleForm()
        formset = ModulePageFormSet(queryset=ModulePage.objects.none())

    return render(request, 'modules/add.html', {
        'form': form,
        'formset': formset,
    })

@staff_member_required(login_url=reverse_lazy('login'))
@transaction.atomic
def edit_modules(request, pk):
    has_perms(request, ["modules.change_module"], None, 'overviewmodules')
    instance = get_object_or_404(Module, pk=pk)
    ModulePageFormSet = modelformset_factory(ModulePage, form=ModulePageForm)
    modulesPages = ModulePage.objects.filter(module=instance, date_deleted=None)
    if request.method == 'POST':
        form = ModuleForm(request.POST or request.FILES,instance=instance)
        formset = ModulePageFormSet(request.POST, request.FILES, queryset=ModulePage.objects.none())
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The module has been succesfully changed!'))
            for form in formset.cleaned_data:
                try:
                    route = form['route']
                    show_nav = form['show_nav']
                    name = form['name']
                    page = ModulePage(module=instance, route=route, show_nav=show_nav, name=name)
                    page.save()
                except Exception as e:
                    break
            return redirect('overviewmodules')
    else:
        form = ModuleForm(instance=instance)
        formset = ModulePageFormSet(queryset=ModulePage.objects.none())

    return render(request, 'modules/edit.html', {
        'form': form,
        'module':instance,
        'formset': formset,
        'modulesPages': modulesPages
    })

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_modules_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        module = Module.objects.get(id=id)
        if module:
            context = {
                'module': module
            }
            data = {
                'template': render_to_string('modules/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_modules(request,pk):
    has_perms(request, ["modules.delete_module"], None, 'overviewmodules')
    instance = Module.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
    return redirect('overviewmodules')

@staff_member_required(login_url=reverse_lazy('login'))
def delete_modules_page(request,pk):
    has_perms(request, ["modules.delete_modulepage"], None, 'overviewmodules')
    instance = ModulePage.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The modulepage has been succesfully deleted!'))
    return redirect('overviewmodules')

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_activation_view(request, pk):
    has_perms(request, ["modules.change_module"], None, 'overviewmodules')

    item = Module.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de gebruiker is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewmodules')

def reorder_module(request):
    has_perms(request, ["modules.change_module"], None, 'overviewmodules')
    items = request.POST.get('item', 'None')
    array = items.split('[]=')
    ids = ''.join(array)
    ids = ids.split('&')
    position = 0 

    for id in ids:
        item = Module.objects.get(id=id)
        position += 1
        item.position = position 
        item.save()
    data = {

    }
    return JsonResponse(data)


@staff_member_required(login_url=reverse_lazy('login'))
def get_version_ajax_modal(request, mode):
    data = {}
    # import pdb;pdb.set_trace();
    id = request.POST.get('id', False)
    if mode == 'module':
        reversion = ModelRevision1.objects.get(current_instance=Module.objects.get(id=id))
        versions = ModelVersion1.objects.filter(revision=reversion).order_by("date_created")
        template_path = 'modules/__partials/version_modal.html'
    else:
        reversion = ModelRevision2.objects.get(current_instance=Tab.objects.get(id=id))
        versions = ModelVersion2.objects.filter(revision=reversion).order_by("date_created")
        template_path = 'tabs/__partials/version_modal.html'
    if versions:
        context = {
            'versions': versions
        }
        data = {
            'template': render_to_string(template_path, context=context, request=request)
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def get_delete_version_ajax_modal(request, mode):
    data = {}
    # import pdb;pdb.set_trace();
    id = request.POST.get('id', False)
    try:
        if mode == 'module':
            version = ModelVersion1.objects.get(id=id)
            template_path = 'modules/__partials/delete_version_modal.html'
        else:
            version = ModelVersion2.objects.get(id=id)
            template_path = 'tabs/__partials/delete_version_modal.html'
    except Exception as e:
        print('Error: ', e)
        version = None
    if version:
        context = {
            'version': version
        }
        data = {
            'template': render_to_string(template_path, context=context, request=request)
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def select_version(request, mode, pk):
    # import pdb;pdb.set_trace();
    if mode == 'module':
        redirect_obj = redirect('overviewmodules')
    else:
        redirect_obj = redirect('overviewtab')

    if mode == 'module':
        try:
            version = ModelVersion1.objects.get(id=pk)
            model_obj = ModelRevision1.objects.get(versions__id=pk).current_instance
        except Exception as e:
            messages.add_message(request, messages.WARNING, _(str(e)))
            return redirect_obj
    else:
        try:
            version = ModelVersion2.objects.get(id=pk)
            model_obj = ModelRevision2.objects.get(versions__id=pk).current_instance
        except Exception as e:
            messages.add_message(request, messages.WARNING, _(str(e)))
            return redirect_obj

    version_dict = json.loads(version.serialized_instance)
    for attr, value in version_dict.items():
        if attr == 'attachments':
            model_obj.attachments.set(value)
            continue
        if attr == 'modules':
            model_obj.modules.set(value)
            continue
        if attr == 'icon':
            try:
                model_obj.icon = Icon.objects.get(id=value)
            except:
                pass
            continue
        setattr(model_obj, attr, value)
    model_obj.not_new_object=1
    model_obj.save()
    messages.add_message(request, messages.SUCCESS, _('Versie succesvol gewijzigd'))
    return redirect_obj

@staff_member_required(login_url=reverse_lazy('login'))
def delete_version(request, mode, pk):
    # import pdb;pdb.set_trace();
    if mode == 'module':
        redirect_obj = redirect('overviewmodules')
    else:
        redirect_obj = redirect('overviewtab')

    try:
        if mode == 'module':
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
    if mode == 'module':
        redirect_obj = redirect('overviewmodules')
    else:
        redirect_obj = redirect('overviewtab')

    try:
        if mode == 'module':
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