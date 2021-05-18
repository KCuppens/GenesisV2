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

class BlockFormTestCase(TestCase):

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

	# @pytest.mark.django_db
	# def setUp(self):
	# 	# self.client = Client()
	# 	self.user = User.objects.create_superuser('testuser', 
	# 										 'testuser@gmail.com'
	# 										 'testing321')
	# 	self.block = self.create_block()
	# 	self.block_category = self.create_block_category()

	@pytest.mark.django_db
	def test_valid_block_form(self):
		block = self.create_block()
		data = {
			'name': block.name,
			'has_title': block.has_title,
			'has_image': block.has_image,
			'has_block_elements': block.has_block_elements,
			'has_block_element_title': block.has_block_element_title,
			'image': block.image
		}
		form = BlockForm(data=data)
		self.assertTrue(form.is_valid())

	@pytest.mark.django_db
	def test_invalid_block_form(self):
		block = self.create_block()
		data = {
			'name': '',
			'has_title': block.has_title,
			'has_image': block.has_image,
			'has_block_elements': block.has_block_elements,
			'has_block_element_title': block.has_block_element_title,
			'image': block.image
		}
		form = BlockForm(data=data)
		self.assertFalse(form.is_valid())

	def test_invalid_block_form_empty_data(self):
		form = BlockForm(data={})
		self.assertFalse(form.is_valid())

	def test_invalid_block_category_form_empty_data(self):
		form = BlockCategoryForm(data={})
		self.assertFalse(form.is_valid())

	def test_valid_block_category_form(self):
		data = {
			'name': 'Test block category',
			'date_published': '',
			'date_expired': '',
			'active': ''
		}

		form = BlockCategoryForm(data=data)
		self.assertTrue(form.is_valid())

	def test_valid_block_category_form_2(self):
		data = {
			'name': 'Test block category'
		}
		form = BlockCategoryForm(data=data)
		self.assertTrue(form.is_valid())