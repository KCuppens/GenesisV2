import pytest
import uuid
import json
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.user.forms import (
	UserForm, 
	GroupForm, 
	UserChangePasswordForm, 
	UserSetPasswordForm
)
User = get_user_model()
from django.utils.translation import ugettext_lazy as _


class BaseViewTestCase(TestCase):

	@pytest.mark.django_db
	def create_new_user(self, firstname='John',
						lastname='Doe',
						username='johndoe',
						email='johndoe@gmail.com',
					  	**kwargs):
		return User.objects.create(
			first_name=firstname,
			last_name=lastname,
			username=username,
			email=email,
			**kwargs
		)

	@pytest.mark.django_db
	def setUp(self):
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.new_user = self.create_new_user()


class OverviewUserTestCase(BaseViewTestCase):
	'''
	test overview_user view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewuser'
		super(OverviewUserTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_with_login_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'user/index.html')
		with self.subTest():
			self.assertContains(resp, _(self.new_user.first_name))
		with self.subTest():
			self.assertTrue(resp.context['users'])

	@pytest.mark.django_db
	def test_view_with_search_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url) + f'?search=John'
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'user/index.html')
		with self.subTest():
			self.assertContains(resp, _(self.new_user.first_name))
		with self.subTest():
			self.assertTrue(resp.context['users'])


class AddUserTestCase(BaseViewTestCase):
	'''
	test add_user view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'adduser'
		super(AddUserTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'user/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], UserForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'user/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], UserForm)
		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())

	def test_view_post_request_valid_data(self):
		data = {
			'firstname': 'NewTest',
			'lastname': 'User',
			'username': 'newtestuser',
			'email': 'newtestuser@gmail.com'
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewuser'))
		with self.subTest():
			self.assertContains(resp, _('The user has been succesfully added!'))


class ChangeUserPasswordTestCase(BaseViewTestCase):
	'''
	test change_user_password view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'changepassworduser'
		super(ChangeUserPasswordTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.new_user.pk])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'user/changepassword.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], UserChangePasswordForm)
		with self.subTest():
			self.assertIsInstance(resp.context['user'], User)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.new_user.pk])
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'user/changepassword.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], UserChangePasswordForm)
		with self.subTest():
			self.assertIsInstance(resp.context['user'], User)
		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())

	def test_view_post_request_valid_data(self):
		data = {
			'password': 'testing321'
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.new_user.pk])
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewuser'))
		with self.subTest():
			self.assertContains(resp, _('The password has been successfully changed!'))

class EditUserTestCase(BaseViewTestCase):
	'''
	test edit_user view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'edituser'
		super(EditUserTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.new_user.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'user/edit.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], UserForm)
		with self.subTest():
			self.assertIsInstance(resp.context['user'], User)

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		data = {
			'first_name': 'Adam',
			'last_name': self.new_user.last_name,
			'email': self.new_user.email,
			'username': self.new_user.username
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.new_user.id])
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewuser'))
		with self.subTest(msg="Test changed data"):
			self.assertContains(resp, _('The user has been succesfully changed!'))


class DeleteAjaxUserModalTestCase(BaseViewTestCase):
	'''
	test delete_ajax_user_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodaluser'
		super(DeleteAjaxUserModalTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(User.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(User.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.user.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			resp_data = json.loads(resp.content)
			text = 'Weet u zeker dat u wilt verwijderen?'
			self.assertIn(text, resp_data['template'])


class ToggleActivationViewTestCase(BaseViewTestCase):
	'''
	test toggle_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'activate-user'
		super(ToggleActivationViewTestCase, self).__init__(*args, **kwargs)

	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[123])
		with self.assertRaises(User.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.new_user.id])
		resp = self.client.get(url)
		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewuser'))
		self.new_user.refresh_from_db()
		with self.subTest():
			self.assertFalse(self.new_user.is_active)

class DeleteUserTestCase(BaseViewTestCase):
	'''
	test delete_user view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deleteuser'
		super(DeleteUserTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.new_user.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewuser'))
		with self.subTest():
			self.assertContains(resp, _('The user has been succesfully deleted!'))

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[123])

		with self.assertRaises(User.DoesNotExist):
			resp = self.client.get(url)

class OverviewGroupTestCase(BaseViewTestCase):
	'''
	test group_view view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewgroup'
		super(OverviewGroupTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_with_login_get_request(self):
		group = Group.objects.create(name='Test Group')
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'group/index.html')
		with self.subTest():
			self.assertTrue(resp.context['groups'])


class AddGroupTestCase(BaseViewTestCase):
	'''
	test add_group_view view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addgroup'
		super(AddGroupTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'group/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], GroupForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={}, follow=True)

		with self.subTest():
			self.assertTemplateUsed(resp, 'group/add.html')
		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())

	def test_view_post_request_valid_data(self):
		data = {
			'name': 'Test Group'
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewgroup'))
		with self.subTest():
			self.assertContains(resp, _('The group has been succesfully added!'))


class DeleteGroupTestCase(BaseViewTestCase):
	'''
	test delete_group_view view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletegroup'
		super(DeleteGroupTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_get_request(self):
		group = Group.objects.create(name='Test Group')
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[group.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewgroup'))
		with self.subTest():
			self.assertContains(resp, _('The group has been succesfully deleted!'))

	def test_view_post_request_wrong_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[123])

		with self.assertRaises(Group.DoesNotExist):
			resp = self.client.get(url)

class DeleteAjaxGroupModalTestCase(BaseViewTestCase):
	'''
	test delete_ajax_group_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodalgroup'
		super(DeleteAjaxGroupModalTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Group.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Group.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		group = Group.objects.create(name='Test Group')
		data = {
			'id': group.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			resp_data = json.loads(resp.content)
			text = 'Weet u zeker dat u wilt verwijderen?'
			self.assertIn(text, resp_data['template'])
