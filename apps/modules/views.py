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
from apps.modules.models import Tab, Module, ModulePage
from apps.modules.forms import TabForm, ModuleForm, ModulePageForm
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site

@staff_member_required(login_url='/account/login')
def overview_tab(request):
    tabs = Tab.objects.filter(date_deleted=None)
    has_perms(request, ["modules.add_tab"], 'tabs/index.html')
    
    return render(request,'tabs/index.html', {"tabs":tabs})

@staff_member_required(login_url='/account/login')
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

@staff_member_required(login_url='/account/login')
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

@staff_member_required(login_url='/account/login')
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

        
@staff_member_required(login_url='/account/login')
def delete_tab(request,pk):
    has_perms(request, ["modules.delete_tab"], None, 'overviewtab')
    instance = Tab.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
    return redirect('overviewtab')


@staff_member_required(login_url='/account/login')
def overview_modules(request):
    modules = Module.objects.filter(date_deleted=None)
    has_perms(request, ["modules.add_module"], 'modules/index.html')
    
    return render(request,'modules/index.html', {"modules":modules})

@staff_member_required(login_url='/account/login')
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
            form = formset.cleaned_data[0]
            route = form['route']
            show_nav = form['show_nav']
            name = form['name']
            page = ModulePage(module=instance, route=route, show_nav=show_nav, name=name)
            page.save()
            return redirect('overviewmodules')
    else:
        form = ModuleForm()
        formset = ModulePageFormSet(queryset=ModulePage.objects.none())

    return render(request, 'modules/add.html', {
        'form': form,
        'formset': formset,
    })

@staff_member_required(login_url='/account/login')
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

@staff_member_required(login_url='/account/login')
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

        
@staff_member_required(login_url='/account/login')
def delete_modules(request,pk):
    has_perms(request, ["modules.delete_module"], None, 'overviewmodules')
    instance = Module.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
    return redirect('overviewmodules')

@staff_member_required(login_url='/account/login')
def delete_modules_page(request,pk):
    has_perms(request, ["modules.delete_modulepage"], None, 'overviewmodules')
    instance = ModulePage.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The modulepage has been succesfully deleted!'))
    return redirect('overviewmodules')
