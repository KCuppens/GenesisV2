import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
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
from apps.formbuilder.forms import FormPageForm



class FormPageFormTest(TestCase):
	'''
	test FormPageForm
	'''

	def test_with_empty_data(self):
		form = FormPageForm(data={})
		self.assertFalse(form.is_valid())

	def test_with_empty_name(self):
		data = {
			'name': '' # empty name
		}
		form = FormPageForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest():
			self.assertEqual(form.errors['name'][0], 
							_('You have to enter a name'))

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'name': 'Test Form Page'
		}
		form = FormPageForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form.save(), FormPage)

