import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from apps.blocks.models import Block, BlockCategory, BlocksRevision,\
							   BlocksVersion

class BlockModelTest(TestCase):

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
	def test_block_creation(self):
		block = self.create_block(has_block_element_image=True)
		self.assertTrue(isinstance(block, Block))
		self.assertTrue(block.has_block_element_image)
	
	def test_block_slug(self):
		block = self.create_block()
		self.assertEqual(block.slug, 'test-block')

	def test_block_name(self):
		block = self.create_block()
		self.assertEqual(block.name, 'Test Block')

	def test_block_has_category(self):
		block = self.create_block()
		block_category = self.create_block_category()
		block.category.set([block_category])
		self.assertEqual(block.category.count(), 1)

	def test_block_category_creation(self):
		block_category = self.create_block_category()
		self.assertTrue(isinstance(block_category, BlockCategory))

	def test_block_category_slug(self):
		block_category = self.create_block_category()
		self.assertEqual(block_category.slug, 'test-category')

	def test_block_revision(self):
		block = self.create_block()
		block_revision = BlocksRevision.objects.filter(
			current_instance=block
		)
		self.assertEqual(block_revision.count(), 1)

	@pytest.mark.django_db
	def test_block_versions(self):
		block = self.create_block()
		block_revision = BlocksRevision.objects.get(
			current_instance=block
		)
		versions = BlocksVersion.objects.filter(revision=block_revision)
		self.assertEqual(len(versions), 1)

		block.name = "Test Block 2"
		block.save()

		versions = BlocksVersion.objects.filter(revision=block_revision)
		self.assertEqual(versions.count(), 2)