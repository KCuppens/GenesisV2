import pytest
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ValidationError
from django.test import TestCase
from apps.dashboard.models import DashboardConfiguration


class DashboardConfigurationTestCase(TestCase):

	@pytest.mark.django_db
	def create_dash_conf(self, title='Test Dashboard',
					   method='count_files',
					   sort='position',
					   order='asc', **kwargs):
		return DashboardConfiguration.objects.create(
			title=title, method=method,
			sort=sort, order=order,
			**kwargs
		)

	def test_model_instance_type(self):
		dash_conf = self.create_dash_conf()
		self.assertIsInstance(dash_conf, DashboardConfiguration)

	def test_model_with_invalid_method_choice(self):
		with self.assertRaises(ValidationError):
			dash_conf = self.create_dash_conf(method='abc')
		self.assertIsInstance(dash_conf, DashboardConfiguration)

	def test_model_with_invalid_sort_choice(self):
		with self.assertRaises(ValidationError):
			dash_conf = self.create_dash_conf(sort='abc')
		self.assertIsInstance(dash_conf, DashboardConfiguration)

	def test_model_with_invalid_order_choice(self):
		with self.assertRaises(ValidationError):
			dash_conf = self.create_dash_conf(order='abc')
		self.assertIsInstance(dash_conf, DashboardConfiguration)

