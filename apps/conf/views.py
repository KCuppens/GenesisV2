from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required
from apps.base.utils import has_perms
from django.contrib import messages
from apps.conf.models import Configuration
from apps.conf.forms import ConfigurationForm
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.

@staff_member_required(login_url=reverse_lazy('login'))
def overview_conf(request):
    conf = Configuration.objects.filter()
    has_perms(request, ["conf.add_configuration"], 'conf/index.html')
    
    return render(request,'conf/index.html', {"conf":conf})

@staff_member_required(login_url=reverse_lazy('login'))
def add_conf(request):
    has_perms(request, ["conf.add_configuration"], None, 'overviewconf')
    if request.method == 'POST':
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()

            messages.add_message(request, messages.SUCCESS, _('The configuration has been succesfully added!'))

            return redirect('overviewconf')
    else:
        form = ConfigurationForm()

    return render(request, 'conf/add.html', {
        'form': form,
    })

@staff_member_required(login_url=reverse_lazy('login'))
def edit_conf(request, pk):
    has_perms(request, ["conf.change_configuration"], None, 'overviewconf')
    instance = get_object_or_404(Configuration, pk=pk)
    if request.method == 'POST':
        form = ConfigurationForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The configuration has been succesfully changed!'))

            return redirect('overviewconf')
    else:
        form = ConfigurationForm(instance=instance)

    return render(request, 'conf/edit.html', {
        'form': form,
        'conf':instance
    })

def save_conf(request):
    has_perms(request, ["conf.change_configuration"], None, 'overviewconf')
    conf = Configuration.objects.filter()
    if request.method == "POST":
        values = request.POST.getlist('conf-value')
        count = 0
        for item in conf:
            item.value = values[count]
            item.save()
            count += 1
    return redirect('overviewconf')

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_conf_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        conf = Configuration.objects.get(id=id)
        if conf:
            context = {
                'conf': conf
            }
            data = {
                'template': render_to_string('conf/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_conf(request,pk):
    has_perms(request, ["conf.delete_configuration"], None, 'overviewconf')
    instance = Configuration.objects.get(pk=pk)
    instance.delete()
    messages.add_message(request, messages.SUCCESS, _('The configuration has been succesfully deleted!'))
    return redirect('overviewconf')
        

