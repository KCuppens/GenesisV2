import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from apps.filemanager.models import (
	Directory, 
	Media, 
	Thumbnail,
	DirectoryRevision,
	DirectoryVersion,
	MediaRevision,
	MediaVersion
)
from apps.filemanager.forms import (
	DirectoryForm,
	MediaForm,
	MediaFileForm
)


class BaseFormTestCase(TestCase):

	@pytest.mark.django_db
	def create_directory(self, name="Test Directory", **kwargs):
		return Directory.objects.create(
			name=name, **kwargs
		)

	@pytest.mark.django_db
	def create_media(self, name='Test media',
					 file='/home/wangoes/Downloads/59A.jpg',
					 type='image', **kwargs):
		return Media.objects.create(
			name=name, file=file, type=type, **kwargs
		)

	@pytest.mark.django_db
	def create_thumbnail(self, format='png', **kwargs):
		return Thumbnail.objects.create(
			format=format,
			**kwargs
		)


class DirectoryFormTest(BaseFormTestCase):
	'''
	test DirectoryForm
	'''

	def test_with_empty_data(self):
		form = DirectoryForm(data={})
		self.assertFalse(form.is_valid())

	def test_with_partial_data(self):
		data = {
			'name': 'Test Directory'
		}
		form = DirectoryForm(data=data)
		self.assertTrue(form.is_valid())

	def test_with_empty_name(self):
		data = {
			'name': '' # empty name
		}
		form = DirectoryForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest():
			self.assertEqual(form.errors['name'][0], 
							_('Please enter a directory name.'))

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'name': 'Test Directory',
			'summary': 'Test summary'
		}
		form = DirectoryForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form, DirectoryForm)
		with self.subTest():
			self.assertIsInstance(form.save(), Directory)

	def test_with_instance(self):
		directory = self.create_directory()
		data = {
			'name': 'New Test Directory',
			'summary': 'Test summary'
		}
		form = DirectoryForm(data=data, instance=directory)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of value'):
			self.assertEqual(form.save().name, 'New Test Directory')

