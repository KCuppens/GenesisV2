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
from apps.formbuilder.models import Form, FormPage, FormElement, FormElementOption, FormResult, FormResultField
from apps.formbuilder.forms import FormbuilderForm, FormPageForm
from django.utils.translation import ugettext_lazy as _
from apps.mail.mail import send
import xlsxwriter
import io
from django.http import HttpResponse
import datetime
now = datetime.datetime.now()

@staff_member_required(login_url=reverse_lazy('login'))
def overview_form(request):
    has_perms(request, ["formbuilder.view_form"], None, 'overviewform')
    forms = Form.objects.filter(date_deleted=None)
    return render(request,'forms/index.html', {"forms":forms})

@staff_member_required(login_url=reverse_lazy('login'))
def add_form(request):
    has_perms(request, ["formbuilder.add_form"], None, 'overviewform')
    if request.method == 'POST':
        form = FormbuilderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            if 'form_page' in request.session:
                for page in request.session['form_page']:
                    page_obj = FormPage.objects.get(id=page)
                    instance.pages.add(page_obj)
            form.save_m2m()
            if 'form_page' in request.session:
                del request.session['form_page']

            messages.add_message(request, messages.SUCCESS, _('The form has been succesfully added!'))

            return redirect('overviewform')
    else:
        form = FormbuilderForm()

    return render(request, 'forms/add.html', {
        'form': form,
    })

@staff_member_required(login_url=reverse_lazy('login'))
def edit_form(request, pk):
    has_perms(request, ["formbuilder.change_form"], None, 'overviewform')
    instance = get_object_or_404(Form, pk=pk)
    request.session['form_page'] = []
    for page in instance.pages.all():
        form_page = request.session['form_page']
        form_page.append(page.id)
        request.session['form_page'] = form_page
    if request.method == 'POST':
        form = FormbuilderForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            if 'form_page' in request.session:
                instance.pages.clear()
                for page in request.session['form_page']:
                    page_obj = FormPage.objects.get(id=page)
                    instance.pages.add(page_obj)
            if 'form_page' in request.session:
                del request.session['form_page']
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The form has been succesfully changed!'))

            return redirect('overviewform')
    else:
        form = FormbuilderForm(instance=instance)

    return render(request, 'forms/edit.html', {
        'form': form,
        'instance':instance
    })

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_form_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        form = Form.objects.get(id=id)
        if form:
            context = {
                'form': form
            }
            data = {
                'template': render_to_string('forms/__partials/modal.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

@staff_member_required(login_url=reverse_lazy('login'))
def toggle_form_activation_view(request, pk):
    has_perms(request, ["formbuilder.change_form"], None, 'overviewform')

    item = Form.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de form is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewform')

        
@staff_member_required(login_url=reverse_lazy('login'))
def delete_form(request,pk):
    has_perms(request, ["formbuilder.delete_form"], None, 'overviewform')
    instance = Form.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The form has been succesfully deleted!'))
    return redirect('overviewform')

@staff_member_required(login_url=reverse_lazy('login'))
def overview_form_results(request, pk):
    has_perms(request, ["formbuilder.view_formresult"], None, 'overviewform')
    form_results = FormResult.objects.filter(form=pk, date_deleted=None)
    form = Form.objects.filter(id=pk).first()
    return render(request,'forms/results.html', 
        {
            "form_results":form_results,
            'form': form
        })

@staff_member_required(login_url=reverse_lazy('login'))
def export_form_results(request, pk):
    has_perms(request, ["formbuilder.view_formresult"], None, 'overviewform')
    form_results = FormResult.objects.filter(form=pk, date_deleted=None)
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI']

    output = io.BytesIO()
        
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True} )
    worksheet =  workbook.add_worksheet()
    row = 1
    headers = []
    for result in form_results:
        for field in result.entries.all():
            if not field.field.type == 'submit_button' and not field.field.label in headers:
                if field.field.label == None:
                    headers.append('')
                else:
                    headers.append(field.field.label)

    counter = 0
    for name in headers:
        worksheet.write(letters[counter] + str(row), str(name))
        counter += 1

    row += 1
    for result in form_results:
        counter = 0
        if result.entries.exists():
            for field in result.entries.all():
                if not field.field.type == 'submit_button':
                    worksheet.write(letters[counter] + str(row), field.value)
                    counter += 1
            row += 1

    workbook.close()
    output.seek(0)

    filename = 'export_form_result_' + now.strftime("%H:%M:%S") + '.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@staff_member_required(login_url=reverse_lazy('login'))
def delete_formresult(request, pk, id):
    has_perms(request, ["formbuilder.delete_formresult"], None, 'overviewform')
    instance = FormResult.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The formresult has been succesfully deleted!'))
    return redirect(reverse('results-form', kwargs={'pk': id}))

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_formresult_modal(request):
    if request.is_ajax():
        data = {}
        id = request.POST.get('id', False)
        pk = request.POST.get('pk', False)
        formresult = FormResult.objects.get(id=id)
        form = Form.objects.get(pk=pk)
        if form:
            context = {
                'form': form,
                'formresult': formresult
            }
            data = {
                'template': render_to_string('forms/__partials/modalresult.html', context=context, request=request)
            }
        return JsonResponse(data)
    return False

def get_formbuilder(request):
    if request.method == "POST":
        action = request.POST.get('action', '')
        page = request.POST.get('page', '')
    else:
        action = request.GET.get('action', '')
        page = request.GET.get('page', '')    
    fields = FormElement.GET_FIELDS
    content_fields = FormElement.GET_CONTENT_FIELDS
    colsizes = FormElement.GET_COL_SIZES
    data = {}
    if not 'form_page' in request.session:
        page = FormPage.objects.create(name="Page 1")
        request.session['form_page'] = [page.id]
        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }
    elif action == 'createpage':
        if request.method == "POST":
            form = FormPageForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = form.cleaned_data.get('name')
                instance.save()
                form_page = request.session['form_page']
                form_page.append(instance.id)
                request.session['form_page'] = form_page
                context = {
                    'form': form,
                }
                data = {
                    'template': render_to_string('forms/__partials/__create_page_modal.html', context=context, request=request),
                    'success': True
                }
            else:
                context = {
                    'errors': form.errors,
                    'form': form,
                }
                data = {
                    'template': render_to_string('forms/__partials/__create_page_modal.html', context=context, request=request),
                    'success': False
                }
        else:
            form = FormPageForm()
            context = {
                'errors': form.errors,
                'form': form,
            }
            data = {
                'template': render_to_string('forms/__partials/__create_page_modal.html', context=context, request=request),
                'success': False
            }
    elif action == 'editpage':
        instance = FormPage.objects.filter(id=page).first()
        if instance:
            if request.method == "POST":
                form = FormPageForm(request.POST, instance=instance)
                if form.is_valid():
                    object = form.save(commit=False)
                    object.save()
                    form_page = request.session['form_page']
                    if not instance.id in form_page:
                        form_page.append(instance.id)
                        request.session['form_page'] = form_page
                    context = {
                        'form': form,
                        'instance': instance
                    }
                    data = {
                        'template': render_to_string('forms/__partials/__edit_page_modal.html', context=context, request=request),
                        'success': True
                    }
                else:
                    context = {
                        'errors': form.errors,
                        'form': form,
                    }
                    data = {
                        'template': render_to_string('forms/__partials/__edit_page_modal.html', context=context, request=request),
                        'success': False
                    }
            else:
                form = FormPageForm(instance=instance)
                context = {
                    'errors': form.errors,
                    'form': form,
                    'instance': instance
                }
                data = {
                    'template': render_to_string('forms/__partials/__edit_page_modal.html', context=context, request=request),
                    'success': False
                }
    elif action == 'deletepagemodal':
        page = FormPage.objects.filter(id=page).first()
        if page:
            context = {
                'page': page
            }
            data = {
                'template': render_to_string('forms/__partials/__delete_page_modal.html', context=context, request=request),
                'title': _('The decision is yours')
            }
    elif action == 'deletepage':
        instance = FormPage.objects.filter(id=page).first()
        if instance:
            if instance.id in request.session['form_page']:
                form_page = request.session['form_page']
                form_page.remove(instance.id)
                request.session['form_page'] = form_page
            instance.delete()
    elif action == 'addfield':
        page = request.POST.get('page')
        field = request.POST.get('field')
        form_page = FormPage.objects.filter(id=page).first()
        form_element = FormElement.objects.create(type=field)
        if field == 'multi_radio_field' or field == 'select_field':
            option1 = FormElementOption.objects.create()
            option2 = FormElementOption.objects.create()
            option3 = FormElementOption.objects.create()
            form_element.options.add(option1, option2, option3)
            form_element.save()
        form_page.elements.add(form_element)
        form_page.save() 
        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }
    elif action == 'sortfields':
        page = request.POST.get('page')
        items = request.POST.get('item', 'None')
        array = items.split('item[]=')
        ids = ''.join(array)
        ids = ids.split('&')
        position = 0 

        for id in ids:
            item = FormElement.objects.get(id=id)
            position += 1
            item.position = position 
            item.save()
        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }
        return JsonResponse(data)
    elif action == 'sortfieldoptions':
        field = request.POST.get('field')
        items = request.POST.get('item', 'None')
        array = items.split('item[]=')
        ids = ''.join(array)
        ids = ids.split('&')
        position = 0 

        for id in ids:
            item = FormElementOption.objects.get(id=id)
            position += 1
            item.position = position 
            item.save()
        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }
        return JsonResponse(data)
    elif action == 'deletefield':
        field = request.POST.get('field')
        form_element = FormElement.objects.filter(id=field).first()
        form_element.delete()

        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }
    elif action == 'deletefieldoption':
        option = request.POST.get('option')
        form_element_option = FormElementOption.objects.filter(id=option).first()
        form_element_option.delete()

        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }
    elif action == 'addfieldoption':
        field = request.POST.get('field')
        form_element = FormElement.objects.filter(id=field).first()

        option = FormElementOption.objects.create()
        form_element.options.add(option)
        form_element.save()

        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }
    elif action == 'savecolsizefield':
        if request.method == 'POST':
            field = request.POST.get('field')
            colsize = request.POST.get('colsize')
        else:
            field = request.GET.get('field')
            colsize = request.GET.get('colsize')

        if field:
            request.session['current_field'] = field
        else:
            field = request.session['current_field']

        form_element = FormElement.objects.filter(id=field).first()
        if request.method == 'POST':
            form_element.col_size = colsize 
            form_element.save()

        context = {
            'field': field,
            'colsize': form_element.col_size,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/__save_colsize.html', context=context, request=request)
        }
    elif action == 'savefield':
        field = request.POST.get('field')
        label = request.POST.get('label')
        minimum = request.POST.get('minimum')
        maximum = request.POST.get('maximum')
        placeholder = request.POST.get('placeholder')
        required = request.POST.get('required')
        is_checked = request.POST.get('checked')
        text = request.POST.get('text')
        image = request.POST.get('image')
        video = request.POST.get('video')
        form_element = FormElement.objects.filter(id=field).first()
        if form_element.type == 'multi_radio_field' or form_element.type == 'select_field':
            option_value = request.POST.getlist('option_value[]')
            option_checked = request.POST.getlist('option_checked[]')
            option_label = request.POST.getlist('option_label[]')
            count = 0
            for option in form_element.options.all():
                option.value = option_value[count]
                option.is_checked = option_checked[count]
                option.label = option_label[count]
                option.save()
                count += 1

        if label:
            form_element.label = label
        if text:
            form_element.text = text 
        if video:
            form_element.video = video 
        if image:
            form_element.image = image
        if placeholder:
            form_element.placeholder = placeholder
        if required:
            form_element.required = required
        if minimum:
            form_element.minimum = minimum
        if maximum:
            form_element.maximum = maximum
        if is_checked:
            form_element.is_checked = is_checked
        form_element.save()
        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }
    elif 'form_page' in request.session:
        context = {
            'pages': request.session['form_page'],
            'fields': fields,
            'content_fields': content_fields,
            'colsizes': colsizes
        }
        data = {
            'template': render_to_string('forms/__partials/formbuilder.html', context=context, request=request)
        }

    return JsonResponse(data)

def render_form(request):
    if 'form_page' in request.session:
        pages = request.session['form_page']
    context = {
        'pages': pages,
    }
    data = {
        'template': render_to_string('forms/__partials/preview.html', context=context, request=request)
    }
    return JsonResponse(data)


def get_form(request):
    form = request.POST.get('form')
    form_obj = Form.objects.filter(id=form).first()
    if not 'form_' + str(form_obj.id) in request.session:
        pages = []
        for page in form_obj.pages.all():
            pages.append(page.id)
        request.session['form_' + str(form_obj.id)] = {
            'current_page': 1,
            'count_pages': form_obj.pages.count(),
            'pages': pages
        }
    else:
        pages = request.session['form_' + str(form_obj.id)]['pages']
    page = FormPage.objects.filter(id=pages[(request.session['form_' + str(form_obj.id)]['current_page'] - 1)]).first()
    context = {
        'item': form_obj,
        'page': page,
        'current_page': request.session['form_'+ str(form_obj.id)]['current_page'],
        'count_pages': request.session['form_'+ str(form_obj.id)]['count_pages'],
        'pages': request.session['form_'+ str(form_obj.id)]['pages'],
    }
    data = {
        'template': render_to_string('forms/__partials/formrendered.html', context=context, request=request), 
    }
    return JsonResponse(data)

def handle_form(request):
    form = request.POST.get('form')
    form_obj = Form.objects.filter(id=form).first()
    page_session_obj = request.session['form_' + str(form_obj.id)] 
    print(request.session['form_'+ str(form_obj.id)])
    current_page_obj = FormPage.objects.filter(id=(page_session_obj['pages'][page_session_obj['current_page'] - 1])).first()
    if form_obj:
        fields = {}
        for field in current_page_obj.elements.all():
            if field.type == 'security_honeypot':
                fields[field.type + '-' + str(field.id)] = request.POST.get(field.type + '-' + str(field.id))
                fields[field.type + '-hidden' + '-' + str(field.id) ] = request.POST.get(field.type + '-hidden' + '-' + str(field.id) )
            else:
                fields[field.type + '-' + str(field.id)] = request.POST.get(field.type + '-' + str(field.id))
        if not 'form_entry_' + str(form_obj.id) in request.session:
            request.session['form_entry_' + str(form_obj.id)] = {page_session_obj['pages'][page_session_obj['current_page'] - 1]: fields}
        elif not page_session_obj['current_page'] in request.session['form_entry_' + str(form_obj.id)]:
            request.session['form_entry_' + str(form_obj.id)][page_session_obj['current_page']] = fields
        else:
            form_entries = request.session['form_entry_' + str(form_obj.id)]
            form_entries.append(fields)
            request.session['form_entry_' + str(form_obj.id)] = form_entries
        if page_session_obj['current_page'] >= page_session_obj['count_pages']:
            #No next page so time to post value and check if security passed
            form_result = FormResult.objects.create(form=form_obj)
            for i in range(page_session_obj['count_pages']):
                for key, value in request.session['form_entry_' + str(form_obj.id)][page_session_obj['pages'][i]].items():
                    key_id = key.split('-')[-1]
                    key_type = key.split('-')[0]
                    if key_type == 'email_field':
                        request.session['visitor_email'] = value
                    if key_type == 'security_honeypot':
                        if not value or value == '' or value == None:
                            if form_result.entries.exists():
                                for entry in form_result.entries.all():
                                    entry.delete()
                            form_result.delete()
                            context = {
                                'item': form_obj,
                                'page': page,
                                'current_page': request.session['form_'+ str(form_obj.id)]['current_page'],
                                'count_pages': request.session['form_'+ str(form_obj.id)]['count_pages'],
                                'pages': request.session['form_'+ str(form_obj.id)]['pages'],
                            }
                            data = {
                                'template': render_to_string('forms/__partials/formrendered.html', context=context, request=request), 
                                'success': True
                            }
                            return JsonResponse(data)
                    else:
                        if form_obj.store_results:
                            form_element = FormElement.objects.filter(id=key_id).first()
                            form_result_field = FormResultField.objects.create(field=form_element, value=value, field_type=key_type, page=page_session_obj['pages'][i])
                            form_result.entries.add(form_result_field)
                        else:
                            if form_result.entries.exists():
                                for entry in form_result.entries.all():
                                    entry.delete()
                            form_result.delete()

                            if form_obj.send_mail:
                                send_admin_email(request, form_obj)
                                request.session['form_entry_' + str(form_obj.id)]['results_not_stored'] = 1
                            if form_obj.mail_sender_visitor:
                                send_visitor_email(request, form_obj)
                                request.session['form_entry_' + str(form_obj.id)]['results_not_stored'] = 1

            if form_obj.success_type == 'message':
                value = form_obj.success_message
            elif form_obj.success_type == 'action':
                value = form_obj.success_action
            elif form_obj.success_type == 'redirect':
                value = form_obj.success_url

            if form_obj.send_mail and not 'results_not_stored' in request.session['form_entry_' + str(form_obj.id)]:
                send_admin_email(request, form_obj)
            if form_obj.mail_sender_visitor and not 'results_not_stored' in request.session['form_entry_' + str(form_obj.id)]:
                send_visitor_email(request, form_obj)

            if 'form_entry_' + str(form_obj.id) in request.session:
                del request.session['form_entry_' + str(form_obj.id)]
            context = {
                'item': form_obj,
            }
            data = {
                'template': render_to_string('forms/__partials/formrendered.html', context=context, request=request), 
                'success': True,
                'action': form_obj.success_type,
                'value': value
            }
            return JsonResponse(data)
        else:
            #Next page render
            request.session['form_' + str(form_obj.id)]['current_page'] = page_session_obj['current_page'] + 1
            context = {
                'item': form_obj,
                'page': page,
                'current_page': request.session['form_'+ str(form_obj.id)]['current_page'],
                'count_pages': request.session['form_'+ str(form_obj.id)]['count_pages'],
                'pages': request.session['form_'+ str(form_obj.id)]['pages'],
            }
            data = {
                'template': render_to_string('forms/__partials/formrendered.html', context=context, request=request), 
            }
            return JsonResponse(data)

def send_visitor_email(request, form):
    if 'visitor_email' in request.session: 
        context = {
            'content_html': form.mail_visitor.content_html
        }
        html_message = render_to_string('mail/default.html', context=context, request=request)
        send([request.session['visitor_email']], form.mail_visitor_sender_email, form.mail_visitor, {'form': form}, form.mail_visitor.subject,
         form.mail_visitor.content_plain, html_message)

def send_admin_email(request, form):        
    context = {
        'content_html': form.mail_admin.content_html
    }
    html_message = render_to_string('mail/default.html', context=context, request=request)
    send([form.mail_recipient_email], form.mail_sender_email, form.mail_admin, {'form': form}, form.mail_admin.subject,
        form.mail_admin.content_plain, html_message)