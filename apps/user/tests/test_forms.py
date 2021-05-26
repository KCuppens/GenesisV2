import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from apps.user.forms import (
	UserForm, 
	GroupForm
)

class UserFormTestCase(TestCase):
	'''
	test UserForm
	'''
	@pytest.mark.django_db
	def test_with_empty_data(self):
		form = UserForm(data={})
		self.assertFalse(form.is_valid())

	@pytest.mark.django_db
	def test_with_no_email(self):
		data = {
			'firstname': 'John',
			'lastname': 'Doe',
			'username': 'johndoe'
		}
		form = UserForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest(msg='Test email error'):
			self.assertEqual(form.errors['email'][0],
							 _('Please enter a emailaddress.'))

	@pytest.mark.django_db
	def test_with_no_username(self):
		data = {
			'firstname': 'John',
			'lastname': 'Doe',
			'email': 'johndoe@gmail.com'
		}
		form = UserForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest(msg='Test username error'):
			self.assertEqual(form.errors['username'][0],
							 _('Please enter a username.'))

	@pytest.mark.django_db
	def test_with_no_firstname_no_lastname(self):
		data = {
			'username': 'kenadams',
			'email': 'kenadams@gmail.com'
		}
		form = UserForm(data=data)

		with self.subTest():
			self.assertFalse(form.is_valid())
		with self.subTest(msg='Test firstname error'):
			self.assertEqual(form.errors['firstname'][0],
							 _('Please enter a firstname.'))
		with self.subTest(msg='Test firstname error'):
			self.assertEqual(form.errors['lastname'][0],
							 _('Please enter a lastname.'))

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'firstname': 'John',
			'lastname': 'Doe',
			'username': 'johndoe',
			'email': 'johndoe@gmail.com'
		}
		form = UserForm(data=data)
		self.assertTrue(form.is_valid())


class GroupFormTestCase(TestCase):
	'''
	GroupForm Testcases
	'''
	@pytest.mark.django_db
	def test_with_empty_data(self):
		form = GroupForm(data={})
		self.assertFalse(form.is_valid())

	@pytest.mark.django_db
	def test_with_only_name(self):
		form = GroupForm(data={'name': 'Test Group'})
		self.assertTrue(form.is_valid())

	@pytest.mark.django_db
	def test_with_only_permission(self):
		permission = Permission.objects.all().first()
		form = GroupForm(data={'permissions': [permission]})
		self.assertFalse(form.is_valid())

	@pytest.mark.django_db
	def test_with_permission_and_name(self):
		permission = Permission.objects.all().first()
		data = {
			'name': 'Test Group',
			'permission': [permission]
		}
		form = GroupForm(data=data)
		self.assertTrue(form.is_valid())


