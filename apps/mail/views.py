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
from apps.mail.models import MailConfig, MailTemplate
from apps.mail.forms import MailConfigForm, MailTemplateForm
from django.utils.translation import ugettext_lazy as _


@staff_member_required(login_url='/nl/account/login')
def overview_mailconfig(request):
    has_perms(request, ["mail.view_mailconfig"], None, 'overviewmailconfig')
    mailconfigs = MailConfig.objects.filter(date_deleted=None)
    return render(request,'mailconfigs/index.html', {"configs":mailconfigs})

@staff_member_required(login_url='/nl/account/login')
def add_mailconfig(request):
    has_perms(request, ["mail.add_mailconfig"], None, 'overviewmailconfig')
    if request.method == 'POST':
        form = MailConfigForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS, _('The mailconfig has been succesfully added!'))
            return redirect('overviewmailconfig')
    else:
        form = MailConfigForm()

    return render(request, 'mailconfigs/add.html', {
        'form': form,
    })

@staff_member_required(login_url='/nl/account/login')
def edit_mailconfig(request, pk):
    has_perms(request, ["mail.change_mailconfig"], None, 'overviewmailconfig')
    instance = get_object_or_404(MailConfig, pk=pk)
    if request.method == 'POST':
        form = MailConfigForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The mailconfig has been succesfully changed!'))

            return redirect('overviewmailconfig')
    else:
        form = MailConfigForm(instance=instance)

    return render(request, 'mailconfigs/edit.html', {
        'form': form,
        'instance':instance
    })

@staff_member_required(login_url='/nl/account/login')
def delete_ajax_mailconfig_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        mailconfig = MailConfig.objects.get(id=id)
        if mailconfig:
            context = {
                'mailconfig': mailconfig
            }
            data = {
                'template': render_to_string('mailconfigs/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url='/nl/account/login')
def toggle_mailconfig_activation_view(request, pk):
    has_perms(request, ["mail.change_mailconfig"], None, 'overviewmailconfig')

    item = MailConfig.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de mailconfig is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewmailconfig')

        
@staff_member_required(login_url='/nl/account/login')
def delete_mailconfig(request,pk):
    has_perms(request, ["mail.delete_mailconfig"], None, 'overviewmailconfig')
    instance = MailConfig.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
    return redirect('overviewmailconfig')

@staff_member_required(login_url='/nl/account/login')
def overview_mailtemplate(request):
    has_perms(request, ["mail.view_mailtemplate"], None, 'overviewmailtemplate')
    mailtemplates = MailTemplate.objects.filter()
    return render(request,'mailtemplates/index.html', {"templates":mailtemplates})

@staff_member_required(login_url='/nl/account/login')
def add_mailtemplate(request):
    has_perms(request, ["mail.add_mailtemplate"], None, 'overviewmailtemplate')
    if request.method == 'POST':
        form = MailTemplateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()

            messages.add_message(request, messages.SUCCESS, _('The mailtemplate has been succesfully added!'))

            return redirect('overviewmailtemplate')
    else:
        form = MailTemplateForm()

    return render(request, 'mailtemplates/add.html', {
        'form': form,
    })

@staff_member_required(login_url='/nl/account/login')
def edit_mailtemplate(request, pk):
    has_perms(request, ["mail.change_mailtemplate"], None, 'overviewmailtemplate')
    instance = get_object_or_404(MailTemplate, pk=pk)
    if request.method == 'POST':
        form = MailTemplateForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The mailtemplate has been succesfully changed!'))

            return redirect('overviewmailtemplate')
    else:
        form = MailTemplateForm(instance=instance)

    return render(request, 'mailtemplates/edit.html', {
        'form': form,
        'instance':instance
    })

@staff_member_required(login_url='/nl/account/login')
def delete_ajax_mailtemplate_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        mailtemplate = MailTemplate.objects.get(id=id)
        if mailtemplate:
            context = {
                'mailtemplate': mailtemplate
            }
            data = {
                'template': render_to_string('mailtemplates/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url='/nl/account/login')
def toggle_mailtemplate_activation_view(request, pk):
    has_perms(request, ["mail.change_mailtemplate"], None, 'overviewmailtemplate')

    item = MailTemplate.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de mailtemplate is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewmailtemplate')

        
@staff_member_required(login_url='/nl/account/login')
def delete_mailtemplate(request,pk):
    has_perms(request, ["mail.delete_mailtemplate"], None, 'overviewmailtemplate')
    instance = MailTemplate.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
    return redirect('overviewmailtemplate')
