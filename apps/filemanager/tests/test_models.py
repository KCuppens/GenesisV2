import pytest
import re
from django.contrib.auth import get_user_model
User = get_user_model()
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

class BaseModelTestCase(TestCase):

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


class DirectoryModelTestCase(BaseModelTestCase):

	def test_config_model_instance_type(self):
		directory = self.create_directory()
		self.assertIsInstance(directory, Directory)

	def test_model_slug(self):
		directory = self.create_directory()
		self.assertEqual(directory.slug, 'test-directory')

	@pytest.mark.django_db
	def test_model_parent(self):
		parent_dir = self.create_directory(name="Parent directory")
		child_dir = self.create_directory(parent=parent_dir)
		self.assertIsInstance(child_dir.parent, Directory)

		with self.subTest():
			self.assertEqual(child_dir.parent.id, parent_dir.id)
		with self.subTest():
			self.assertTrue(child_dir.has_parent())

	@pytest.mark.django_db
	def test_model_mtm_field(self):
		directory = self.create_directory()
		media = self.create_media()
		directory.documents.set([media.pk])
		self.assertEqual(directory.documents.count(),
						 1)

	@pytest.mark.django_db
	def test_directory_version(self):
		directory = self.create_directory()
		revision = DirectoryRevision.objects.get(current_instance=directory)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 1)

		with self.subTest():
			self.assertIsInstance(versions.first(), DirectoryVersion)


class MediaModelTestCase(BaseModelTestCase):

	def test_media_instance_type(self):
		media = self.create_media()
		self.assertIsInstance(media, Media)

	def test_model_slug(self):
		media = self.create_media()
		self.assertEqual(media.slug, 'test-media')

	@pytest.mark.django_db
	def test_model_directory(self):
		directory = self.create_directory()
		media = self.create_media(directory=directory)
		self.assertIsInstance(media.directory, Directory)

	@pytest.mark.django_db
	def test_model_mtm_thumbnail_field(self):
		media = self.create_media()
		thumb = self.create_thumbnail()
		media.thumbnails.set([thumb.pk])
		self.assertEqual(media.thumbnails.count(),
						 1)

	@pytest.mark.django_db
	def test_media_version(self):
		directory = self.create_directory()
		media = self.create_media(directory=directory)
		revision = MediaRevision.objects.get(current_instance=media)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 1)

		with self.subTest():
			self.assertIsInstance(versions.first(), MediaVersion)

class ThunbnailModelTestCase(BaseModelTestCase):

	def test_thnumbnail_instance_type(self):
		thumb = self.create_thumbnail()
		self.assertIsInstance(thumb, Thumbnail)