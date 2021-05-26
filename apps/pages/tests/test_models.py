import pytest
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.pages.models import (
	Page,
	Canvas,
	CanvasRow,
	PageBlock,
	PageBlockElement,
	DetailPage,
	PageRevision,
	PageVersion
)

class BaseModelTestCase(TestCase):

	@pytest.mark.django_db
	def create_page(self, page_title='Test Page',
					menu_title='Test Menu',
					slug='test-page',
					full_slug='test-page',
					**kwargs):
		return Page.objects.create(
			page_title=page_title,
			menu_title=menu_title,
			slug=slug,
			full_slug=full_slug,
			**kwargs
		)

	@pytest.mark.django_db
	def create_page_block(self, title='Test Page Block',
					subtitle='Test sub title',
					**kwargs):
		return PageBlock.objects.create(
			title=title,
			subtitle=subtitle,
			**kwargs
		)


class PageModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		page = self.create_page()
		self.assertIsInstance(page, Page)

		with self.subTest(msg='Test page title'):
			self.assertEqual(page.page_title, 'Test Page')

	def test_model_slug(self):
		page = self.create_page()
		self.assertEqual(page.slug, 'test-page')

	def test_if_slug_full_slug_equal(self):
		page = self.create_page()
		self.assertEqual(page.slug, page.full_slug)

	def test_page_create_with_wrong_url_type(self):
		with self.assertRaises(ValidationError):
			page = self.create_page(url_type='wrong_url_type')
		self.assertEqual(page.url_type, 'wrong_url_type')

	def test_page_is_link_through(self):
		page = self.create_page()
		self.assertFalse(page.is_link_through())

	def test_page_is_link_through(self):
		page = self.create_page()
		self.assertEqual(page.get_active_children().count(), 0)

	@pytest.mark.django_db
	def test_model_revision(self):
		page = self.create_page()
		revision = PageRevision.objects.get(current_instance=page)
		self.assertIsInstance(revision, PageRevision)


	@pytest.mark.django_db
	def test_model_version(self):
		page = self.create_page()
		revision = PageRevision.objects.get(current_instance=page)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 0)


class PageBlockModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		page_block = self.create_page_block()
		self.assertIsInstance(page_block, PageBlock)

		with self.subTest(msg='Test page block title'):
			self.assertEqual(page_block.title, 'Test Page Block')

	def test_page_block_create_with_wrong_module_choice(self):
		with self.assertRaises(ValidationError):
			page_block = self.create_page_block(module='wrong_module')
		self.assertEqual(page_block.module, 'wrong_module')

	def test_page_block_create_with_wrong_sort_choice(self):
		with self.assertRaises(ValidationError):
			page_block = self.create_page_block(sort='wrong_sort')
		self.assertEqual(page_block.sort, 'wrong_module')

	def test_page_block_create_with_wrong_sort_order(self):
		with self.assertRaises(ValidationError):
			page_block = self.create_page_block(sort_order='wrong_sort_order')
		self.assertEqual(page_block.sort_order, 'wrong_sort_order')


class CanvasModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		canvas = Canvas.objects.create()
		self.assertIsInstance(canvas, Canvas)

	@pytest.mark.django_db
	def test_canvas_rows_m2m_field(self):
		page_block1 = self.create_page_block(title='Page block 1')
		page_block2 = self.create_page_block(title='Page block 2')
		canvas_row1 = CanvasRow.objects.create(block=page_block1)
		canvas_row2 = CanvasRow.objects.create(block=page_block2)

		canvas = Canvas.objects.create()
		canvas.rows.set([canvas_row1, canvas_row2])

		self.assertEqual(canvas.rows.count(), 2)
