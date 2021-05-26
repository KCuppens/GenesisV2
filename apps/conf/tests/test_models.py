import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from apps.conf.models import Configuration


class ConfModelTest(TestCase):

	@pytest.mark.django_db
	def create_config(self, key_name='test_config',
					  title='Test Config', **kwargs):
		return Configuration.objects.create(
			key_name=key_name,
			title=title,
			**kwargs
		)

	def test_config_model_basic(self):
		config = self.create_config()
		self.assertEqual(config.key_name, 'test_config')

		with self.subTest(msg='Test config title'):
			self.assertEqual(config.title, 'Test Config')

	def test_config_model_with_value(self):
		config = self.create_config(value='Test Value')
		self.assertEqual(config.value, 'Test Value')

	def test_config_model_with_description(self):
		desc = 'Test Description'
		config = self.create_config(description=desc)
		self.assertEqual(config.description, desc)

	def test_config_model_with_conf_type(self):
		config = self.create_config(conf_type='Gebruiker')
		self.assertEqual(config.conf_type, 'Gebruiker')

	def test_config_model_with_type(self):
		config = self.create_config(type='Textvalue')
		self.assertEqual(config.type, 'Textvalue')