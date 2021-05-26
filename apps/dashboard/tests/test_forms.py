import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from apps.dashboard.models import DashboardConfiguration
from apps.dashboard.forms import DashboardConfigurationForm


class DashboardConfigurationFormTest(TestCase):
	'''
	test DashboardConfigurationForm
	'''

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

	def test_with_empty_data(self):
		form = DashboardConfigurationForm(data={})
		self.assertFalse(form.is_valid())

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'title': 'Test Dash',
			'method': 'count_files_by_type',
			'sort': 'position',
			'order': 'asc',
			'active': False
		}
		form = DashboardConfigurationForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form, DashboardConfigurationForm)
		with self.subTest():
			self.assertIsInstance(form.save(), DashboardConfiguration)

	def test_with_instance(self):
		dash_conf = self.create_dash_conf()
		data = {
			'title': 'New Updated Dashboard',
			'method': dash_conf.method,
			'sort': dash_conf.sort,
			'order': dash_conf.order,
			'active': False
		}
		form = DashboardConfigurationForm(data=data, instance=dash_conf)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of value'):
			self.assertEqual(form.save().title, data['title'])
