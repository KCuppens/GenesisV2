from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from apps.dashboard.models import DashboardConfiguration
from apps.dashboard.forms import DashboardConfigurationForm
from django.utils.translation import ugettext as _
from apps.base.utils import has_perms
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
@staff_member_required(login_url=reverse_lazy('login'))
def dashboard_view(request):
    has_perms(request, ["dashboard.view_dashboardconfiguration"], 'dashboard/admin/index.html')
    dashboard = DashboardConfiguration.objects.filter(active=True, date_deleted=None).order_by('position')
    # filtering dashboard on the basis of GoogleAnalytics presence
    dashboard = [dash for dash in dashboard if dash.is_available()]
    return render(request, 'dashboard/dashboard.html', {'dashboard': dashboard})

@staff_member_required(login_url=reverse_lazy('login'))
def overview_dashboard(request):
    dashboard = DashboardConfiguration.objects.filter(date_deleted=None, active=True).order_by('position')
    has_perms(request, ["dashboard.view_dashboardconfiguration"], 'dashboard/admin/index.html')
    
    return render(request,'dashboard/admin/index.html', {"dashboard":dashboard})

@staff_member_required(login_url=reverse_lazy('login'))
def add_dashboard(request):
    has_perms(request, ["dashboard.add_dashboardconfiguration"], None, 'overviewdashboard')
    if request.method == 'POST':
        form = DashboardConfigurationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()

            messages.add_message(request, messages.SUCCESS, _('The dashboard has been succesfully added!'))

            return redirect('overviewdashboard')
    else:
        form = DashboardConfigurationForm()

    return render(request, 'dashboard/admin/add.html', {
        'form': form,
    })

@staff_member_required(login_url=reverse_lazy('login'))
def edit_dashboard(request, pk):
    has_perms(request, ["dashboard.change_dashboardconfiguration"], None, 'overviewdashboard')
    instance = get_object_or_404(DashboardConfiguration, pk=pk)
    if request.method == 'POST':
        form = DashboardConfigurationForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The dashboard has been succesfully changed!'))

            return redirect('overviewdashboard')
    else:
        form = DashboardConfigurationForm(instance=instance)

    return render(request, 'dashboard/admin/edit.html', {
        'form': form,
        'dashboard':instance
    })

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_dashboard_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        dashboard = DashboardConfiguration.objects.get(id=id)
        if dashboard:
            context = {
                'dashboard': dashboard
            }
            data = {
                'template': render_to_string('dashboard/admin/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_dashboard_activation_view(request, pk):
    has_perms(request, ["dashboard.change_dashboardconfiguration"], None, 'overviewdashboard')

    item = DashboardConfiguration.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de dashboard is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewdashboard')

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_dashboard(request,pk):
    has_perms(request, ["dashboard.delete_dashboardconfiguration"], None, 'overviewdashboard')
    instance = DashboardConfiguration.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
    return redirect('overviewdashboard')

def reorder_dashboard(request):
    has_perms(request, ["dashboard.change_dashboardconfiguration"], None, 'overviewdashboard')
    items = request.POST.get('item', 'None')
    array = items.split('[]=')
    ids = ''.join(array)
    ids = ids.split('&')
    position = 0 

    for id in ids:
        item = DashboardConfiguration.objects.get(id=id)
        position += 1
        item.position = position 
        item.save()
    data = {

    }
    return JsonResponse(data)


@staff_member_required(login_url=reverse_lazy('login'))
def overview_reversion(request):
    dashboard_confs = DashboardConfiguration.objects.filter(date_deleted__isnull=False)
    return render(request,'dashboard/admin/reversion-overview-index.html', {"dashboard":dashboard_confs})

@staff_member_required(login_url=reverse_lazy('login'))
def revert_dashboard(request, pk):
    try:
        dashboard = DashboardConfiguration.objects.get(id=pk)
        dashboard.date_deleted = None
        dashboard.save()
        messages.add_message(request, messages.SUCCESS, _('The Dashboard Configuration has been succesfully reverted!'))
    except:
        messages.add_message(request, messages.WARNING, _('No such Dashboard Configuration is available!'))
    
    return redirect('overviewreversiondashboard')