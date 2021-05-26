import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from apps.modules.models import Module, Tab, ModulePage
from apps.modules.forms import ModulePageForm, ModuleForm, TabForm


class BaseFormTestCase(TestCase):

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
			module=self.create_module(),
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


class ModulePageFormTestCase(BaseFormTestCase):
	'''
	test ModulePageForm
	'''

	def test_with_empty_data(self):
		form = ModulePageForm(data={})
		self.assertTrue(form.is_valid())

	def test_with_partial_data(self):
		data = {
			'name': 'Test Module Page'
		}
		form = ModulePageForm(data=data)
		self.assertTrue(form.is_valid())

	def test_with_non_existent_route(self):
		data = {
			'name': 'Test Module Page',
			'route': '/page/test-module-page/'
		}
		form = ModulePageForm(data=data)
		# 'Form should be invalid. Non existent route.'
		self.assertFalse(form.is_valid())

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'name': 'Test Module Page',
			'route': '/page/test-module-page/', #assuming valid url
			'show_nav': False
		}
		form = ModulePageForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form, ModulePageForm)
		with self.subTest():
			self.assertIsInstance(form.save(), ModulePage)

	@pytest.mark.django_db
	def test_partial_update_with_instance(self):
		module_page = self.create_module_page(
			route='/page/test-module-page/',
			show_nav=False
		)
		data = {
			'name': 'New Module Page',
			'route': module_page.route, #assuming valid url
			'show_nav': module_page.show_nav
		}
		form = ModulePageForm(data=data, instance=module_page)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of value'):
			self.assertEqual(form.save().name, data['name'])



class ModuleFormTestCase(BaseFormTestCase):
	'''
	test ModuleForm
	'''

	def test_with_empty_data(self):
		form = ModuleForm(data={})
		self.assertTrue(form.is_valid())

	def test_with_partial_data(self):
		data = {
			'name': 'Test Module'
		}
		form = ModuleForm(data=data)
		self.assertTrue(form.is_valid())

	def test_with_non_existent_route(self):
		data = {
			'name': 'Test Module',
			'route': '/page/test-module/' # non existing route
		}
		form = ModuleForm(data=data)
		#'Form should be invalid. Non existent route.'
		self.assertFalse(form.is_valid())

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'name': 'Test Module Page',
			'route': '/page/test-module-page/', #assuming valid url
			'appname': 'Test App',
			'models': 'Test model'
		}
		form = ModuleForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form, ModuleForm)
		with self.subTest():
			self.assertIsInstance(form.save(), Module)

	@pytest.mark.django_db
	def test_partial_update_with_instance(self):
		module = self.create_module(
			route='/page/test-module-page/',
			appname='Test App',
			models='Test model'
		)
		data = {
			'name': 'New Test Module',
		}
		form = ModuleForm(data=data, instance=module)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of value'):
			self.assertEqual(form.save().name, data['name'])


class TabFormTestCase(BaseFormTestCase):
	'''
	test TabForm
	'''

	def test_with_empty_data(self):
		form = TabForm(data={})
		self.assertTrue(form.is_valid())

	def test_with_partial_data(self):
		data = {
			'name': 'Test Tab'
		}
		form = TabForm(data=data)
		self.assertTrue(form.is_valid())

	@pytest.mark.django_db
	def test_with_valid_data(self):
		module = self.create_module()
		data = {
			'name': 'Test Tab',
			'active': False,
			'module': [module.pk]
		}
		form = TabForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form, TabForm)
		with self.subTest():
			self.assertIsInstance(form.save(), Tab)

	@pytest.mark.django_db
	def test_partial_update_with_instance(self):
		tab = self.create_tab(
			active=False
		)
		data = {
			'name': 'New Test Tab',
		}
		form = TabForm(data=data, instance=tab)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of value'):
			self.assertEqual(form.save().name, data['name'])
