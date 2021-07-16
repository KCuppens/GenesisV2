from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
from django.contrib import messages
from . forms import GroupForm
from django.utils import timezone
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.hashers import make_password
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
from .utils import EmailActivationTokenGenerator, send_activation_email,has_perms
from django.views.generic import View
User = get_user_model()
from django.contrib.admin.views.decorators import staff_member_required
from apps.base.utils import has_perms
from apps.user.forms import UserForm, UserChangePasswordForm, UserSetPasswordForm
import xlsxwriter
import io
from django.http import HttpResponse
import datetime
now = datetime.datetime.now()
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site
User = get_user_model()

class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request,'users/login.html')

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
                            return JsonResponse({'url': reverse('dashboard')})
                        return JsonResponse({"not_suser":_("Sorry you do not have the proper access to login")})
                    return JsonResponse({"errorpass":_("Incorrect password")})
                return JsonResponse({"invalup":_("Sorry email and password is invalid")})
            else:
                if User.objects.filter(username=username).exists():
                    user=authenticate(username=username,password=password)
                    if user:
                        if user.is_superuser or user.is_staff:      
                            login(request,user)
                            return redirect('dashboard')
                        return JsonResponse({"not_suser":_("Sorry you do not have the proper access to login")})
                    return JsonResponse({"errorpass":_("Incorrect password")})
                return JsonResponse({"invalup":_("Sorry username and password is invalid")})
        return JsonResponse({"blankf":_("Username and password cant be blank")})

@staff_member_required(login_url=reverse_lazy('login'))
def overview_user(request):
    has_perms(request, ["user.view_user"], 'users/overview.html')

    search = request.GET.get('search', None)
    group = request.GET.get('group', None)
    if group:
        user = User.objects.filter(groups__id=group)
    elif search:
        user = User.objects.filter(Q(first_name__contains=search) | Q(last_name__contains=search) | Q(email__contains=search))
    else:
        user=User.objects.filter(date_deleted=None)
    groups=Group.objects.filter(date_deleted=None)
    
    return render(request,'user/index.html', {
        "users":user,
        "groups": groups,
        'search': search,
        "group_select": group,
    })

@staff_member_required(login_url=reverse_lazy('login'))
def add_user(request):
    has_perms(request, ["user.add_user"], None, 'overviewuser')
    if request.method == 'POST':
        form = UserForm(request.POST or request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.edited_by = request.user
            instance.save()
            send_mail_password_set(instance)
            group_ids = dict(request.POST).get('groups', [])
            groups = Group.objects.filter(pk__in=group_ids)

            for id_ in list(Group.objects.values_list('id', flat=True)):
                instance.groups.remove(int(id_))
            for id_ in list(groups.values_list('id', flat=True)):
                instance.groups.add(int(id_))
            messages.add_message(request, messages.SUCCESS, _('The user has been succesfully added!'))

            return redirect('overviewuser')
    else:
        form = UserForm()

    return render(request, 'user/add.html', {
        'form': form,
    })

def change_user_password(request, pk):
    has_perms(request, ["user.change_user"], None, 'overviewuser')

    instance = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserChangePasswordForm(instance=instance, data=request.POST)
        if form.is_valid():
            instance.edited_by = request.user
            instance.password = make_password(form.cleaned_data.get('password'))
            instance.save()
            messages.add_message(request, messages.SUCCESS, _('The password has been successfully changed!'))

            return redirect('overviewuser')
    else:
        form = UserChangePasswordForm()

    return render(request, 'user/changepassword.html', {
        'form': form,
        'user': instance
    })

@staff_member_required(login_url=reverse_lazy('login'))
def edit_user(request, pk):
    has_perms(request, ["user.change_user"], None, 'overviewuser')
    instance = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.edited_by = request.user
            instance.save()
            group_ids = dict(request.POST).get('groups', [])
            groups = Group.objects.filter(pk__in=group_ids)

            for id_ in list(Group.objects.values_list('id', flat=True)):
                instance.groups.remove(int(id_))
            for id_ in list(groups.values_list('id', flat=True)):
                instance.groups.add(int(id_))

            messages.add_message(request, messages.SUCCESS, _('The user has been succesfully changed!'))

            return redirect('overviewuser')
    else:
        form = UserForm(instance=instance)

    return render(request, 'user/edit.html', {
        'form': form,
        'user':instance
    })

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_user_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        user = User.objects.get(id=id)
        if user:
            context = {
                'user': user
            }
            data = {
                'template': render_to_string('user/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_user(request,pk):
    has_perms(request, ["user.delete_user"], None, 'overviewuser')
    instance = User.objects.get(pk=pk)
    instance.edited_by = request.user
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The user has been succesfully deleted!'))
    return redirect('overviewuser')

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_activation_view(request, pk):
    has_perms(request, ["user.change_user"], None, 'overviewuser')

    item = User.objects.get(pk=pk)
    item.is_active = not item.is_active
    messages.add_message(request, messages.SUCCESS, _('De status van de gebruiker is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewuser')

@staff_member_required(login_url=reverse_lazy('login'))
def my_profile(request):
    has_perms(request, ["user.view_user"], None, 'overviewuser')
    user = User.objects.get(id=request.user.id)
    return render(request,'users/myprofile.html',{"user":user})

@staff_member_required(login_url=reverse_lazy('login'))
def group_view(request):
    has_perms(request, ["user.view_group"], "group/index.html")

    return render(request, 'group/index.html', {
        'groups': Group.objects.filter(date_deleted=None)
    })

@staff_member_required(login_url=reverse_lazy('login'))
def add_group_view(request):
    has_perms(request, ["user.view_group"], None, 'overviewgroup')

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.edited_by = request.user
            instance.save()

            permission_ids = dict(request.POST).get('permissions', [])
            permissions = Permission.objects.filter(pk__in=permission_ids)

            for id_ in list(Permission.objects.values_list('id', flat=True)):
                instance.permissions.remove(int(id_))
            for id_ in list(permissions.values_list('id', flat=True)):
                instance.permissions.add(int(id_))
            instance.save()
            messages.add_message(request, messages.SUCCESS, _('The group has been succesfully added!'))
            return redirect('overviewgroup')

    else:
        form = GroupForm()

    return render(request, 'group/add.html', {
        'form': form,
    })

@staff_member_required(login_url=reverse_lazy('login'))
def edit_group_view(request, pk):
    has_perms(request, ["user.change_group"], None, 'overviewgroup')

    try:
        instance = Group.objects.filter(pk=pk).first()
    except:
        raise Http404

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.edited_by = request.user
            instance.name = request.POST.get('name')
            permission_ids = dict(request.POST).get('permissions', [])
            permissions = Permission.objects.filter(pk__in=permission_ids)

            for id_ in list(Permission.objects.values_list('id', flat=True)):
                instance.permissions.remove(int(id_))
            for id_ in list(permissions.values_list('id', flat=True)):
                instance.permissions.add(int(id_))
            instance.save()

            messages.add_message(request, messages.SUCCESS, _('The group has been succesfully edited!'))
            return redirect('overviewgroup')
    else:
        form = GroupForm(instance=instance)

    return render(request, 'group/edit.html', {
        'form': form,
        'group': instance
    })

@staff_member_required(login_url=reverse_lazy('login'))
def delete_group_view(request, pk):
    has_perms(request, ["user.delete_group"], None, 'overviewgroup')

    item = Group.objects.get(pk=pk)
    item.date_deleted = timezone.now()
    item.edited_by = request.user
    item.save()

    messages.add_message(request, messages.SUCCESS, _('The group has been succesfully deleted!'))
    return redirect('overviewgroup')

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_group_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        group = Group.objects.get(id=id)
        if group:
            context = {
                'group': group
            }
            data = {
                'template': render_to_string('group/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url=reverse_lazy('login'))
def export_users(request):
    has_perms(request, ["user.view_user"], 'users/overview.html')
    output = io.BytesIO()
    
    workbook = xlsxwriter.Workbook(output)
    worksheet =  workbook.add_worksheet()
    row = 1
    first_name_header = 'Voornaam'
    last_name_header = 'Achternaam'
    email_header = 'Email'
    group_header = 'Groepen'
    username_header = 'Gebruikersnaam'
    

    worksheet.write('A' + str(row), first_name_header)
    worksheet.write('B' + str(row), last_name_header)
    worksheet.write('C' + str(row), email_header)
    worksheet.write('D' + str(row), group_header)
    worksheet.write('E' + str(row), username_header)    
    row += 1

    for user in User.objects.filter(date_deleted=None, is_staff=True):
        usergroups = ''
        for group in user.groups.all():
            usergroups += group.name + ','
        worksheet.write('A' + str(row), user.first_name)
        worksheet.write('B' + str(row), user.last_name)
        worksheet.write('C' + str(row), user.email)
        worksheet.write('D' + str(row), usergroups)
        worksheet.write('E' + str(row), user.username)    

        row += 1

    workbook.close()
    output.seek(0)

    filename = 'export_users_' + now.strftime("%H:%M:%S") + '.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def send_mail_password_set(user):
    subject = "Password Set Requested"
    email_template_name = "users/password_set_email.html"
    context = {
        "email": user.email,
        'domain':'127.0.0.1:8000',
        'site_name': 'Website',
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    email = render_to_string(email_template_name, context)
    try:
        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

def password_set_request(request, uidb64):
    user = self.get_user(uidb64)
    if user:
        if request.method == "POST":
            form = UserSetPasswordForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data['password']
                user = User.objects.filter(email=data).first()
                if user.exists() and data:
                    user.set_password(data)
                    user.save()
                    return render(request=request, template_name="user/setpassword.html", context={"message": _('Password has been succesfully changed')})       
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="user/setpassword.html", context={"form":password_reset_form})
    else:
        return render(request=request, template_name="user/setpassword.html", context={"message": _('Link not valid')})

def get_user(self, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
        user = None
    return user


@staff_member_required(login_url=reverse_lazy('login'))
def overview_reversion(request):
    users = User.objects.filter(date_deleted__isnull=False)
    return render(request,'user/reversion-overview-index.html', {"users": users})

@staff_member_required(login_url=reverse_lazy('login'))
def revert_user(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.date_deleted = None
        user.save()
        messages.add_message(request, messages.SUCCESS, _('User has been succesfully reverted!'))
    except:
        messages.add_message(request, messages.WARNING, _('No such user is available!'))
    
    return redirect('overviewreversionuser')