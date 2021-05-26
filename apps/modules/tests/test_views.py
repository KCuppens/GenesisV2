import pytest
import uuid
import json
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import reverse
from apps.modules.models import (
	Module,
	ModulePage,
	Tab,
	ModuleRevision,
	ModuleVersion,
	TabRevision,
	TabVersion
)
from apps.modules.forms import ModulePageForm, ModuleForm, TabForm
from django.utils.translation import ugettext_lazy as _


class BaseViewTestCase(TestCase):

	@pytest.mark.django_db
	def create_module(self, name='Test Module',
					  **kwargs):
		return Module.objects.create(
			name=name,
			**kwargs
		)

	@pytest.mark.django_db
	def create_module_page(self, name='Test Module Page',
					  **kwargs):
		return ModulePage.objects.create(
			name=name,
			**kwargs
		)

	@pytest.mark.django_db
	def create_tab(self, name='Test Tab',
					  **kwargs):
		module = self.create_module()
		tab =  Tab.objects.create(
			name=name,
			**kwargs
		)
		tab.modules.set([self.create_module()])
		tab.save()
		return tab

	@pytest.mark.django_db
	def setUp(self):
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.module = self.create_module()
		self.module_page = self.create_module_page(module=self.module)
		self.tab = self.create_tab()


class OverviewTabTestCase(BaseViewTestCase):
	'''
	test overview_tab view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewtab'
		super(OverviewTabTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'tabs/index.html')
		with self.subTest():
			self.assertContains(resp, _(self.tab.name))
		with self.subTest():
			self.assertTrue(resp.context['tabs'])


class AddTabTestCase(BaseViewTestCase):
	'''
	test add_tab view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addtab'
		super(AddTabTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'tabs/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], TabForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewtab'))

	def test_view_post_request_valid_data(self):
		data = {
			'name': 'Test Tab',
			'active': False
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewtab'))


class EditTabTestCase(BaseViewTestCase):
	'''
	test edit_tab view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'edittab'
		super(EditTabTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.tab.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.tab.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'tabs/edit.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], TabForm)
		with self.subTest():
			self.assertIsInstance(resp.context['tab'], Tab)

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		new_module = self.create_module(name='New Module')
		data = {
			'name': self.tab.name,
			'active': self.tab.active,
			'modules': [new_module.pk]
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.tab.id])
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewtab'))
		with self.subTest(msg="Test changed data"):
			self.assertEqual(self.tab.modules.count(), 1)


class DeleteAjaxTabModalTestCase(BaseViewTestCase):
	'''
	test delete_ajax_tab_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodaltab'
		super(DeleteAjaxTabModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Tab.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Tab.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.tab.id
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



class ToggleTabActivationViewTestCase(BaseViewTestCase):
	'''
	test toggle_Tab_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'activate-tabs'
		super(ToggleTabActivationViewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.tab.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)


	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[id])
		with self.assertRaises(Tab.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.tab.id])
		resp = self.client.get(url)
		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewtab'))
		self.tab.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.tab.active)

class DeleteTabTestCase(BaseViewTestCase):
	'''
	test delete_tab view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletetab'
		super(DeleteTabTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.tab.pk])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.tab.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewtab'))

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Tab.DoesNotExist):
			resp = self.client.get(url)

class OverviewModulesTestCase(BaseViewTestCase):
	'''
	test overview_modules view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewmodules'
		super(OverviewModulesTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'modules/index.html')
		with self.subTest():
			self.assertContains(resp, _(self.module.name))
		with self.subTest():
			self.assertTrue(resp.context['modules'])


class AddModuleTestCase(BaseViewTestCase):
	'''
	test add_modules view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addmodules'
		super(AddModuleTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'modules/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], ModuleForm)
		with self.subTest():
			self.assertTrue(resp.context['formset'])

	def test_view_post_request_empty_data(self):
		data = {
			# management_form data
	        'form-INITIAL_FORMS': '0',
	        'form-TOTAL_FORMS': '0',
	        'form-MAX_NUM_FORMS': '',
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))

	def test_view_post_request_valid_data(self):
		data = {
			'name': 'Test Module',
			'route': '/page/test-module/', # non existing route
			'appname': 'Test Appname',
			'models': 'Test model',

			# management_form data
	        'form-INITIAL_FORMS': '0',
	        'form-TOTAL_FORMS': '2',
	        'form-MAX_NUM_FORMS': '',

	        # First ModulePage data
	        'form-0-name': 'Test ModulePage 1',
	        'form-0-route': '/test/module_page_1/',
	        'form-0-show_nav': False,

	        # Second ModulePage data
	        'form-1-name': 'Test ModulePage 2',
	        'form-1-route': '/test/module_page_2/',
	        'form-1-show_nav': False,
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))


class EditModuleTestCase(BaseViewTestCase):
	'''
	test edit_modules view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'editmodules'
		super(EditModuleTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.module.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	@pytest.mark.django_db
	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.module.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'modules/edit.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], ModuleForm)
		with self.subTest():
			self.assertIsInstance(resp.context['module'], Module)
		with self.subTest():
			self.assertTrue(resp.context['modulesPages'])
		with self.subTest():
			self.assertTrue(resp.context['formset'])

	@pytest.mark.django_db
	def test_view_post_partial_update_modules_page(self):
		data = {
			'name': self.module.name,
			'route': self.module.route or '',
			'appname': self.module.appname or '',
			'models': self.module.models or '',

			# management_form data
	        'form-INITIAL_FORMS': '0',
	        'form-TOTAL_FORMS': '1',
	        'form-MAX_NUM_FORMS': '',

	        # First ModulePage data
	        'form-0-name': 'Updated Modules Page',
	        'form-0-route': self.module_page.route or '',
	        'form-0-show_nav': self.module_page.show_nav or ''
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.module.id])
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))
		self.module_page.refresh_from_db()
		with self.subTest(msg="Test changed data"):
			self.assertEqual(self.module_page.name, data['form-0-name'])

	@pytest.mark.django_db
	def test_view_post_create_new_modules_page(self):
		data = {
			'name': self.module.name,
			'route': self.module.route or '',
			'appname': self.module.appname or '',
			'models': self.module.models or '',

			# management_form data
	        'form-INITIAL_FORMS': '0',
	        'form-TOTAL_FORMS': '1',
	        'form-MAX_NUM_FORMS': '',

	        # First ModulePage data
	        'form-0-name': self.module_page.name,
	        'form-0-route': self.module_page.route or '',
	        'form-0-show_nav': self.module_page.show_nav or '',

	        # Second ModulePage data
	        'form-1-name': 'Test ModulePage 2',
	        'form-1-route': '/test/module_page_2/',
	        'form-1-show_nav': False,
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.module.id])
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))
		with self.subTest(msg="Test changed data"):
			self.assertEqual(ModulePage.objects.all().count(), 2)


class DeleteAjaxModulesModalTestCase(BaseViewTestCase):
	'''
	test delete_ajax_modules_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodalmodules'
		super(DeleteAjaxModulesModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Module.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Module.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.module.id
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


class DeleteModulesTestCase(BaseViewTestCase):
	'''
	test delete_modules view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodules'
		super(DeleteModulesTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.module.pk])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_delete_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.module.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Module.DoesNotExist):
			resp = self.client.get(url)


class DeleteModulesPagesTestCase(BaseViewTestCase):
	'''
	test delete_modules_pages view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletepagemodules'
		super(DeleteModulesPagesTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.module_page.pk])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_delete_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.module_page.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(ModulePage.DoesNotExist):
			resp = self.client.get(url)

class ToggleModuleActivationViewTestCase(BaseViewTestCase):
	'''
	test toggle_module_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'activate-modules'
		super(ToggleModuleActivationViewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.module.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)


	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[id])
		with self.assertRaises(Module.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.module.id])
		resp = self.client.get(url)
		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))
		self.module.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.module.active)

class GetVersionAjaxModalTestCase(BaseViewTestCase):
	'''
	test get_version_ajax_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'moduleversionmodal'
		super(GetVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=['module'])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_mode_module_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['module'])

		with self.assertRaises(Module.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_tab_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['tab'])

		with self.assertRaises(Tab.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_module_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['module'])

		with self.assertRaises(Module.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_tab_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['tab'])

		with self.assertRaises(Tab.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_mode_module_post_request_valid_data(self):
		data = {
			'id': self.module.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['module'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Versions')
			self.assertContains(resp, text)

	def test_view_mode_tab_post_request_valid_data(self):
		data = {
			'id': self.tab.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['tab'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

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
		self.view_url_conf = 'moduledeleteversionmodal'
		super(DeleteVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=['module'])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	@pytest.mark.django_db
	def test_view_mode_module_post_request_valid_data(self):
		revision = ModuleRevision.objects.get(current_instance=self.module)
		version = revision.versions.all().first()
		data = {
			'id': version.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['module'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Are you sure you want to delete this version?')
			self.assertContains(resp, text)

	@pytest.mark.django_db
	def test_view_mode_tab_post_request_valid_data(self):
		revision = TabRevision.objects.get(current_instance=self.tab)
		version = revision.versions.all().first()
		data = {
			'id': version.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['tab'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

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
		self.view_url_conf = 'moduleselectversion'
		super(SelectVersionTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_select_version_mode_module_with_valid_version_id(self):
		revision = ModuleRevision.objects.get(current_instance=self.module)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['module', version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('overviewmodules'))
		version.refresh_from_db()
		with self.subTest():
			self.assertTrue(version.is_current)

	@pytest.mark.django_db
	def test_select_version_mode_tab_with_valid_version_id(self):
		revision = TabRevision.objects.get(current_instance=self.tab)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['tab', version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('overviewtab'))
		version.refresh_from_db()
		with self.subTest():
			self.assertTrue(version.is_current)

	def test_select_version_mode_module_with_wrong_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['module', id])
		resp = self.client.get(url)
		self.assertRedirects(resp, reverse('overviewmodules'))


	def test_select_version_mode_tab_with_wrong_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['tab', id])
		resp = self.client.get(url)
		self.assertRedirects(resp, reverse('overviewtab'))


class DeleteVersionTestCase(BaseViewTestCase):
	'''
	test delete_version view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'moduledeleteversion'
		super(DeleteVersionTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_delete_version_mode_module_with_valid_version_id(self):
		revision = ModuleRevision.objects.get(current_instance=self.module)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['module', version.id])
		resp = self.client.get(url, follow=True)
		
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))
		with self.subTest(msg='Test contains'):
			self.assertContains(resp, _('De versie is succesvol verwijderd'))

	@pytest.mark.django_db
	def test_delete_version_mode_tab_with_valid_version_id(self):
		revision = TabRevision.objects.get(current_instance=self.tab)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['tab', version.id])
		resp = self.client.get(url, follow=True)
		
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewtab'))
		with self.subTest(msg='Test contains'):
			self.assertContains(resp, _('De versie is succesvol verwijderd'))

	def test_delete_version_mode_module_with_wrong_version_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['module', id])

		resp = self.client.get(url, follow=True)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmodules'))

	def test_delete_version_mode_tab_with_wrong_version_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['tab', id])

		resp = self.client.get(url)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewtab'))
