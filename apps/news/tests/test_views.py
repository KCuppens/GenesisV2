import pytest
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import reverse
from apps.news.models import Article, NewsRevision, NewsVersion
from apps.news.forms import ArticleForm
from django.utils.translation import ugettext_lazy as _


class BaseArticleViewTestCase(TestCase):

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

	@pytest.mark.django_db
	def setUp(self):
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.article = self.create_article()


class OverviewTestCase(BaseArticleViewTestCase):
	'''
	test overview_article view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewarticle'
		super(OverviewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'news/index.html')
		with self.subTest():
			self.assertContains(resp, _('News overview'))
		with self.subTest():
			self.assertTrue(resp.context['articles'])


class AddArticleTestCase(BaseArticleViewTestCase):
	'''
	test add_article view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addarticle'
		super(AddArticleTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'news/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], ArticleForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())
		with self.subTest():
			self.assertTemplateUsed(resp, 'news/add.html')
		with self.subTest():
			gallery_error = resp.context['form'].errors['gallery'][0]
			self.assertEqual(gallery_error, _('Dit veld is verplicht.\t'))
		with self.subTest():
			image_error = resp.context['form'].errors['image'][0]
			self.assertEqual(image_error, _('Dit veld is verplicht.\t'))
		with self.subTest():
			title_error = resp.context['form'].errors['title'][0]
			self.assertEqual(title_error, _('Er moet altijd een titel zijn.\t'))

	def test_view_post_request_valid_data(self):
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

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewarticle'))
		with self.subTest():
			self.assertContains(resp, _('The article has been succesfully added!'))


class EditArticleTestCase(BaseArticleViewTestCase):
	'''
	test edit_article view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'editarticle'
		super(EditArticleTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.article.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.article.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'news/edit.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], ArticleForm)
		with self.subTest():
			self.assertIsInstance(resp.context['article'], Article)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.article.id])
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())
		with self.subTest():
			self.assertTemplateUsed(resp, 'news/edit.html')
		with self.subTest():
			gallery_error = resp.context['form'].errors['gallery'][0]
			self.assertEqual(gallery_error, _('Dit veld is verplicht.\t'))
		with self.subTest():
			image_error = resp.context['form'].errors['image'][0]
			self.assertEqual(image_error, _('Dit veld is verplicht.\t'))
		with self.subTest():
			title_error = resp.context['form'].errors['title'][0]
			self.assertEqual(title_error, _('Er moet altijd een titel zijn.\t'))

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		data = {
			'title': self.article.title,
			'gallery': '["value": "/home/wangoes/Downloads/59A.jpg"]',
			'image': self.article.image,
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.article.id])
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewarticle'))
		with self.subTest():
			self.assertContains(resp, _('The article has been succesfully changed!'))
		self.article.refresh_from_db()
		with self.subTest(msg="Test changed data"):
			self.assertEqual(self.article.gallery, 
							 data['gallery'])


class DeleteAjaxArticleModalTestCase(BaseArticleViewTestCase):
	'''
	test delete_ajax_article_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodalarticle'
		super(DeleteAjaxArticleModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Article.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Article.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.article.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		# with self.subTest():
		# 	self.assertContains(resp, _('Are you sure you want to delete?'))


class GetVersionAjaxArticleModalTestCase(BaseArticleViewTestCase):
	'''
	test get_version_ajax_article_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'versionmodalarticle'
		super(GetVersionAjaxArticleModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Article.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Article.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.article.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Versions')
			self.assertContains(resp, text)


class DeleteVersionAjaxArticleModalTestCase(BaseArticleViewTestCase):
	'''
	test get_delete_version_ajax_article_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deleteversionmodalarticle'
		super(DeleteVersionAjaxArticleModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	# def test_view_post_request_empty_data(self):
	# 	self.client.force_login(self.user)
	# 	url = reverse(self.view_url_conf)

	# 	with self.assertRaises(NewsVersion.DoesNotExist):
	# 		resp = self.client.post(url, 
	# 								data={}, 
	# 								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		revision = NewsRevision.objects.get(current_instance=self.article)
		version = revision.versions.all().first()
		data = {
			'id': version.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		# with self.subTest():
		# 	text = _('Are you sure you want to delete this version?')
		# 	self.assertContains(resp, text)


class SelectVersionTestCase(BaseArticleViewTestCase):
	'''
	test select_version view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'selectversion'
		super(SelectVersionTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_select_version_with_valid_version_id(self):
		revision = NewsRevision.objects.get(current_instance=self.article)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('overviewarticle'))
		with self.subTest():
			self.assertTrue(version.is_current)

	def test_select_version_with_wrong_id(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[123])
		with self.assertRaises(NewsVersion.DoesNotExist):
			resp = self.client.get(url)


class DeleteVersionTestCase(BaseArticleViewTestCase):
	'''
	test delete_version view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deleteversion'
		super(DeleteVersionTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_delete_version_with_valid_version_id(self):
		revision = NewsRevision.objects.get(current_instance=self.article)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[version.id])
		resp = self.client.get(url, follow=True)
		
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewarticle'))
		with self.subTest(msg='Test contains'):
			self.assertContains(resp, _('De versie is succesvol verwijderd'))

	def test_delete_version_with_wrong_version_id(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[123])

		with self.assertRaises(NewsVersion.DoesNotExist):
			resp = self.client.get(url)


class ToggleArticleActivationViewTestCase(BaseArticleViewTestCase):
	'''
	test toggle_article_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'activate-article'
		super(ToggleArticleActivationViewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.article.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)


	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[id])
		with self.assertRaises(Article.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.article.id])
		resp = self.client.get(url)
		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewarticle'))
		self.article.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.article.active)


class DeleteArticleTestCase(BaseArticleViewTestCase):
	'''
	test delete_article view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletearticle'
		super(DeleteArticleTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.article.pk])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.article.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewarticle'))
		with self.subTest():
			self.assertContains(resp, _('The article has been succesfully deleted!!'))

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Article.DoesNotExist):
			resp = self.client.get(url)
