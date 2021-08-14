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
from apps.mail.models import (
    Email, 
    MailTemplate,
    MailTemplateRevision as ModelRevision1,
    MailTemplateVersion as ModelVersion1,
)
from collections import namedtuple
from apps.mail.forms import MailTemplateForm
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
import json
from django.db.models import Q
STATUS = namedtuple('STATUS', 'sent failed queued requeued')._make(range(4))
PRIORITY = namedtuple('PRIORITY', 'low medium high now')._make(range(4))

@staff_member_required(login_url=reverse_lazy('login'))
def overview_email(request):
    has_perms(request, ["mail.view_email"], None, 'dashboard')
    emails = Email.objects.filter(Q(status=STATUS.queued) | Q(status=STATUS.requeued))
    return render(request,'emails/index.html', {"emails":emails})

@staff_member_required(login_url=reverse_lazy('login'))
def overview_mailtemplate(request):
    has_perms(request, ["mail.view_mailtemplate"], None, 'overviewmailtemplate')
    mailtemplates = MailTemplate.objects.filter()
    for template in mailtemplates:
        try:
            revision = ModelRevision1.objects.get(current_instance=template)
            versions = revision.versions.all()
            template.has_versions = bool(versions)
        except:
            continue
    return render(request,'mailtemplates/index.html', {"templates":mailtemplates})

@staff_member_required(login_url=reverse_lazy('login'))
@transaction.atomic
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

@staff_member_required(login_url=reverse_lazy('login'))
@transaction.atomic
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

@staff_member_required(login_url=reverse_lazy('login'))
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

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_mailtemplate_activation_view(request, pk):
    has_perms(request, ["mail.change_mailtemplate"], None, 'overviewmailtemplate')

    item = MailTemplate.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de mailtemplate is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewmailtemplate')

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_mailtemplate(request,pk):
    has_perms(request, ["mail.delete_mailtemplate"], None, 'overviewmailtemplate')
    instance = MailTemplate.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
    return redirect('overviewmailtemplate')

@staff_member_required(login_url=reverse_lazy('login'))
def overview_reversion(request, mode):
    if mode == 'template':
        items = MailTemplate.objects.filter(date_deleted__isnull=False)
    else:
        items = Email.objects.filter(date_deleted__isnull=False)
    return render(request,'mail/reversion-overview-index.html', {"items": items, 'mode': mode})

@staff_member_required(login_url=reverse_lazy('login'))
def revert_mail_item(request, mode, pk):
    try:
        if mode == 'template':
            item = MailTemplate.objects.get(id=pk)
            # redirect_obj = redirect('overviewreversionmail', mode)
            messages.add_message(request, messages.SUCCESS, _('The template has been succesfully reverted!'))
        else:
            item = Email.objects.get(id=pk)
            # redirect_obj = redirect('overviewreversionmail', mode)
            messages.add_message(request, messages.SUCCESS, _('The configuration has been succesfully reverted!'))
        item.date_deleted = None
        item.save()
    except:
        messages.add_message(request, messages.WARNING, _('No such item is available!'))
    
    return redirect('overviewreversionmail', mode)

@staff_member_required(login_url=reverse_lazy('login'))
def get_version_ajax_modal(request):
    if 'template' in request.get_full_path():
        mode = 'template'
    else:
        mode = 'config'
    data = {}
    # import pdb;pdb.set_trace();
    id = request.POST.get('id', False)
    if mode == 'template':
        reversion = ModelRevision1.objects.get(current_instance=MailTemplate.objects.get(id=id))
        versions = ModelVersion1.objects.filter(revision=reversion).order_by("date_created")
        template_path = 'mailtemplates/__partials/version_modal.html'
    else:
        reversion = ModelRevision2.objects.get(current_instance=Email.objects.get(id=id))
        versions = ModelVersion2.objects.filter(revision=reversion).order_by("date_created")
        template_path = 'emails/__partials/version_modal.html'
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
        if mode == 'template':
            version = ModelVersion1.objects.get(id=id)
            template_path = 'mailtemplates/__partials/delete_version_modal.html'
        else:
            version = ModelVersion2.objects.get(id=id)
            template_path = 'emails/__partials/delete_version_modal.html'
    except Exception as e:
        print('Error: ', e)
        version = None
    if version:
        context = {
            'version': version,
        }
        data = {
            'template': render_to_string(template_path, context=context, request=request)
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def select_version(request, mode, pk):
    # import pdb;pdb.set_trace();
    if mode == 'template':
        redirect_obj = redirect('overviewmailtemplate')
    else:
        redirect_obj = redirect('overviewemail')

    if mode == 'template':
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
        setattr(model_obj, attr, value)
    model_obj.not_new_object=1
    model_obj.save()
    messages.add_message(request, messages.SUCCESS, _('Versie succesvol gewijzigd'))
    return redirect_obj

@staff_member_required(login_url=reverse_lazy('login'))
def delete_version(request, mode, pk):
    # import pdb;pdb.set_trace();
    if mode == 'template':
        redirect_obj = redirect('overviewmailtemplate')
    else:
        redirect_obj = redirect('overviewemail')

    try:
        if mode == 'template':
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
    # import pdb;pdb.set_trace();
    if mode == 'template':
        redirect_obj = redirect('overviewmailtemplate')
    else:
        redirect_obj = redirect('overviewemail')

    try:
        if mode == 'template':
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