import pytest
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import reverse
from apps.conf.models import Configuration
from apps.conf.forms import ConfigurationForm, ConfigurationValueForm
from django.utils.translation import ugettext_lazy as _


class BaseConfigTestCase(TestCase):

	@pytest.mark.django_db
	def create_config(self, key_name='test_config',
					  title='Test Config', **kwargs):
		return Configuration.objects.create(
			key_name=key_name,
			title=title,
			**kwargs
		)

	@pytest.mark.django_db
	def setUp(self):
		# self.client = Client()
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.config = self.create_config()


class OverviewTestCase(BaseConfigTestCase):
	'''
	test overview_conf view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewconf'
		super(OverviewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'conf/index.html')
		with self.subTest():
			self.assertContains(resp, _('Configuration overview'))
		with self.subTest():
			self.assertTrue(resp.context)


class AddConfTestCase(BaseConfigTestCase):
	'''
	test add_conf view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addconf'
		super(AddConfTestCase, self).__init__(*args, **kwargs)

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
			self.assertTemplateUsed(resp, 'conf/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], ConfigurationForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())
		with self.subTest():
			self.assertTemplateUsed(resp, 'conf/add.html')


	def test_view_post_request_valid_data(self):
		data = {
			'key_name': 'test_config',
			'title': 'Test Config',
			'value': 'Test Value',
			'description': 'Test description',
			'conf_type': 'user',
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewconf'))
		with self.subTest():
			text = _('The configuration has been succesfully added!')
			self.assertContains(resp, text)

	def test_view_post_request_invalid_data(self):
		data = {
			'key_name': 'test_config',
			'title': 'Test Config',
			'value': 'Test Value',
			'description': 'Test description',
			'conf_type': 'Gebruiker', #invalid choice
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(KeyError):
			resp = self.client.post(url, data=data)


class SaveConfTestCase(BaseConfigTestCase):
	'''
	test save_conf view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'saveconf'
		super(SaveConfTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewconf'))

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(IndexError):
			resp = self.client.post(url, data={})

	def test_view_post_request_valid_data(self):
		data = {
			'conf-value': [self.config.value]
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewconf'))


class DeleteAjaxConfModalTestCase(BaseConfigTestCase):
	'''
	test delete_ajax_conf_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodalconf'
		super(DeleteAjaxConfModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Configuration.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Configuration.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.config.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)


class DeleteConfTestCase(BaseConfigTestCase):
	'''
	test delete_conf view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deleteconf'
		super(DeleteConfTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.config.id])
		resp = self.client.get(url, args=[self.config.pk])
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.config.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewconf'))
		with self.subTest():
			text = _('The configuration has been succesfully deleted!')
			self.assertContains(resp, text)

	def test_view_post_request_invalid_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Configuration.DoesNotExist):
			resp = self.client.get(url)
