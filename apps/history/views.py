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
from apps.history.models import History
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site

@staff_member_required(login_url=reverse_lazy('login'))
def overview_history(request):
    has_perms(request, ["history.view_history"], 'history/index.html')
    page = request.GET.get('page', 1)

    history = History.objects.filter().order_by('-id')
    paginator = Paginator(history, 25)

    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)
    
    return render(request,'history/index.html', {"history":history})

