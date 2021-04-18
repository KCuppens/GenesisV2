from django.conf.urls import url
from .views import delete_ajax_mailtemplate_modal, overview_mailtemplate, add_mailtemplate, edit_mailtemplate, delete_mailtemplate, \
                    delete_ajax_mailconfig_modal, overview_mailconfig, add_mailconfig, edit_mailconfig, delete_mailconfig, toggle_mailconfig_activation_view, toggle_mailtemplate_activation_view
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^mailtemplate/overview$').strip(),overview_mailtemplate,name="overviewmailtemplate"),
    url(_('^mailtemplate/add$').strip(),add_mailtemplate,name="addmailtemplate"),
    url(_('^mailtemplate/toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_mailtemplate_activation_view, name="activate-mailtemplates"),
    url(_('^mailtemplate/edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_mailtemplate,name="editmailtemplate"),
    url(_('^mailtemplate/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_mailtemplate,name="deletemailtemplate"),
    url(_('^mailtemplate/delete/modal$').strip(),delete_ajax_mailtemplate_modal,name="deletemodalmailtemplate"),

    url(_('^overview$').strip(),overview_mailconfig,name="overviewmailconfig"),
    url(_('^add$').strip(),add_mailconfig,name="addmailconfig"),
    url(_('^edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_mailconfig,name="editmailconfig"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_mailconfig_activation_view, name="activate-mailconfig"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_mailconfig,name="deletemailconfig"),
    url(_('^delete/modal$').strip(),delete_ajax_mailconfig_modal,name="deletemodalmailconfig"),
]