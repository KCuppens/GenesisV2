from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.urls import reverse
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from .compat import urlsafe_base64_decode
from apps.conf.utils import get_config
from .signals import user_activated, user_registered
from .utils import EmailActivationTokenGenerator, send_activation_email
from django.views.generic import View
User = get_user_model()
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site


if get_config('USERS_SPAM_PROTECTION'):  # pragma: no cover
    from .forms import RegistrationFormHoneypot as RegistrationForm
else:
    from .forms import RegistrationForm

class LoginView(View):
      def get(self,request):
            return render(request,'users/login2.html')
            
            
      def post(self,request):
            username=request.POST['username']
            password=request.POST['password']
            
            if username and password:
                  if User.objects.filter(username=username).exists():
                        user=authenticate(username=username,password=password)
                         
                        if user:
                              if user.is_superuser or user.is_staff:      
                                    login(request,user)
                                    return JsonResponse({"url":reverse('dashboard')})
                              return JsonResponse({"not_suser":"Sorry You're Not eligible for login"})
                        return JsonResponse({"errorpass":"Incorrect Password"})
                  return JsonResponse({"invalup":"Sorry Username and Password is invalid"})
            return JsonResponse({"blankf":"Username and Password Cant be blank"})
            return render(request,'users/login2.html')


