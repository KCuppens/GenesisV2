import pytest
import uuid
import os
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import reverse
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
from django.utils.translation import ugettext_lazy as _


class BaseViewTestCase(TestCase):

	@pytest.mark.django_db
	def create_directory(self, name="Test Directory", **kwargs):
		return Directory.objects.create(
			name=name, **kwargs
		)

	@pytest.mark.django_db
	def create_media(self, name='Test media',
					 file=os.path.join(settings.BASE_DIR, 'media/image/orig/a.png'),
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

	@pytest.mark.django_db
	def setUp(self):
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.directory = self.create_directory()
		self.media = self.create_media()
		self.thumb = self.create_thumbnail()


class GetMediaOverviewTestCase(BaseViewTestCase):
	'''
	test get_media_overview view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'media-overview'
		super(GetMediaOverviewTestCase, self).__init__(*args, **kwargs)
	
	@pytest.mark.django_db
	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertContains(resp, _('Test Directory'))
		with self.subTest():
			self.assertContains(resp, _('Test media'))

	@pytest.mark.django_db
	def test_view_with_type_directory(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url) + '?type=directories'
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertContains(resp, _('Test Directory'))

	@pytest.mark.django_db
	def test_view_with_type_image(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url) + '?type=image'
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertContains(resp, _('Test media'))

	@pytest.mark.django_db
	def test_view_with_dir(self):
		media = self.create_media(directory=self.directory)
		self.client.force_login(self.user)
		url = reverse(self.view_url) + f'?dir={self.directory.id}'
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertContains(resp, _(media.name))


class CreateDirectoryTestCase(BaseViewTestCase):
	'''
	test create_directory view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'create-directory'
		super(CreateDirectoryTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertEqual(resp.json()['title'], 'Create directory')

	def test_view_get_with_dir(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf) + f'?dir={self.directory.id}'
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertContains(resp, self.directory.name)

	def test_view_post_without_parent_dir(self):
		data = {
			'name': 'New Test Directory'
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('media-document-index'))

	def test_view_post_with_parent_dir(self):
		data = {
			'name': 'New Test Directory',
			'dir': self.directory.id
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('media-document-index'))

	def test_view_post_with_invalid_parent_dir(self):
		id = uuid.uuid4()
		data = {
			'name': 'New Test Directory',
			'dir': id
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Directory.DoesNotExist):
			resp = self.client.post(url, data=data)


class EditDirectoryTestCase(BaseViewTestCase):
	'''
	test edit_directory view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'edit-directory'
		super(EditDirectoryTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf) + f'?dir={self.directory.id}'
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertEqual(resp.json()['title'], 'Directory bewerken\t')

	@pytest.mark.django_db
	def test_view_post_dir_valid_name(self):
		data = {
			'name': 'Updated directory name',
			'dir': self.directory.id
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('media-document-index'))

	@pytest.mark.django_db
	def test_view_post_dir_invalid_name(self):
		data = {
			'name': '',
			'dir': self.directory.id
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertEqual(resp.json()['title'], 'Directory bewerken\t')


class DeleteModalDirectoryTestCase(BaseViewTestCase):
	'''
	test delete_modal_directory view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'delete-modal-directory'
		super(DeleteModalDirectoryTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Directory.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Directory.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		data = {
			'dir': self.directory.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		# with self.subTest():
		# 	self.assertEqual(resp.json()['title'], 'Delete directory')


class DeleteDirectoryTestCase(BaseViewTestCase):
	'''
	test delete_directory view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'delete-directory'
		super(DeleteDirectoryTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.directory.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('media-document-index'))
		# with self.subTest():
		# 	text = 'The directory has been succesfully deleted!'
		# 	self.assertContains(resp, text)

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Directory.DoesNotExist):
			resp = self.client.get(url)

class CreateMediaTypeTestCase(BaseViewTestCase):
	'''
	test create_media_type view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'add-media'
		super(CreateMediaTypeTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertEqual(resp.json()['title'], 'Media uploaden\t')

	@pytest.mark.django_db
	def test_view_post_with_dir(self):
		file_path = os.path.join(settings.BASE_DIR, 'media/image/orig/59A.jpg')
		with open(file_path, 'rb') as file:
			data = {
				'name': 'New Test Image',
				'file': file
			}
			self.client.force_login(self.user)
			url = reverse(self.view_url_conf) + f'?dir={self.directory.id}'
			resp = self.client.post(url, data=data)

			with self.subTest():
				self.assertEqual(resp.status_code, 200)
			with self.subTest():
				self.assertEqual(resp.json()['title'], _('Upload media'))


class EditMediaTypeTestCase(BaseViewTestCase):
	'''
	test edit_media view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'edit-media'
		super(EditMediaTypeTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf) + f'?media={self.media.id}'
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertEqual(resp.json()['title'], 'Media bewerken\t')

	@pytest.mark.django_db
	def test_view_post_with_media(self):
		data = {
			'media': self.media.id, 
			'name': 'New Updated Media'
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('media-document-index'))
		# with self.subTest():
		# 	self.assertContains(resp, data['name'])
		self.media.refresh_from_db()
		with self.subTest():
			self.assertEqual(self.media.name, data['name'])


class DeleteModalMediaTestCase(BaseViewTestCase):
	'''
	test delete_modal_media view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'delete-modal-media'
		super(DeleteModalMediaTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Media.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Media.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'media': self.media.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertEqual(resp.json()['title'], 'Media verwijderen\t')

class DeleteMediaTestCase(BaseViewTestCase):
	'''
	test delete_media view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'delete-media'
		super(DeleteMediaTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.media.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('media-document-index'))
		# with self.subTest():
		# 	text = 'The media has been succesfully deleted!'
		# 	self.assertContains(resp, text)

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Media.DoesNotExist):
			resp = self.client.get(url)


class DownloadMediaTestCase(BaseViewTestCase):
	'''
	test download_media view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'download-media'
		super(DownloadMediaTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_get_request(self):
		media = self.create_media(filename='test_media')
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[media.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertEqual(resp.get('Content-Disposition'),
							'attachment; filename=a.png')

	def test_view_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Media.DoesNotExist):
			resp = self.client.get(url)



class GetVersionAjaxModalTestCase(BaseViewTestCase):
	'''
	test get_version_ajax_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'filemanagerversionmodal'
		super(GetVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=['module'])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_mode_directory_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['directory'])

		with self.assertRaises(Directory.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_media_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['media'])

		with self.assertRaises(Media.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_directory_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['directory'])

		with self.assertRaises(Directory.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_media_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['media'])

		with self.assertRaises(Media.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_mode_directory_post_request_valid_data(self):
		data = {
			'id': self.directory.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['directory'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Versions')
			self.assertContains(resp, text)

	def test_view_mode_media_post_request_valid_data(self):
		data = {
			'id': self.media.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['media'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Versions')
			self.assertContains(resp, text)


class DeleteVersionAjaxModalTestCase(BaseViewTestCase):
	'''
	test get_delete_version_ajax_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'filemanagerdeleteversionmodal'
		super(DeleteVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_mode_directory_post_request_valid_data(self):
		revision = DirectoryRevision.objects.get(current_instance=self.directory)
		version = revision.versions.all().first()
		data = {
			'id': version.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['directory'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		# with self.subTest():
		# 	text = 'Are you sure you want to delete this version?'
		# 	self.assertContains(resp, _('Are you sure you want to delete this version?'))

	@pytest.mark.django_db
	def test_view_mode_media_post_request_valid_data(self):
		revision = MediaRevision.objects.get(current_instance=self.media)
		version = revision.versions.all().first()
		data = {
			'id': version.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['media'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		# with self.subTest():
		# 	text = 'Are you sure you want to delete this version?'
		# 	self.assertContains(resp, text)


class SelectVersionTestCase(BaseViewTestCase):
	'''
	test select_version view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'filemanagerselectversion'
		super(SelectVersionTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_select_version_mode_directory_with_valid_version_id(self):
		revision = DirectoryRevision.objects.get(current_instance=self.directory)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['directory', version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('media-document-index'))
		version.refresh_from_db()
		with self.subTest():
			self.assertTrue(version.is_current)

	@pytest.mark.django_db
	def test_select_version_mode_media_with_valid_version_id(self):
		revision = MediaRevision.objects.get(current_instance=self.media)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['media', version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('media-document-index'))
		version.refresh_from_db()
		with self.subTest():
			self.assertTrue(version.is_current)


class DeleteVersionTestCase(BaseViewTestCase):
	'''
	test delete_version view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'filemanagerdeleteversion'
		super(DeleteVersionTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_delete_version_mode_directory_with_valid_version_id(self):
		revision = DirectoryRevision.objects.get(current_instance=self.directory)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['directory', version.id])
		resp = self.client.get(url, follow=True)
		
		with self.subTest():
			self.assertRedirects(resp, reverse('media-document-index'))
		# with self.subTest(msg='Test contains'):
		# 	self.assertContains(resp, 'De versie is succesvol verwijderd')

	@pytest.mark.django_db
	def test_delete_version_mode_media_with_valid_version_id(self):
		revision = MediaRevision.objects.get(current_instance=self.media)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['media', version.id])
		resp = self.client.get(url, follow=True)
		
		with self.subTest():
			self.assertRedirects(resp, reverse('media-document-index'))
		# with self.subTest(msg='Test contains'):
		# 	self.assertContains(resp, 'De versie is succesvol verwijderd')
