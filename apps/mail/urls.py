from django.conf.urls import url
from .views import delete_ajax_mailtemplate_modal, overview_mailtemplate, add_mailtemplate, edit_mailtemplate, delete_mailtemplate, \
                   overview_email, toggle_mailtemplate_activation_view, \
                   get_version_ajax_modal, select_version, \
                   delete_version, add_version_comment, get_delete_version_ajax_modal, \
                   overview_reversion, revert_mail_item
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^mailtemplate/overview$').strip(),overview_mailtemplate,name="overviewmailtemplate"),
    url(_('^mailtemplate/add$').strip(),add_mailtemplate,name="addmailtemplate"),
    url(_('^mailtemplate/toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_mailtemplate_activation_view, name="activate-mailtemplates"),
    url(_('^mailtemplate/edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_mailtemplate,name="editmailtemplate"),
    url(_('^mailtemplate/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_mailtemplate,name="deletemailtemplate"),
    url(_('^mailtemplate/delete/modal$').strip(),delete_ajax_mailtemplate_modal,name="deletemodalmailtemplate"),

    url(_('^overview$').strip(),overview_email,name="overviewemail"),

    url(_('^overview/reversion/(?P<mode>[a-z]+)/$').strip(),overview_reversion,name="overviewreversionmail"),
    url(_('^revert/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)/$').strip(),revert_mail_item,name="revertmail"),

    url(_('^version/modal/template/$').strip(),get_version_ajax_modal,name="mailtemplateversionmodal"),
    url(_('^version/modal/delete/(?P<mode>[a-z]+)/$').strip(),get_delete_version_ajax_modal,name="maildeleteversionmodal"),
    url(_('^version/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)$').strip(),select_version,name="mailselectversion"),
    url(_('^version/delete/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)/$').strip(),delete_version,name="maildeleteversion"),
    url(_('^version/comment/(?P<mode>[a-z]+)/(?P<pk>[0-9a-f-]+)/$').strip(),add_version_comment,name="mailaddversioncomment"),
]