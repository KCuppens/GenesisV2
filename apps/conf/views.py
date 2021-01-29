from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from apps.conf.models import Configuration
from apps.conf.forms import ConfigurationForm
# Create your views here.

@method_decorator(staff_member_required, name='dispatch')
class ConfigurationListView(ListView):
    model = Configuration
    template_name = 'conf/configuration.html'

    def get_queryset(self):
        return Configuration.objects.filter()


@method_decorator(staff_member_required, name='dispatch')
class ConfigurationEditView(FormView):
    template_name = 'conf/configuration-edit.html'
    form_class =  ConfigurationForm
    succes_url = '/nl/dashboard'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

        

