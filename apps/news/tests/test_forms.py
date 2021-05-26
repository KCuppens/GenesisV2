import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from apps.news.models import Article
from apps.news.forms import ArticleForm


class ArticleFormTest(TestCase):
	'''
	test ArticleForm
	'''

	@pytest.mark.django_db
	def create_article(self, title='Test Article',
					   image='/home/wangoes/Downloads/59A.jpg',
					   summary='Test Summary',
					   content='Test Content', **kwargs):
		return Article.objects.create(
			title=title, image=image,
			summary=summary, content=content,
			**kwargs
		)

	def test_with_empty_data(self):
		form = ArticleForm(data={})
		self.assertFalse(form.is_valid())

	def test_with_partial_data(self):
		data = {
			'title': 'Test Title'
		}
		form = ArticleForm(data=data)
		self.assertFalse(form.is_valid())

	def test_with_empty_title_gallery(self):
		data = {
			'title': '',
			'gallery': '',
			'image': '/home/wangoes/Downloads/59A.jpg',
			'content': 'Test Content',
			'summary': 'Test Summary',
			'meta_title': '',
			'meta_description': '',
			'meta_keywords': '',
			'date_expired': '',
			'date_published': '',
			'active': False
		}
		form = ArticleForm(data=data)
		self.assertFalse(form.is_valid())

		with self.subTest():
			self.assertEqual(form.errors['title'][0], 
							_('Er moet altijd een titel zijn.'))
		with self.subTest():
			self.assertEqual(form.errors['gallery'][0], 
							'Dit veld is verplicht.\t')

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'title': 'Test Title',
			'gallery': '["value": "/home/wangoes/Downloads/59A.jpg"]',
			'image': '/home/wangoes/Downloads/59A.jpg',
			'content': 'Test Content',
			'summary': 'Test Summary',
			'meta_title': '',
			'meta_description': '',
			'meta_keywords': '',
			'date_expired': '',
			'date_published': '',
			'active': False
		}
		form = ArticleForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form, ArticleForm)
		with self.subTest():
			self.assertIsInstance(form.save(), Article)

	def test_with_instance(self):
		gallery = '["value": "/home/wangoes/Downloads/59A.jpg"]'
		article = self.create_article(gallery=gallery)
		data = {
			'title': 'New Updated Title',
			'gallery': '["value": "/home/wangoes/Downloads/59A.jpg"]',
			'image': '/home/wangoes/Downloads/59A.jpg'
		}
		form = ArticleForm(data=data, instance=article)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of value'):
			self.assertEqual(form.save().title, 'New Updated Title')
