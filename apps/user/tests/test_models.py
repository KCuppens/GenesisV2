import pytest
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from apps.user.models import (
	User
)

class BaseModelTestCase(TestCase):

	@pytest.mark.django_db
	def create_user(self, username='testuser',
					email='testuser@gmail.com',
					password='testing321',
					**kwargs):
		return User.objects.create(
			username=username,
			email=email,
			password=password,
			**kwargs
		)

class UserModelTestCases(BaseModelTestCase):
	'''
	Test: User model
	'''

	@pytest.mark.django_db
	def test_wrong_user_type(self):
		user = self.create_user()
		with self.assertRaises(ValueError):
			user.user_type = 'wrong_type'
			user.save()

	@pytest.mark.django_db
	def test_get_full_name(self):
		user = self.create_user()
		user.first_name = 'John'
		user.last_name = 'Doe'
		user.save()

		self.assertEqual(user.get_full_name(), 'John Doe')

	@pytest.mark.django_db
	def test_get_short_email(self):
		user = self.create_user()
		self.assertEqual(user.get_short_name(), user.email)

	@pytest.mark.django_db
	def test_activate(self):
		user = self.create_user()
		user.activate()
		self.assertTrue(user.is_active)

