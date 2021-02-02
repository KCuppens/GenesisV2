from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import LoginView,dashboardtable,edit_user,delete_user,my_profile

urlpatterns = [
    url(r'^login/$',LoginView.as_view(),
        name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(
        template_name='users/logout.html'),

        name='users_logout'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url='users_password_change_done'),
        name='users_password_change'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
        name='users_password_change_done'),
    # url(r'^sign-up/',Signup.as_view(),name='register'),
    url(r'^password_reset/$',auth_views.PasswordResetView.as_view(template_name="reset/reset_email.html",
                                                      email_template_name='reset/password_reset_email.html',
                                                      subject_template_name='reset/password_reset_subject.txt',
                                                      html_email_template_name='reset/password_email_html.html',
                                                      ),name="password_reset"),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'),name='password_reset_done'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'),name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html'),name='password_reset_confirm'),
    url(r'^dashobard/usertable/$',dashboardtable,name="usermanagement"),
    path('user/edit/<int:pk>/',edit_user,name="edituser"),
    path('user/delete/<int:pk>/',delete_user,name="deleteuser"),
    path('my-profile/',my_profile,name="my-profile"),
    path('group/',group_view,name="group"),
    path('group/add/',add_group_view,name="addgroup"),
    path('group/<pk>/',edit_group_view,name="editgroup"),
    path('group/<pk>/',delete_group_view,name="deletegroup"),
]