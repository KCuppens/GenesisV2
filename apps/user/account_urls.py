from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .views import LoginView
from django.utils.translation import ugettext as _
from apps.user.views import password_set_request

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(_('^login$').strip(),LoginView.as_view(),
        name='login'),
    url(_('^logout$').strip(), auth_views.LogoutView.as_view(
        template_name='users/logout.html'),

        name='users_logout'),
    url(_('^password_change$').strip(), auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url='users_password_change_done'),
        name='users_password_change'),
    url(_('^password_change/done$').strip(), auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
        name='users_password_change_done'),
    # url(r'^sign-up/',Signup.as_view(),name='register'),
    url(_('^password_reset$').strip(),auth_views.PasswordResetView.as_view(template_name="reset/reset_email.html",
                                                      email_template_name='reset/password_reset_email.html',
                                                      subject_template_name='reset/password_reset_subject.txt',
                                                      html_email_template_name='reset/password_email_html.html',
                                                      ),name="password_reset"),
    url(_('^password_set/(?P<uidb64>[0-9A-Za-z_\-]+)/$').strip(),password_set_request,name='password_set'),
    url(_('^reset/done$').strip(), auth_views.PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'),name='password_reset_done'),
    url(_('^reset/complete$').strip(), auth_views.PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'),name='password_reset_complete'),
    url(_('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$').strip(),auth_views.PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html'),name='password_reset_confirm'),
]