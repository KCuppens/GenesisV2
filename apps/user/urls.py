from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import LoginView, overview_user, edit_user, delete_user, my_profile, group_view, add_group_view, edit_group_view, delete_group_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^login$'),LoginView.as_view(),
        name='login'),
    url(_('^logout$'), auth_views.LogoutView.as_view(
        template_name='users/logout.html'),

        name='users_logout'),
    url(_('^password_change$'), auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url='users_password_change_done'),
        name='users_password_change'),
    url(_('^password_change/done$'), auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
        name='users_password_change_done'),
    # url(r'^sign-up/',Signup.as_view(),name='register'),
    url(_('^password_reset$'),auth_views.PasswordResetView.as_view(template_name="reset/reset_email.html",
                                                      email_template_name='reset/password_reset_email.html',
                                                      subject_template_name='reset/password_reset_subject.txt',
                                                      html_email_template_name='reset/password_email_html.html',
                                                      ),name="password_reset"),
    url(_('^reset/done$'), auth_views.PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'),name='password_reset_done'),
    url(_('^reset/complete$'), auth_views.PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'),name='password_reset_complete'),
    url(_('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$'),auth_views.PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html'),name='password_reset_confirm'),
    url(_('^user/overview$'),overview_user,name="overviewuser"),
    url(_('^user/edit/<int:pk>'),edit_user,name="edituser"),
    url(_('^user/delete/<int:pk>'),delete_user,name="deleteuser"),
    url(_('^my-profile$'),my_profile,name="my-profile"),
    url(_('^group'),group_view,name="group"),
    url(_('^group/add'),add_group_view,name="addgroup"),
    url(_('^group/edit/<pk>'),edit_group_view,name="editgroup"),
    url(_('^group/delete/<pk>'),delete_group_view,name="deletegroup"),
]