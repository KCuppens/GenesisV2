import pytest
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from apps.news.models import Article, NewsRevision, NewsVersion


class ArticleModelTest(TestCase):

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

	def test_config_model_instance_type(self):
		article = self.create_article()
		self.assertIsInstance(article, Article)

		with self.subTest(msg='Test title'):
			self.assertEqual(article.title, 'Test Article')

	def test_model_slug(self):
		article = self.create_article()
		self.assertEqual(article.slug, 'test-article')

	def test_model_image_path(self):
		article = self.create_article()
		match = re.match(r'(\/.*?\.[\w:]+)', article.image)
		self.assertTrue(match)

	def test_model_image_invalid_path(self):
		path = 'some_invalid_image_path'
		article = self.create_article(image=path)
		match = re.match(r'(\/.*?\.[\w:]+)', article.image)
		self.assertTrue(match)

	@pytest.mark.django_db
	def test_article_newsrevision(self):
		article = self.create_article()
		revision = NewsRevision.objects.get(current_instance=article)
		self.assertIsInstance(revision, NewsRevision)


	@pytest.mark.django_db
	def test_article_newsversion(self):
		article = self.create_article()
		revision = NewsRevision.objects.get(current_instance=article)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 1)

		with self.subTest():
			self.assertIsInstance(versions.first(), NewsVersion)
