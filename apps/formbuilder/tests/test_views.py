import pytest
import uuid
import json
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase, override_settings
from django.urls import reverse
from apps.formbuilder.models import (
    Form,
    FormPage,
    FormElement,
    FormResult,
    FormElementOption,
    FormResultField,
    FormRevision,
    FormVersion
)
from apps.formbuilder.forms import FormbuilderForm, FormPageForm
from django.utils.translation import ugettext_lazy as _


class BaseViewTestCase(TestCase):

    @pytest.mark.django_db
    def create_form(self, name='Test Form',
                      **kwargs):
        return Form.objects.create(
            name=name,
            **kwargs
        )

    @pytest.mark.django_db
    def create_form_page(self, name='Test Form Page',
                      **kwargs):
        return FormPage.objects.create(
            name=name,
            **kwargs
        )

    @pytest.mark.django_db
    def create_form_element(self, name='Test Form Page Element',
                      **kwargs):
        return FormElement.objects.create(
            name=name,
            **kwargs
        )

    @pytest.mark.django_db
    def create_form_element_option(self, name='Test Form Page Element Option',
                      **kwargs):
        return FormElementOption.objects.create(
            name=name,
            **kwargs
        )

    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_superuser('testuser', 
                                             'testuser@gmail.com'
                                             'testing321')
        self.form = self.create_form()
        self.form_page = self.create_form_page()
        self.form_element = self.create_form_element()
        self.form_element_option = self.create_form_element_option()


class AddFormTestCase(BaseViewTestCase):
    '''
    test add_form view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'addform'
        super(AddFormTestCase, self).__init__(*args, **kwargs)

    def test_view_get_request(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.get(url)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertTemplateUsed(resp, 'forms/add.html')
        with self.subTest():
            self.assertIsInstance(resp.context['form'], FormbuilderForm)

    def test_view_post_request_empty_data(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data={})

        with self.subTest():
            self.assertFalse(resp.context['form'].is_valid())

    def test_view_post_request_valid_data(self):
        data = {
            'name': 'Test Form',
            'active': False
        }

        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data, follow=True)

        with self.subTest():
            self.assertRedirects(resp, reverse('overviewform'))

    @pytest.mark.django_db
    def test_view_app_form_with_form_page(self):
        session = self.client.session
        session['form_page'] = [self.create_form_page().id]
        session.save()
        data = {
            'name': 'Test Form',
            'active': False
        }

        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data, follow=True)

        with self.subTest():
            self.assertRedirects(resp, reverse('overviewform'))

class EditFormTestCase(BaseViewTestCase):
    '''
    test editform view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'editform'
        super(EditFormTestCase, self).__init__(*args, **kwargs)

    @pytest.mark.django_db
    def test_view_get_request(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[self.form.id])
        resp = self.client.get(url)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertTemplateUsed(resp, 'forms/edit.html')
        with self.subTest():
            self.assertIsInstance(resp.context['form'], FormbuilderForm)
        with self.subTest():
            self.assertIsInstance(resp.context['instance'], Form)


    @pytest.mark.django_db
    def test_view_post_request_valid_data_without_formpage(self):
        data = {
            'name': 'New Updated Test Form',
            'active': self.form.active
        }

        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[self.form.id])
        resp = self.client.post(url, data=data, follow=True)

        with self.subTest():
            self.assertRedirects(resp, reverse('overviewform'))
        self.form.refresh_from_db()
        with self.subTest():
            self.assertEqual(self.form.name, data['name'])

    @pytest.mark.django_db
    def test_view_app_form_with_form_page(self):
        session = self.client.session
        session['form_page'] = [self.create_form_page().id]
        session.save()
        data = {
            'name': 'Test Form',
            'active': False
        }

        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[self.form.id])
        resp = self.client.post(url, data=data, follow=True)

        with self.subTest():
            self.assertRedirects(resp, reverse('overviewform'))
        with self.subTest():
            self.assertContains(resp, _('The form has been succesfully changed!'))
        self.form.refresh_from_db()
        # with self.subTest():
        #     self.assertEqual(self.form.pages.count(), 1)


class DeleteAjaxModalTestCase(BaseViewTestCase):
    '''
    test delete_ajax_modal view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'deletemodalform'
        super(DeleteAjaxModalTestCase, self).__init__(*args, **kwargs)

    def test_view_get_request(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)

        with self.assertRaises(Form.DoesNotExist):
            resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_view_post_request_empty_data(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)

        with self.assertRaises(Form.DoesNotExist):
            resp = self.client.post(url, 
                                    data={}, 
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')


    def test_view_post_request_valid_data(self):
        data = {
            'id': self.form.id
        }

        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, 
                                data=data,
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            resp_data = json.loads(resp.content)
            text = 'Weet u zeker dat u wilt verwijderen?'
            self.assertIn(text, resp_data['template'])



class ToggleFormActivationViewTestCase(BaseViewTestCase):
    '''
    test toggle_form_activation_view
    '''
    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'activate-form'
        super(ToggleFormActivationViewTestCase, self).__init__(*args, **kwargs)

    def test_view_without_login(self):
        url = reverse(self.view_url_conf, args=[self.form.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_view_with_wrong_pk(self):
        id = uuid.uuid4()
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[id])
        with self.assertRaises(Form.DoesNotExist):
            resp = self.client.get(url)

    @pytest.mark.django_db
    def test_view_with_valid_pk(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[self.form.id])
        resp = self.client.get(url)
        with self.subTest(msg='Status code'):
            self.assertEqual(resp.status_code, 302)
        with self.subTest():
            self.assertRedirects(resp, reverse('overviewform'))
        self.form.refresh_from_db()
        with self.subTest():
            self.assertTrue(self.form.active)

class DeleteFormTestCase(BaseViewTestCase):
    '''
    test delete_form view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'deleteform'
        super(DeleteFormTestCase, self).__init__(*args, **kwargs)

    def test_view_without_login(self):
        url = reverse(self.view_url_conf, args=[self.form.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    @pytest.mark.django_db
    def test_view_get_request(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[self.form.id])
        resp = self.client.get(url)

        with self.subTest():
            self.assertRedirects(resp, reverse('overviewform'))
        self.form.refresh_from_db()
        with self.subTest():
            self.assertTrue(self.form.date_deleted)

    def test_view_post_request_wrong_pk(self):
        pk = uuid.uuid4()
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[pk])

        with self.assertRaises(Form.DoesNotExist):
            resp = self.client.get(url)

class ExportFormResultTestCase(BaseViewTestCase):
    '''
    test export_form_results view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url = 'export-results-form'
        super(ExportFormResultTestCase, self).__init__(*args, **kwargs)

    @pytest.mark.django_db
    def test_view_with_get_request(self):
        formpage = self.create_form_page()
        self.form.pages.set([formpage])

        self.client.force_login(self.user)
        url = reverse(self.view_url, args=[self.form.pk])
        resp = self.client.get(url)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            filename = 'export_form_result_' + datetime.now().strftime("%H:%M:%S") + '.xlsx'
            self.assertIn('attachment; filename=export_form_result', resp.get('Content-Disposition'))


class GetFormBuilderTestCase(BaseViewTestCase):
    '''
    test get_formbuilder view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'getformbuilder'
        super(GetFormBuilderTestCase, self).__init__(*args, **kwargs)

    @pytest.mark.django_db
    def test_view_get_request(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.get(url)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertContains(resp, 'Page 1')
        with self.subTest():
            self.assertEqual(FormPage.objects.filter(name='Page 1').count(), 1)

    def test_view_get_request_action_createpage(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        # with self.subTest():
        #     self.assertFalse(resp.json()['success'])

    @pytest.mark.django_db
    def test_view_post_request_action_createpage(self):
        data = {
            'name': 'New Form Page',
            'action': 'createpage'
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertEqual(FormPage.objects.all().count(), 2)

    @pytest.mark.django_db
    def test_view_get_request_action_editpage(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf) + f'?action=editpage&page={self.form_page.id}'
        resp = self.client.get(url)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)


    @pytest.mark.django_db
    def test_view_post_request_action_editpage(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()
        data = {
            'name': 'New Updated Page',
            'action': 'editpage',
            'page': self.form_page.id
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertTrue(resp.json()['success'])
        self.form_page.refresh_from_db()
        with self.subTest():
            self.assertEqual(self.form_page.name, data['name'])

    @pytest.mark.django_db
    def test_view_post_request_action_deletepagemodal(self):
        session = self.client.session
        session['form_page'] = self.form_page.id
        session.save()
        data = {
            'action': 'deletepagemodal',
            'page': self.form_page.id
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertIn('De beslissing is aan u\t', resp.json()['title'])


    @pytest.mark.django_db
    def test_view_post_request_action_deletepage(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()
        data = {
            'action': 'deletepage',
            'page': self.form_page.id
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)


    @pytest.mark.django_db
    def test_view_post_request_action_addfield(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()
        data = {
            'action': 'addfield',
            'page': self.form_page.id,
            'field': FormElement.TYPE_TEXT_FIELD
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertIn('Label', resp.json()['template'])
        self.form_page.refresh_from_db()
        with self.subTest():
            self.assertEqual(self.form_page.elements.count(), 1)

    @pytest.mark.django_db
    def test_view_post_request_action_addfield_mutiradiofield(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()
        data = {
            'action': 'addfield',
            'page': self.form_page.id,
            'field': FormElement.TYPE_MULTI_RADIO_FIELD
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertIn('Label', resp.json()['template'])
        self.form_page.refresh_from_db()
        with self.subTest():
            self.assertEqual(self.form_page.elements.count(), 1)
        form_element = self.form_page.elements.all().first()
        with self.subTest(msg='Counting options in form_element'):
            self.assertEqual(form_element.options.count(), 3)
        with self.subTest():
            self.assertIn('Multi', resp.json()['template'])

    @pytest.mark.django_db
    def test_view_post_request_action_sortfields(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()

        formElement1 = self.create_form_element(name='elem1',
                                                type=FormElement.TYPE_MULTI_RADIO_FIELD,
                                                position=1)
        formElement2 = self.create_form_element(name='elem2',
                                                type=FormElement.TYPE_MULTI_RADIO_FIELD,
                                                position=2)
        self.form_page.elements.set([formElement1, formElement2])
        data = {
            'action': 'sortfields',
            'page': self.form_page.id,
            'field': FormElement.TYPE_MULTI_RADIO_FIELD,
            'item': f'item[]={formElement2.id}&item[]={formElement1.id}'
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertIn('Label', resp.json()['template'])
        formElement1.refresh_from_db()
        formElement2.refresh_from_db()
        with self.subTest(msg='formElement1 position'):
            self.assertEqual(formElement1.position, 2)
        with self.subTest(msg='formElement2 position'):
            self.assertEqual(formElement2.position, 1)

    @pytest.mark.django_db
    def test_view_post_request_action_sortfieldoptions(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()

        formElement1 = self.create_form_element(name='elem1',
                                                type=FormElement.TYPE_MULTI_RADIO_FIELD)

        formElementOp1 = self.create_form_element_option(name='elemOp1')
        formElementOp2 = self.create_form_element_option(name='elemOp2')

        formElement1.options.set([formElementOp1, formElementOp2])

        self.form_page.elements.set([formElement1])
        data = {
            'action': 'sortfieldoptions',
            'page': self.form_page.id,
            'field': FormElement.TYPE_MULTI_RADIO_FIELD,
            'item': f'item[]={formElementOp2.id}&item[]={formElementOp1.id}'
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertIn('Label', resp.json()['template'])
        formElementOp1.refresh_from_db()
        formElementOp2.refresh_from_db()
        with self.subTest(msg='formElement1 position'):
            self.assertEqual(formElementOp1.position, 2)
        with self.subTest(msg='formElement2 position'):
            self.assertEqual(formElementOp2.position, 1)

    @pytest.mark.django_db
    def test_view_post_request_action_deletefield(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()

        field = self.create_form_element()
        data = {
            'action': 'deletefield',
            'page': self.form_page.id,
            'field': field.id
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest(msg='Test if field exists'):
            self.assertEqual(FormElement.objects.filter(id=field.id).count(), 0)

    @pytest.mark.django_db
    def test_view_post_request_action_deletefieldoption(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()

        fieldOption = self.create_form_element_option()
        data = {
            'action': 'deletefieldoption',
            'page': self.form_page.id,
            'option': fieldOption.id
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest(msg='Test if field option exists'):
            self.assertEqual(FormElementOption.objects.filter(id=fieldOption.id).count(), 0)

    @pytest.mark.django_db
    def test_view_post_request_action_addfieldoption(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()

        formElement1 = self.create_form_element(name='elem1',
                                                type=FormElement.TYPE_MULTI_RADIO_FIELD)

        formElementOp1 = self.create_form_element_option(name='elemOp1')
        formElementOp2 = self.create_form_element_option(name='elemOp2')

        formElement1.options.set([formElementOp1, formElementOp2])
        data = {
            'action': 'addfieldoption',
            'page': self.form_page.id,
            'field': formElement1.id,
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        formElement1.refresh_from_db()
        with self.subTest(msg='Test if field option added'):
            self.assertEqual(formElement1.options.count(), 3)

    @pytest.mark.django_db
    def test_view_post_request_action_savecolsizefield(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()

        formElement1 = self.create_form_element(name='elem1',
                                                type=FormElement.TYPE_MULTI_RADIO_FIELD)

        formElementOp1 = self.create_form_element_option(name='elemOp1')
        formElementOp2 = self.create_form_element_option(name='elemOp2')

        formElement1.options.set([formElementOp1, formElementOp2])
        data = {
            'action': 'addfieldoption',
            'page': self.form_page.id,
            'field': formElement1.id,
            'colsize': _('Halve kolom')
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        # formElement1.refresh_from_db()
        # with self.subTest(msg='Test if field colsize'):
        #     self.assertEqual(formElement1.col_size,  'half')

    @pytest.mark.django_db
    def test_view_post_request_action_savefield(self):
        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()

        formElement1 = self.create_form_element(name='elem1',
                                                type=FormElement.TYPE_MULTI_RADIO_FIELD)

        formElementOp1 = self.create_form_element_option(name='elemOp1')
        formElementOp2 = self.create_form_element_option(name='elemOp2')

        # formElement1.options.set([formElementOp1, formElementOp2])
        data = {
            'action': 'savefield',
            'page': self.form_page.id,
            'field': formElement1.id,
            'label': 'First Name',
            'placeholder': 'Enter first name',
        }
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        formElement1.refresh_from_db()
        with self.subTest(msg='Test label'):
            self.assertEqual(formElement1.label, 'First Name')
        with self.subTest(msg='Test placeholder'):
            self.assertEqual(formElement1.placeholder, 'Enter first name')
        # with self.subTest():
        #     self.assertIn('First Name', resp.json()['template'])
        # with self.subTest():
        #     self.assertIn('Enter first name', resp.json()['template'])


class RenderFormTestCase(BaseViewTestCase):
    '''
    test render_form view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'previewform'
        super(RenderFormTestCase, self).__init__(*args, **kwargs)

    @pytest.mark.django_db
    def test_view_get_request(self):
        self.form.pages.set([self.form_page])
        formElement1 = self.create_form_element(name='elem1',
                                                type=FormElement.TYPE_MULTI_RADIO_FIELD)
        formElement1.label = 'First Name'
        formElement1.placeholder = 'Enter First Name'
        formElement1.save()

        self.form_page.elements.set([formElement1.id])

        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.get(url)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            self.assertIn(self.form_page.name, resp.json()['template'])
        # with self.subTest():
        #     self.assertIn('Enter First Name', resp.json()['template'])



class GetFormTestCase(BaseViewTestCase):
    '''
    test get_form view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'getform'
        super(GetFormTestCase, self).__init__(*args, **kwargs)

    @pytest.mark.django_db
    def test_view_get_request(self):
        self.form.pages.set([self.form_page])
        formElement1 = self.create_form_element(name='elem1',
                                                type=FormElement.TYPE_MULTI_RADIO_FIELD)
        formElement1.label = 'First Name'
        formElement1.placeholder = 'Enter First Name'
        formElement1.save()

        self.form_page.elements.set([formElement1.id])
        self.form.pages.set([self.form_page.id])

        session = self.client.session
        session['form_page'] = [self.form_page.id]
        session.save()
        data = {'form': self.form.id}

        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        # with self.subTest():
        #     self.assertIn(self.form_page.name, resp.json()['template'])


class GetVersionAjaxModalTestCase(BaseViewTestCase):
    '''
    test get_version_ajax_modal view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'formversionmodal'
        super(GetVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

    def test_view_without_login(self):
        url = reverse(self.view_url_conf)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_view_get_request(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)

        with self.assertRaises(Form.DoesNotExist):
            resp = self.client.get(url)

    def test_view_post_request_empty_data(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)

        with self.assertRaises(Form.DoesNotExist):
            resp = self.client.post(url, 
                                    data={})


    def test_view_post_request_valid_data(self):
        data = {
            'id': self.form.id
        }

        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, 
                                data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            text = _('Versions')
            self.assertContains(resp, text)


class DeleteVersionAjaxModalTestCase(BaseViewTestCase):
    '''
    test get_delete_version_ajax_modal view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'formdeleteversionmodal'
        super(DeleteVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

    @pytest.mark.django_db
    def test_view_post_request_valid_data(self):
        revision = FormRevision.objects.get(current_instance=self.form)
        version = revision.versions.all().first()
        data = {
            'id': version.id
        }

        self.client.force_login(self.user)
        url = reverse(self.view_url_conf)
        resp = self.client.post(url, 
                                data=data)

        with self.subTest():
            self.assertEqual(resp.status_code, 200)
        with self.subTest():
            text = _('Are you sure you want to delete this version?')
            self.assertContains(resp, text)


class SelectVersionTestCase(BaseViewTestCase):
    '''
    test select_version view
    '''

    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'formselectversion'
        super(SelectVersionTestCase, self).__init__(*args, **kwargs)

    @pytest.mark.django_db
    def test_select_version_with_valid_version_id(self):
        revision = FormRevision.objects.get(current_instance=self.form)
        version = revision.versions.all().first()
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[version.id])
        resp = self.client.get(url)

        with self.subTest():
            self.assertRedirects(resp, reverse('overviewform'))
        with self.subTest():
            self.assertTrue(version.is_current)

    def test_select_version_with_wrong_id(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[123])
        with self.assertRaises(FormVersion.DoesNotExist):
            resp = self.client.get(url)


class DeleteVersionTestCase(BaseViewTestCase):
    '''
    test delete_version view
    '''
    def __init__(self, *args, **kwargs):
        self.view_url_conf = 'formdeleteversion'
        super(DeleteVersionTestCase, self).__init__(*args, **kwargs)

    @pytest.mark.django_db
    def test_delete_version_with_valid_version_id(self):
        revision = FormRevision.objects.get(current_instance=self.form)
        version = revision.versions.all().first()
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[version.id])
        resp = self.client.get(url, follow=True)
        
        with self.subTest():
            self.assertRedirects(resp, reverse('overviewform'))
        with self.subTest(msg='Test contains'):
            self.assertContains(resp, _('The version has been successfully deleted!'))

    def test_delete_version_with_wrong_version_id(self):
        self.client.force_login(self.user)
        url = reverse(self.view_url_conf, args=[123])

        with self.assertRaises(FormVersion.DoesNotExist):
            resp = self.client.get(url)