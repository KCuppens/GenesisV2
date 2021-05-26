import pytest
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import reverse
from apps.news.models import Article 
from apps.pages.models import DetailPage, Page, Canvas
from django.utils.translation import ugettext_lazy as _


class BaseViewTestCase(TestCase):

	@pytest.mark.django_db
	def create_page(self, page_title='Test Page',
					**kwargs):
		return Page.objects.create(
			page_title=page_title,
			**kwargs
		)

	@pytest.mark.django_db
	def create_detailpage(self, **kwargs):
		return DetailPage.objects.create(
			**kwargs
		)

	@pytest.mark.django_db
	def setUp(self):
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.page = self.create_page()
		canvas = Canvas.objects.create()
		self.detail_page = self.create_detailpage(canvas=canvas)



class PageViewTestCase(BaseViewTestCase):
	'''
	test page_view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'index'
		super(PageViewTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_with_slug(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url, args=[self.page.slug])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'front/index.html')
		with self.subTest():
			self.assertTrue(resp.context['page'])

	@pytest.mark.django_db
	def test_view_without_slug(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 404)
		with self.subTest():
			self.assertTemplateUsed(resp, 'front/index.html')
		with self.subTest():
			self.assertTrue(resp.context['page'])

# class PageDetailTestCase(BaseViewTestCase):
# 	'''
# 	test page_detail_view
# 	'''

# 	def __init__(self, *args, **kwargs):
# 		self.view_url = 'detail'
# 		super(PageDetailTestCase, self).__init__(*args, **kwargs)

