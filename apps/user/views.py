from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from . forms import GroupForm
from django.utils import timezone
from django.contrib.auth.models import Group,Permission
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
User = get_user_model()
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
from .utils import EmailActivationTokenGenerator, send_activation_email,has_perms
from django.views.generic import View


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
                  if '@' in username:
                        if User.objects.filter(email=username).exists():
                              uname=User.objects.get(email=username).username
                              user=authenticate(username=uname,password=password)
                              if user:
                                    if user.is_superuser or user.is_staff:      
                                          login(request,user)
                                          return JsonResponse({"url":reverse('overviewuser')})
                                    return JsonResponse({"not_suser":_("Sorry You're Not eligible for login")})
                              return JsonResponse({"errorpass":_("Incorrect Password")})
                        return JsonResponse({"invalup":_("Sorry Email and Password is invalid")})
                  else:
                        if User.objects.filter(username=username).exists():
                              user=authenticate(username=username,password=password)
                              if user:
                                    if user.is_superuser or user.is_staff:      
                                          login(request,user)
                                          return JsonResponse({"url":reverse('dashboard')})
                                    return JsonResponse({"not_suser":_("Sorry You're Not eligible for login")})
                              return JsonResponse({"errorpass":_("Incorrect Password")})
                        return JsonResponse({"invalup":_("Sorry Username and Password is invalid")})
            return JsonResponse({"blankf":_("Username and Password Cant be blank")})
            return render(request,'users/login2.html')

# @staff_member_required(login_url='/account/login')
def overview_user(request):
    userr=User.objects.all()
    groups=Group.objects.all()
    if not has_perms(user=request.user, permission="Can add Gebruiker"):
        return render(request,'users/usermanagement.html',{
            'permission_denied':True
        })
    
    return render(request,'users/usermanagement.html',{"users":userr,'groups':groups})

# @staff_member_required(login_url='/account/login')
def edit_user(request, pk):
    if not has_perms(user=request.user, permission="Can change Gebruiker"):
        return redirect('usermanagement')
    instance = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST,instance=instance)
        form.is_valid()
        instance.edited_by = request.user
        instance.first_name = form.cleaned_data.get('first_name')
        instance.last_name = form.cleaned_data.get('last_name')
        instance.email = form.cleaned_data.get('email')
        instance.is_active = form.cleaned_data.get('is_active')
        instance.is_staff = form.cleaned_data.get('is_staff')
        instance.birthdate=form.cleaned_data.get('birthdate')
        instance.avatar=request.FILES.get("pic",instance.avatar)
        instance.phone=form.cleaned_data.get("phone")
        instance.profession=form.cleaned_data.get('profession')
        instance.user_type=form.cleaned_data.get('user_type')
        instance.company_name=form.cleaned_data.get('company_name')
        instance.company_vat=form.cleaned_data.get('company_vat')
        instance.front_client=form.cleaned_data.get('front_client')
        

        
        instance.save()
        group_ids = dict(request.POST).get('groups', [])
        groups = Group.objects.filter(pk__in=group_ids)

        for id_ in list(Group.objects.values_list('id', flat=True)):
            instance.groups.remove(int(id_))
        for id_ in list(groups.values_list('id', flat=True)):
            instance.groups.add(int(id_))

        return redirect('useroverview')
    else:
        form = UserEditForm(
            initial={
                'username': instance.username,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'email': instance.email,
                'avatar':instance.avatar,
                'is_active': instance.is_active,
                'birthdate':instance.birthdate,
                'profession':instance.profession,
                'is_staff': instance.is_staff,
                'phone':instance.phone,
                'user_type':instance.user_type,
                'front_client':instance.front_client,
                'company_name':instance.company_name,
                'is_superuser': instance.is_superuser,
                'groups': User.objects.filter(pk=pk).first().groups.values_list('id', flat=True)
            }
        )

    return render(request, 'users/edituser.html', {
        'form': form,
        'Profile':instance
        
    })

def delete_user(request,pk):
    instance = User.objects.filter(pk=pk)
    instance.date_deleted = timezone.now()
    return redirect('useroverview')

def my_profile(request):
    user = User.objects.get(id=request.user.id)
    return render(request,'users/myprofile.html',{"user":user})

def group_view(request):
    if not has_perms(user=request.user, permission="Can add Gebruiker"):
        return render(request, 'users/group.html', {
            'permission_denied': True,
        })
    return render(request, 'users/group.html', {
        'users': User.objects.all(),
        'groups': Group.objects.all()
    })

def add_group_view(request):
    if not has_perms(user=request.user,permission="Can add group"):
        return render(request, 'users/group.html', {
            'permission_denied': True,
            'users': User.objects.order_by('is_active', '-date_joined'),
            'groups': Group.objects.all()
        })
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.author = request.user
            form.save()
            return render(request, 'users/group.html', {
                'users': User.objects.order_by('is_active', '-date_joined'),
                'groups': Group.objects.all(),
                'form_name': 'groups'
            })
    else:
        form = GroupForm()

    return render(request, 'users/groupadd.html', {
        'form': form,
        'form_name': 'groups'
    })

# @staff_member_required(login_url='/account/login')
def edit_group_view(request, pk):
    if not has_perms(user=request.user, permission="Can change group"):
        return render(request, 'users/group.html', {
            'permission_denied': True,
            'users': User.objects.order_by('is_active', '-date_joined'),
            'groups': Group.objects.all()
        })

    try:
        instance = Group.objects.filter(pk=pk).first()
    except:
        raise Http404

    if request.method == 'POST':
        instance.edited_by = request.user
        instance.name = request.POST.get('name')
        permission_ids = dict(request.POST).get('permissions', [])
        permissions = Permission.objects.filter(pk__in=permission_ids)

        for id_ in list(Permission.objects.values_list('id', flat=True)):
            instance.permissions.remove(int(id_))
        for id_ in list(permissions.values_list('id', flat=True)):
            instance.permissions.add(int(id_))

        instance.save()

        return render(request, 'users/group.html', {
            'grouppermissions': instance.permissions.all(),
            'users': User.objects.order_by('is_active', '-date_joined'),
            'groups': Group.objects.all(),
            'form_name': 'groups'
        })
    else:
        form = GroupForm(
            initial={
                'permissions': Permission.objects.filter(group__id=pk),
                'name': Group.objects.filter(pk=pk).first().name,
                'form_name': 'groups'
            }
        )

    return render(request, 'users/groupedit.html', {
        'form': form,
        'grouppermissions': Permission.objects.filter(group__id=pk),
        'form_name': 'groups'
    })

# @staff_member_required(login_url='/account/login')
def delete_group_view(request, pk):
    if not has_perms(user=request.user, permission="Can delete group"):
        return render(request, 'users/group.html', {
            'permission_denied': True,
            'users': User.objects.order_by('is_active', '-date_joined'),
            'groups': Group.objects.all()
        })

    item = Group.objects.filter(pk=pk).first()
    item.edited_by = request.user
    item.save()

    return render(request, 'users/group.html', {
        'users': User.objects.order_by('is_active', '-date_joined'),
        'groups': Group.objects.all(),
        'form_name': 'groups'
    })
