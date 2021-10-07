import pytest
import uuid
import json
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from apps.blocks.models import Block, BlockCategory, BlocksRevision,\
							   BlocksVersion
from apps.blocks.forms import BlockForm, BlockCategoryForm
from apps.blocks import views
from apps.blocks.tests.test_models import BlockModelTest

class BaseBlockTestCase(TestCase):

	@pytest.mark.django_db
	def create_block(self, name="Test Block", has_title=True,
					 has_image=True, has_block_elements=True,
					 has_block_element_title=True, **kwargs):
		image = '/home/wangoes/Downloads/59A.jpg'

		return Block.objects.create(
			# author=user,
			name=name, image=image, has_title=has_title,
			has_image=has_image, has_block_elements=has_block_elements,
			has_block_element_title=has_block_element_title,
			**kwargs
		)

	@pytest.mark.django_db
	def create_block_category(self, name="Test Category"):
		# user = User.objects.get(id=1)
		return BlockCategory.objects.create(
			name=name
		)

	@pytest.mark.django_db
	def setUp(self):
		# self.client = Client()
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.block = self.create_block()
		self.block_category = self.create_block_category()


class BlockViewTest(BaseBlockTestCase):

	def test_block_overview_view_no_login(self):
		url = reverse('overviewblocks')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	def test_block_overview_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse('overviewblocks')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'blocks/index.html')

	def test_block_overview_with_block_object(self):
		self.client.force_login(self.user)
		url = reverse('overviewblocks')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, self.block.name)

	def test_add_block_view_get(self):
		# testing addblock with get request
		self.client.force_login(self.user)
		url = reverse('addblock')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
		self.assertIsInstance(resp.context['form'], BlockForm)

	def test_add_block_view_post(self):
		# testing addblock with a post request
		block_data = {
			'name': 'Test Block 2',
			'has_title': True,
			'has_image': True,
			'has_block_elements': True,
			'has_block_element_title': True
		}

		self.client.force_login(self.user)
		url = reverse('addblock')
		resp = self.client.post(url, block_data)

		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'Test Block 2')

	def test_add_block_with_empty_data(self):
		# testing addblock with posting empty data
		self.client.force_login(self.user)
		url = reverse('addblock')
		resp = self.client.post(url, {})

		self.assertEqual(resp.status_code, 200)
		# invalid form with errors
		self.assertIsInstance(resp.context['form'], BlockForm)
		self.assertFalse(resp.context['form'].is_valid())

	def test_edit_block_view_get(self):
		self.client.force_login(self.user)
		url = reverse('editblock', args=[self.block.id])
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
		self.assertIsInstance(resp.context['form'], BlockForm)
		self.assertIsInstance(resp.context['form'].instance, 
							  Block)

	def test_edit_block_view_post_wrong_block_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse('editblock', args=[id])
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 404)

	@pytest.mark.django_db
	def test_edit_block_view_post(self):
		# testing addblock with a post request
		block_data = {
			'name': 'Test Block --updated'
		}

		self.client.force_login(self.user)
		url = reverse('editblock', args=[self.block.id])
		resp = self.client.post(url, block_data)

		self.assertEqual(resp.status_code, 200)
		# self.assertContains(resp, 'The block has been succesfully changed!')
		self.assertEqual(resp.context['item'].name, block_data['name'])

	def test_edit_block_view_post_empty_data(self):
		self.client.force_login(self.user)
		url = reverse('editblock', args=[self.block.id])
		resp = self.client.post(url, {})

		self.assertEqual(resp.status_code, 200)
		# invalid form with errors
		self.assertIsInstance(resp.context['form'], BlockForm)
		self.assertFalse(resp.context['form'].is_valid())

class ToggleActivationViewTest(BaseBlockTestCase):
	'''
	testing toggle_activation_view
	'''

	@pytest.mark.django_db
	def test_toggle_activation_view_get(self):
		self.client.force_login(self.user)
		url = reverse('activate-blocks', args=[self.block.id])
		resp = self.client.post(url)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewblocks'))
		self.block.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.block.active)


class TestDeleteAjaxBlockModalView(BaseBlockTestCase):
	'''
	testing delete_ajax_block_modal view
	'''

	def test_delete_ajax_block_modal_get(self):
		self.client.force_login(self.user)
		url = reverse('deletemodalblock')
		with self.assertRaises(Block.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			print('resp: ', resp)
			self.assertFalse(resp)

	def test_delete_ajax_block_modal_post_without_id(self):
		self.client.force_login(self.user)
		url = reverse('deletemodalblock')
		with self.assertRaises(Block.DoesNotExist):
			resp = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			self.assertFalse(resp)

	@pytest.mark.django_db
	def test_delete_ajax_block_modal_post_with_id(self):
		self.client.force_login(self.user)
		data = {
			'id': self.block.id
		}
		url = reverse('deletemodalblock')
		resp = self.client.post(
			url, 
			data=data, 
			HTTP_X_REQUESTED_WITH='XMLHttpRequest'
		)

		with self.subTest():
			self.assertTrue(resp.json()['template'])
		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertIn('The decision is yours', resp.json()['template'])


class TestDeleteBlockView(BaseBlockTestCase):
	'''
	testing delete_block view
	'''

	def test_delete_block_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse('deleteblock', args=[id])

		with self.assertRaises(Block.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_delete_block_with_valid_pk(self):
		self.client.force_login(self.user)
		block = self.create_block()
		url = reverse('deleteblock', args=[block.id])

		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)		
		self.assertRedirects(resp, reverse('overviewblocks'))


class TestOverviewBlockCategory(BaseBlockTestCase):
	'''
	test overview_blockcategories
	'''
	@pytest.mark.django_db
	def test_overview_blockcategories_get(self):
		self.client.force_login(self.user)
		url = reverse('overviewblock-categories')

		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'blockcategory/index.html')
		self.assertTrue(resp.context['categories'])

	@pytest.mark.django_db
	def test_overview_blockcategories_get_with_category(self):
		self.client.force_login(self.user)
		block_category = self.create_block_category()
		url = reverse('overviewblock-categories')

		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'blockcategory/index.html')
		self.assertTrue(resp.context['categories'])	


class TestAddBlockCategory(BaseBlockTestCase):
	'''
	test add_block_category view
	'''
	def test_add_block_category_get_request(self):
		self.client.force_login(self.user)
		block_category = self.create_block_category()
		url = reverse('addblock-category')

		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'blockcategory/add.html')
		self.assertIsInstance(resp.context['form'], BlockCategoryForm)

	def test_add_block_category_post_invalid_data(self):
		self.client.force_login(self.user)
		url = reverse('addblock-category')

		resp = self.client.post(url, data={})
		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())

	def test_add_block_category_post_valid_data(self):
		data = {
			'name': 'Test block category'
		}
		self.client.force_login(self.user)
		url = reverse('addblock-category')

		resp = self.client.post(url, data=data)
		self.assertEqual(resp.status_code, 302)

class TestEditBlockCategories(BaseBlockTestCase):
	'''
	test edit_block_category
	'''
	def test_edit_block_category_get_request(self):
		self.client.force_login(self.user)
		url = reverse('editblock-category', args=[self.block.id])

		resp = self.client.get(url)
		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 200)
		with self.subTest(msg='Template check'):
			self.assertTemplateUsed(resp, 'blockcategory/edit.html')
		with self.subTest(msg='Form check'):
			self.assertIsInstance(resp.context['form'], BlockCategoryForm)
		with self.subTest(msg='Block instance check'):
			self.assertIsInstance(resp.context['item'], Block)

	def test_edit_block_category_post_invalid_data(self):
		self.client.force_login(self.user)
		url = reverse('editblock-category', args=[self.block.id])

		resp = self.client.post(url, data={})

		with self.subTest(msg='Status code check'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest(msg='template check'):
			self.assertTemplateUsed(resp, 'blockcategory/edit.html')

	@pytest.mark.django_db
	def test_edit_block_category_post_valid_data(self):
		data = {
			'name': 'Test block category updated'
		}
		self.client.force_login(self.user)
		url = reverse('editblock-category', args=[self.block.id])
		resp = self.client.post(url, data=data)

		with self.subTest():
			url = reverse('overviewblock-categories')
			self.assertRedirects(resp, url)


class TestToggleCategoryActivationView(BaseBlockTestCase):
	'''
	test toggle_category_activation_view
	'''
	@pytest.mark.django_db
	def test_toggle_category_activation_view_get(self):
		self.client.force_login(self.user)
		url = reverse('activate-blockcategories',
					  args=[self.block_category.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewblock-categories'))


class TestDeleteAjaxBlockCategoryModal(BaseBlockTestCase):
	'''
	test delete_ajax_block_category_modal
	'''
	def test_delete_ajax_block_category_modal_get(self):
		self.client.force_login(self.user)
		url = reverse('deletemodalblock-category')
		with self.assertRaises(BlockCategory.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			self.assertFalse(resp)


	def test_delete_ajax_block_category_modal_post_invalid_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse('deletemodalblock-category')
		with self.assertRaises(BlockCategory.DoesNotExist):
			resp = self.client.post(url, data={'id': id},
								    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			self.assertFalse(resp)

	def test_delete_ajax_block_category_modal_post_valid_id(self):
		id = self.block_category.id
		self.client.force_login(self.user)
		url = reverse('deletemodalblock-category')
		resp = self.client.post(url, data={'id': id},
							    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		with self.subTest():
			self.assertTrue(resp.json()['template'])
		# with self.subTest():
		# 	self.assertContains(resp, 'The decision is yours')


class TestDeleteBlockCategoryView(BaseBlockTestCase):
	'''
	testing delete_blockcategory view
	'''

	def test_delete_block_category_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse('deleteblock-category', args=[id])

		with self.assertRaises(BlockCategory.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_delete_block_category_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse('deleteblock-category',
					  args=[self.block_category.id])

		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)		
		self.assertRedirects(resp, reverse('overviewblock-categories'))


class TestGetVersionAjaxModal(BaseBlockTestCase):
	'''
	test get_version_ajax_modal
	'''
	def test_get_version_ajax_modal(self):
		self.client.force_login(self.user)
		url = reverse('blockversionmodal')
		with self.assertRaises(Block.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			self.assertFalse(resp)


	def test_get_version_ajax_modal_post_invalid_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse('blockversionmodal')
		with self.assertRaises(Block.DoesNotExist):
			resp = self.client.post(url, data={'id': id},
								    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			self.assertFalse(resp)

	def test_get_version_ajax_modal_post_valid_id(self):
		id = self.block.id
		self.client.force_login(self.user)
		url = reverse('blockversionmodal')
		resp = self.client.post(url, data={'id': id},
							    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertTrue(json.loads(resp.content)['template'])
		self.assertContains(resp, 'Versions')


class TestGetDeleteVersionAjaxModal(BaseBlockTestCase):
	'''
	test get_delete_version_ajax_modal
	'''
	def test_get_delete_version_ajax_modal_get(self):
		self.client.force_login(self.user)
		url = reverse('blockdeleteversionmodal')
		with self.assertRaises(BlocksVersion.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
			self.assertFalse(resp.content)

	def test_get_version_ajax_modal_post_valid_id(self):
		revision = BlocksRevision.objects.get(current_instance=self.block)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse('blockdeleteversionmodal')
		resp = self.client.post(url, data={'id': version.id},
							    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertTrue(json.loads(resp.content)['template'])
		# self.assertContains(resp, 'Are you sure you want to delete this version?')

class TestSelectVersion(BaseBlockTestCase):
	'''
	test select_version view
	'''
	def test_select_version_with_valid_version_id(self):
		revision = BlocksRevision.objects.get(current_instance=self.block)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse('blockselectversion', args=[version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('overviewblocks'))

	def test_select_version_with_invalid_version_id(self):
		self.client.force_login(self.user)
		url = reverse('blockselectversion', args=[123])

		with self.assertRaises(BlocksVersion.DoesNotExist):
			resp = self.client.get(url)
			with self.subTest(msg='Valid Version id'):
				self.assertRedirects(resp, reverse('overviewblocks'))
			with self.subTest(msg='Test contains'):
				self.assertContains(resp, 'Versie succesvol gewijzigd')

	def test_select_version_with_valid_wrong_id(self):
		self.client.force_login(self.user)
		url = reverse('blockselectversion', args=[123])
		with self.assertRaises(BlocksVersion.DoesNotExist):
			resp = self.client.get(url)

			with self.subTest(msg='Valid Version id'):
				self.assertRedirects(resp, reverse('overviewblocks'))
			with self.subTest(msg='Test contains'):
				self.assertContains(resp, 'Versie succesvol gewijzigd')


class TestDeleteVersion(BaseBlockTestCase):
	'''
	test delete_version view
	'''
	def test_delete_version_with_valid_version_id(self):
		revision = BlocksRevision.objects.get(current_instance=self.block)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse('blockdeleteversion', args=[version.id])
		resp = self.client.get(url)
		
		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('overviewblocks'))

	def test_delete_version_with_invalid_version_id(self):
		self.client.force_login(self.user)
		url = reverse('blockdeleteversion', args=[123])

		with self.assertRaises(BlocksVersion.DoesNotExist):
			resp = self.client.get(url)
			with self.subTest(msg='Valid Version id'):
				self.assertRedirects(resp, reverse('overviewblocks'))
			with self.subTest(msg='Test contains'):
				self.assertContains(resp, 'De versie is succesvol verwijderd')

	def test_delete_version_with_wrong_version_id(self):
		self.client.force_login(self.user)
		url = reverse('blockdeleteversion', args=[123])

		with self.assertRaises(BlocksVersion.DoesNotExist):
			resp = self.client.get(url)
			with self.subTest(msg='Valid Version id'):
				self.assertRedirects(resp, reverse('overviewblocks'))
			with self.subTest(msg='Test contains'):
				self.assertContains(resp, 'De versie is succesvol verwijderd')

class TestAddVersionComment(BaseBlockTestCase):
	'''
	test add_version_comment view
	'''
	def test_add_version_comment_with_valid_version_id(self):
		data = {
			'comment': 'This is selected version'
		}
		revision = BlocksRevision.objects.get(current_instance=self.block)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse('blockaddversioncomment', args=[version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('overviewblocks'))
		with self.subTest(msg='Test contains'):
			self.assertContains(resp, 'De opmerking is succesvol opgeslagen!')
