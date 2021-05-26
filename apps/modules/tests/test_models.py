import pytest
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.modules.models import (
	Module,
	ModulePage,
	Tab,
	ModuleRevision,
	ModuleVersion,
	TabRevision,
	TabVersion
)

class BaseModelTestCase(TestCase):

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
		module = self.create_module()
		return ModulePage.objects.create(
			name=name,
			module=module,
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


class ModuleModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		module = self.create_module()
		self.assertIsInstance(module, Module)

		with self.subTest(msg='Test title'):
			self.assertEqual(module.name, 'Test Module')

	def test_model_slug(self):
		module = self.create_module()
		self.assertEqual(module.slug, 'test-module')

	@pytest.mark.django_db
	def test_model_revision(self):
		module = self.create_module()
		revision = ModuleRevision.objects.get(current_instance=module)
		self.assertIsInstance(revision, ModuleRevision)


	@pytest.mark.django_db
	def test_model_version(self):
		module = self.create_module()
		revision = ModuleRevision.objects.get(current_instance=module)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 1)

		with self.subTest():
			self.assertIsInstance(versions.first(), ModuleVersion)


class ModulePageModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		module_page = self.create_module_page()
		self.assertIsInstance(module_page, ModulePage)

		with self.subTest(msg='Test title'):
			self.assertEqual(module_page.name, 'Test Module Page')

	def test_model_without_name(self):
		with self.assertRaises(ValidationError):
			module_page = self.create_module_page(name='')

	@pytest.mark.django_db
	def test_module_page_module_foreign_key(self):
		module_page = self.create_module_page()
		self.assertIsInstance(module_page.module, Module)


class TabModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		tab = self.create_tab()
		self.assertIsInstance(tab, Tab)

		with self.subTest(msg='Test Name'):
			self.assertEqual(tab.name, 'Test Tab')

	def test_model_slug(self):
		tab = self.create_tab()
		self.assertEqual(tab.slug, 'test-tab')

	@pytest.mark.django_db	
	def test_model_m2m_field(self):
		tab = self.create_tab()
		self.assertEqual(tab.modules.count(), 1)

		new_module = self.create_module(name='New Module')
		tab.modules.add(new_module)

		with self.subTest(msg='Test m2m field count'):
			self.assertEqual(tab.modules.count(), 2)

	@pytest.mark.django_db
	def test_model_revision(self):
		tab = self.create_tab()
		revision = TabRevision.objects.get(current_instance=tab)
		self.assertIsInstance(revision, TabRevision)


	@pytest.mark.django_db
	def test_model_version(self):
		tab = self.create_tab()
		revision = TabRevision.objects.get(current_instance=tab)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 2)

		with self.subTest():
			self.assertIsInstance(versions.first(), TabVersion)
