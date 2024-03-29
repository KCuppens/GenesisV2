from django.conf import settings
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
from apps.logs.models import MessageLog
from django.utils.translation import ugettext_lazy as _

@staff_member_required(login_url=reverse_lazy('login'))
def overview_logs(request):
    has_perms(request, ["logs.view_messagelog"], None, 'dashboard')
    logs = MessageLog.objects.all().order_by('-date')
    amount_billable = MessageLog.objects.filter(invoiced__isnull=True).count()
    amount_billed = MessageLog.objects.filter(invoiced__isnull=False).count()
    if settings.MAIL_CREDITS_COST:
        mailcredits_cost = settings.MAIL_CREDITS_COST 
    else: 
        mailcredits_cost = 7.5
    billable_amount = int(amount_billable)/1000 * settings.MAIL_CREDITS_COST
    return render(request,'logs/index.html', {"logs":logs, 'amount_billable': amount_billable, 'amount_billed': amount_billed, 'mailcredits_cost': mailcredits_cost, 'billable_amount': billable_amount})

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_log_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        log = MessageLog.objects.get(id=id)
        if log:
            context = {
                'log': log
            }
            data = {
                'template': render_to_string('logs/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_log(request,pk):
    has_perms(request, ["logs.delete_messagelog"], None, 'overviewlogs')
    instance = MessageLog.objects.get(pk=pk)
    instance.delete()
    messages.add_message(request, messages.SUCCESS, _('The message log has been succesfully deleted!'))
    return redirect('overviewlog')
