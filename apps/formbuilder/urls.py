from django.conf.urls import url
from .views import (
    export_form_results, 
    delete_formresult,
    delete_ajax_formresult_modal,  
    handle_form, render_form, 
    delete_ajax_form_modal, 
    overview_form, 
    add_form, 
    edit_form, 
    delete_form, 
    toggle_form_activation_view, 
    get_formbuilder, 
    overview_form_results, 
    get_form,
    get_version_ajax_modal,
    get_delete_version_ajax_modal,
    select_version,
    delete_version,
    add_version_comment, 
    overview_reversion,
    revert_form
)
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$').strip(),overview_form,name="overviewform"),
    url(_('^add$').strip(),add_form,name="addform"),
    url(_('^edit/(?P<pk>[0-9a-f-]+)$').strip(),edit_form,name="editform"),
    url(_('^preview$').strip(),render_form,name="previewform"),
    url(_('^toggle-activation/(?P<pk>[0-9a-f-]+)$').strip(), toggle_form_activation_view, name="activate-form"),
    url(_('^results/(?P<pk>[0-9a-f-]+)$').strip(), overview_form_results, name="results-form"),
    url(_('^export/results/(?P<pk>[0-9a-f-]+)$').strip(), export_form_results, name="export-results-form"),
    url(_('^delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_form,name="deleteform"),
    url(_('^delete/modal$').strip(),delete_ajax_form_modal,name="deletemodalform"),
    url(_('^delete/formresult/(?P<pk>[0-9a-f-]+)/(?P<id>[0-9a-f-]+)$').strip(),delete_formresult,name="deleteformresult"),
    url(_('^delete/formresult/modal$').strip(),delete_ajax_formresult_modal,name="deletemodalformresult"),

    url(_('^get-formbuilder$').strip(),get_formbuilder,name="getformbuilder"),
    url(_('^get-form$').strip(),get_form,name="getform"),
    url(_('^handle-form$').strip(),handle_form,name="handleform"),

    url(_('^overview/reversion/$').strip(),overview_reversion,name="overviewreversionform"),
    url(_('^revert/(?P<pk>[0-9a-f-]+)$').strip(),revert_form,name="revertform"),

    url(_('^version/modal$').strip(),get_version_ajax_modal,name="formversionmodal"),
    url(_('^version/deletemodal$').strip(),get_delete_version_ajax_modal,name="formdeleteversionmodal"),
    url(_('^version/(?P<pk>[0-9a-f-]+)$').strip(),select_version,name="formselectversion"),
    url(_('^version/delete/(?P<pk>[0-9a-f-]+)$').strip(),delete_version,name="formdeleteversion"),
    url(_('^version/comment/(?P<pk>[0-9a-f-]+)$').strip(),add_version_comment,name="formaddversioncomment"),
]