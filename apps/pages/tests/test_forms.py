import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from apps.pages.models import (
	Page,
	Canvas,
	CanvasRow,
	PageBlock,
	PageBlockElement,
	DetailPage
)
from apps.pages.forms import PageForm, BlockForm


class BaseFormTestCase(TestCase):

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
					sub_title='Test sub title',
					**kwargs):
		return PageBlock.objects.create(
			title=title,
			sub_title=sub_title,
			**kwargs
		)


class PageFormTestCase(BaseFormTestCase):
	'''
	test PageForm
	'''

	def test_with_empty_data(self):
		form = PageForm(data={})
		self.assertFalse(form.is_valid())

	def test_with_no_page_title(self):
		data = {
			'menu_title': 'Test Menu Title',
			'in_main_menu': True
		}
		form = PageForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest(msg='Test page_title error'):
			self.assertEqual(form.errors['page_title'][0],
							 _('Please enter a page title'))

	def test_with_no_menu_title(self):
		data = {
			'page_title': 'Test Page Title',
			'in_main_menu': True
		}
		form = PageForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest(msg='Test menu_title error'):
			self.assertEqual(form.errors['menu_title'][0],
							 _('Please enter a menu title'))

	@pytest.mark.django_db
	def test_with_wrong_is_homepage(self):
		home_page = self.create_page(is_homepage=True)
		page = self.create_page()
		data = {
			'page_title': 'Test Page Title',
			'menu_title': 'Test Menu Title',
			'is_homepage': True
		}

		form = PageForm(data=data, instance=page)
		self.assertFalse(form.is_valid())

		with self.subTest(msg='Test is_homepage error'):
			self.assertEqual(form.errors['is_homepage'][0],
							 _('You already have a homepage.'))

class BlockFormTestCase(BaseFormTestCase):
	'''
	test BlockForm
	'''

	def test_with_empty_data(self):
		form = BlockForm(data={})
		self.assertTrue(form.is_valid())

	def test_with_wrong_module_choice(self):
		data = {
			'title': 'Test Block Title',
			'module': 'wrong_module'
		}
		form = BlockForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest(msg='Test block module error'):
			self.assertTrue(form.errors['module'][0])

	def test_with_wrong_sort_choice(self):
		data = {
			'title': 'Test Block Title',
			'sort': 'wrong_sort'
		}
		form = BlockForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest(msg='Test block sort error'):
			self.assertTrue(form.errors['sort'][0])

	def test_with_wrong_sort_order_choice(self):
		data = {
			'title': 'Test Block Title',
			'sort_order': 'wrong_sort_order'
		}
		form = BlockForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest(msg='Test block sort order error'):
			self.assertTrue(form.errors['sort_order'][0])
