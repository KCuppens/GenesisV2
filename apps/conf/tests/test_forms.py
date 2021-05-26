import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from apps.conf.models import Configuration
from apps.conf.forms import ConfigurationValueForm, \
							ConfigurationForm


class ConfigurationValueFormTest(TestCase):
	'''
	test ConfigurationValueForm
	'''

	@pytest.mark.django_db
	def create_config(self, key_name='test_config',
					  title='Test Config', **kwargs):
		return Configuration.objects.create(
			key_name=key_name,
			title=title,
			**kwargs
		)

	def test_with_empty_data(self):
		form = ConfigurationValueForm(data={})
		self.assertFalse(form.is_valid())

	def test_with_invalid_data(self):
		form = ConfigurationValueForm(data={'value': True})
		self.assertFalse(form.is_valid())

	def test_with_valid_data(self):
		form = ConfigurationValueForm(data={'value': 'Test Value'})
		
		with self.subTest(msg='Test with value'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test Config instance'):
			self.assertIsInstance(form, ConfigurationValueForm)

	def test_with_instance(self):
		config = self.create_config(value='Test Value')
		form = ConfigurationValueForm(data={'value': 'New test value'},
									  instance=config)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of value'):
			self.assertEqual(form.save().value, 'New test value')


class ConfigurationFormTest(TestCase):
	'''
	test ConfigurationForm
	'''

	@pytest.mark.django_db
	def create_config(self, key_name='test_config',
					  title='Test Config', **kwargs):
		return Configuration.objects.create(
			key_name=key_name,
			title=title,
			**kwargs
		)

	def test_with_empty_data(self):
		form = ConfigurationForm(data={})
		self.assertFalse(form.is_valid())

	def test_with_invalid_data(self):
		form = ConfigurationForm(data={'value': 123})
		self.assertFalse(form.is_valid())

	def test_with_valid_data(self):
		data = {
			'key_name': 'test_config',
			'title': 'Test Config',
			'value': 'Test Value',
			'description': 'Test description',
			'conf_type': 'user',
		}
		form = ConfigurationForm(data=data)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test Config instance'):
			self.assertIsInstance(form.save(), Configuration)

	def test_with_instance(self):
		data = {
			'value': 'Test Value',
			'description': 'Test description',
			'conf_type': 'user',
		}
		config = self.create_config(**data)
		form = ConfigurationForm(data={'value': 'New test value'},
									  instance=config)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of value'):
			self.assertEqual(form.save().value, 'New test value')