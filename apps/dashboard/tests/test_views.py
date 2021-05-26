import pytest
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import reverse
from apps.dashboard.models import DashboardConfiguration
from apps.dashboard.forms import DashboardConfigurationForm
from django.utils.translation import ugettext_lazy as _


class BaseViewTestCase(TestCase):

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

	@pytest.mark.django_db
	def setUp(self):
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.dash_conf = self.create_dash_conf()


class DashboardViewTestCase(BaseViewTestCase):
	'''
	test dashboard_view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'OverviewDashboardTestCase'
		super(DashboardViewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	@pytest.mark.django_db
	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'dashboard/dashboard.html')
		with self.subTest():
			self.assertTrue(resp.context['dashboard'])

class OverviewDashboardTestCase(BaseViewTestCase):
	'''
	test overview_dashboard
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewdashboard'
		super(OverviewDashboardTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	@pytest.mark.django_db
	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'dashboard/admin/index.html')
		with self.subTest():
			self.assertFalse(resp.context['dashboard'])


class AddDashboardTestCase(BaseViewTestCase):
	'''
	test add_article view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'adddashboard'
		super(AddDashboardTestCase, self).__init__(*args, **kwargs)

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
			self.assertTemplateUsed(resp, 'dashboard/admin/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'],
								  DashboardConfigurationForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewdashboard'))
		# with self.subTest():
		# 	self.assertContains(resp, 
		# 						_('The dashboard has been succesfully added!'))

	def test_view_post_request_valid_data(self):
		data = {
			'title': 'Test Dash',
			'method': 'count_files_by_type',
			'sort': 'position',
			'order': 'asc',
			'active': False
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewdashboard'))
		# with self.subTest():
		# 	self.assertContains(resp, 
		# 						 _('The dashboard has been succesfully added!'))


class EditDashboardTestCase(BaseViewTestCase):
	'''
	test edit_dashboard view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'editdashboard'
		super(EditDashboardTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.dash_conf.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.dash_conf.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'dashboard/admin/edit.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], 
								  DashboardConfigurationForm)
		with self.subTest():
			self.assertIsInstance(resp.context['dashboard'],
								  DashboardConfiguration)

# 	def test_view_post_request_empty_data(self):
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=[self.article.id])
# 		resp = self.client.post(url, data={})

# 		with self.subTest():
# 			self.assertFalse(resp.context['form'].is_valid())
# 		with self.subTest():
# 			self.assertTemplateUsed(resp, 'news/edit.html')
# 		with self.subTest():
# 			gallery_error = resp.context['form'].errors['gallery'][0]
# 			self.assertEqual(gallery_error, _('Dit veld is verplicht.\t'))
# 		with self.subTest():
# 			image_error = resp.context['form'].errors['image'][0]
# 			self.assertEqual(image_error, _('Dit veld is verplicht.\t'))
# 		with self.subTest():
# 			title_error = resp.context['form'].errors['title'][0]
# 			self.assertEqual(title_error, _('Er moet altijd een titel zijn.\t'))

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		data = {
			'title': 'New Updated Dash Title',
			'method': self.dash_conf.method,
			'sort': self.dash_conf.sort,
			'order': self.dash_conf.order,
			'active': self.dash_conf.active
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.dash_conf.id])
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewdashboard'))
		# with self.subTest():
		# 	text = _('The dashboard has been succesfully changed!')
		# 	self.assertContains(resp, text)
		# with self.subTest(msg="Test changed data"):
		# 	self.assertEqual(self.dash_conf.title, 
		# 					 data['title'])


class DeleteAjaxDashboardModalTestCase(BaseViewTestCase):
	'''
	test delete_ajax_dasboard_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodaldashboard'
		super(DeleteAjaxDashboardModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(DashboardConfiguration.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(DashboardConfiguration.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.dash_conf.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Are you sure you want to delete?	')
			self.assertContains(resp, text)


class ToggleDashboardActivationViewTestCase(BaseViewTestCase):
	'''
	test toggle_dashboard_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'activate-dashboard'
		super(ToggleDashboardActivationViewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.dash_conf.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[id])
		with self.assertRaises(DashboardConfiguration.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.dash_conf.id])
		resp = self.client.get(url)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewdashboard'))


class DeleteDashboardTestCase(BaseViewTestCase):
	'''
	test delete_dashboard view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletedashboard'
		super(DeleteDashboardTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.dash_conf.pk])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.dash_conf.pk])
		resp = self.client.get(url)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewdashboard'))
		# with self.subTest():
		# 	text = 'The module has been succesfully deleted!'
		# 	self.assertContains(resp, text)

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(DashboardConfiguration.DoesNotExist):
			resp = self.client.get(url)
