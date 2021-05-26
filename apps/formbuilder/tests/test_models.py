import pytest
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.core.exceptions import ValidationError
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

class BaseModelTestCase(TestCase):

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


class FormModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		form = self.create_form()
		self.assertIsInstance(form, Form)

		with self.subTest(msg='Test name'):
			self.assertEqual(form.name, 'Test Form')

	def test_model_slug(self):
		form = self.create_form()
		self.assertEqual(form.slug, 'test-form')

	def test_create_form_with_wrong_success_type(self):
		with self.assertRaises(ValidationError):
			form = self.create_form(success_type='wrong_choice')

	@pytest.mark.django_db
	def test_form_m2m_page_field(self):
		formPage1 = self.create_form_page(name='Form Page 1')
		formPage2 = self.create_form_page(name='Form Page 2')
		form = self.create_form()
		form.pages.set([formPage1, formPage2])
		self.assertEqual(form.pages.count(), 2)

	@pytest.mark.django_db
	def test_model_revision(self):
		form = self.create_form()
		revision = FormRevision.objects.get(current_instance=form)
		self.assertIsInstance(revision, FormRevision)


	@pytest.mark.django_db
	def test_model_version(self):
		form = self.create_form()
		revision = FormRevision.objects.get(current_instance=form)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 1)

		with self.subTest():
			self.assertIsInstance(versions.first(), FormVersion)


class FormPageModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		form_page = self.create_form_page()
		self.assertIsInstance(form_page, FormPage)

		with self.subTest(msg='Test name'):
			self.assertEqual(form_page.name, 'Test Form Page')

	def test_model_slug(self):
		form_page = self.create_form_page()
		self.assertEqual(form_page.slug, 'test-form-page')

	@pytest.mark.django_db
	def test_elements_m2m_field(self):
		formElement1 = self.create_form_element(name='formElement1')
		formElement2 = self.create_form_element(name='formElement2')
		form_page = self.create_form_page()
		form_page.elements.set([formElement1.id, formElement2.id])
		self.assertEqual(form_page.elements.count(), 2)

class FormElementModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		form_element = self.create_form_element()
		self.assertIsInstance(form_element, FormElement)

		with self.subTest(msg='Test name'):
			self.assertEqual(form_element.name, 'Test Form Page Element')

	@pytest.mark.django_db
	def test_elements_m2m_field(self):
		option1 = self.create_form_element_option(name='option1')
		option2 = self.create_form_element_option(name='option2')
		form_element = self.create_form_element()
		form_element.options.set([option1.id, option2.id])
		self.assertEqual(form_element.options.count(), 2)