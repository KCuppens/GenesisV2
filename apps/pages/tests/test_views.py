import pytest
import uuid
import json
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import reverse
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
from apps.blocks.models import Block
from apps.pages.forms import PageForm, BlockForm, BlockElementForm
from django.utils.translation import ugettext_lazy as _


class BaseViewTestCase(TestCase):

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
	def setUp(self):
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.page = self.create_page()
		self.page_block = self.create_page_block()


class OverviewPageTestCase(BaseViewTestCase):
	'''
	test overview_page view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewpage'
		super(OverviewPageTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_search_page_title(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url) + f'?search={self.page.page_title}'
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'pages/index.html')
		with self.subTest():
			self.assertContains(resp, self.page.page_title)
		with self.subTest():
			self.assertTrue(resp.context['pages'])
		with self.subTest():
			self.assertEqual(resp.context['search'], self.page.page_title)

	@pytest.mark.django_db
	def test_search_menu_title(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url) + f'?search={self.page.menu_title}'
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'pages/index.html')
		with self.subTest():
			self.assertContains(resp, self.page.page_title)
		with self.subTest():
			self.assertTrue(resp.context['pages'])
		with self.subTest():
			self.assertEqual(resp.context['search'], self.page.menu_title)


class OverviewChildrenPageTestCase(BaseViewTestCase):
	'''
	test overview_children_page view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewchildrenpage'
		super(OverviewChildrenPageTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_children_page_population(self):
		self.client.force_login(self.user)
		page = self.create_page()
		child_page = self.create_page(
			page_title='Test Child Page',
			parent=page
		)
		url = reverse(self.view_url, args=[page.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'pages/children-index.html')
		page.refresh_from_db()
		with self.subTest():
			self.assertContains(resp, child_page.page_title)
		with self.subTest():
			self.assertTrue(resp.context['pages'])
		with self.subTest():
			self.assertEqual(resp.context['page'], child_page)

	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url, args=[id])
		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.get(url)


class AddPageTestCase(BaseViewTestCase):
	'''
	test add_page view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addpage'
		super(AddPageTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'pages/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], PageForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'pages/add.html')
		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())
		with self.subTest():
			self.assertContains(resp, _('Please enter a page title'))
		with self.subTest():
			self.assertContains(resp, _('Please enter a menu title'))

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		data = {
			'page_title': 'New Page Title',
			'menu_title': 'New Menu Title',
			'is_homepage': False,
			'url_type': 'generated'
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewpage'))
		with self.subTest():
			self.assertContains(resp, _('The page has been succesfully added!'))


class AddChildrenPageTestCase(BaseViewTestCase):
	'''
	test add_children_page view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addchildrenpage'
		super(AddChildrenPageTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.page.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'pages/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], PageForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.page.id])
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'pages/add.html')
		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())
		with self.subTest():
			self.assertContains(resp, _('Please enter a page title'))
		with self.subTest():
			self.assertContains(resp, _('Please enter a menu title'))

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		# parent_page = self.create_page(page_title='Parent page',
		# 							   menu_title='Parent menu')
		# self.page.parent = parent_page
		# self.page.save()
		data = {
			'page_title': 'Children Page Title',
			'menu_title': 'Children Menu Title',
			'is_homepage': False,
			'url_type': 'generated'
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.page.id])
		resp = self.client.post(url, data=data, follow=True)

		# with self.subTest():
		# 	self.assertRedirects(resp, reverse('overviewchildrenpage', args=[self.page.id]))
		with self.subTest():
			self.assertContains(resp, _('The page has been succesfully added!'))


class EditPageTestCase(BaseViewTestCase):
	'''
	test edit_page view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'editpage'
		super(EditPageTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.page.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'pages/edit.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], PageForm)
		with self.subTest():
			self.assertIsInstance(resp.context['page'], Page)

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		data = {
			'page_title': 'Page Title Updated',
			'menu_title': 'Menu Title Updated',
			'is_homepage': True,
			'url_type': 'generated'
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.page.id])
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewpage'))
		with self.subTest():
			self.assertContains(resp,  _('The page has been succesfully changed!'))
		self.page.refresh_from_db()
		with self.subTest(msg='Test page title change'):
			self.assertEqual(self.page.page_title, data['page_title'])
		with self.subTest(msg='Test menu title change'):
			self.assertEqual(self.page.menu_title, data['menu_title'])
		with self.subTest(msg='Test is_homepage change'):
			self.assertEqual(self.page.is_homepage, data['is_homepage'])


class ToggleMainMenuActivationViewTestCase(BaseViewTestCase):
	'''
	test toggle_mainmenu_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'toggle-mainmenu-activation-view'
		super(ToggleMainMenuActivationViewTestCase, self).__init__(*args, **kwargs)


	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[id])
		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.page.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewpage'))
		with self.subTest():
			self.assertContains(resp, _('De hoofdmenu status van de pagina is succesvol aangepast!'))
		self.page.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.page.in_main_menu)


class ToggleActivationViewTestCase(BaseViewTestCase):
	'''
	test toggle_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'toggle-activation-view'
		super(ToggleActivationViewTestCase, self).__init__(*args, **kwargs)


	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[id])
		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.page.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewpage'))
		with self.subTest():
			self.assertContains(resp, _('De status van de pagina is succesvol aangepast!'))
		self.page.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.page.active)


class DeleteAjaxPageModalTestCase(BaseViewTestCase):
	'''
	test delete_ajax_page_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodalpage'
		super(DeleteAjaxPageModalTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.page.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			resp_data = json.loads(resp.content)
			text = 'Weet u zeker dat u wilt verwijderen?'
			self.assertIn(text, resp_data['template'])


class DeletePageTestCase(BaseViewTestCase):
	'''
	test delete_page view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletepage'
		super(DeletePageTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_get_request_is_deletable_true(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.page.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewpage'))
		with self.subTest():
			self.assertContains(resp, _('The page has been succesfully deleted!'))
		self.page.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.page.date_deleted)

	@pytest.mark.django_db
	def test_view_get_request_is_deletable_false(self):
		page = self.create_page(is_deletable=False)
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[page.id])
		resp = self.client.get(url, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewpage'))
		with self.subTest():
			self.assertContains(resp, _('The page is not deletable!'))
		page.refresh_from_db()
		with self.subTest():
			self.assertEqual(page.date_deleted, None)

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.get(url)

class CanvasPageTestCase(BaseViewTestCase):
	'''
	test canva_page view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'canvaspage'
		super(CanvasPageTestCase, self).__init__(*args, **kwargs)

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.get(url)


class CanvasDetailPageTestCase(BaseViewTestCase):
	'''
	test canva_page view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'canvasdetailpage'
		super(CanvasDetailPageTestCase, self).__init__(*args, **kwargs)

	def test_view_post_request_wrong_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[123])

		with self.assertRaises(DetailPage.DoesNotExist):
			resp = self.client.get(url)


class CanvasRowTestCase(BaseViewTestCase):
	'''
	test canvas_row view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'canvasrow'
		super(CanvasRowTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_get_request_action_add(self):
		canvas = Canvas.objects.create()
		data = {
			'action': 'add',
			'canvas': canvas.id
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertIn('Selecteer een blok', resp.json()['template'])

	@pytest.mark.django_db
	def test_view_get_request_action_delete(self):
		canvas = Canvas.objects.create()
		canvas_row = CanvasRow.objects.create(block=self.page_block)
		canvas.rows.set([canvas_row.id])
		data = {
			'action': 'delete',
			'canvas': canvas.id,
			'row': canvas_row.id
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		canvas.refresh_from_db()
		with self.subTest():
			self.assertEqual(canvas.rows.count(), 0)

	@pytest.mark.django_db
	def test_view_get_request_action_opemodal(self):
		canvas = Canvas.objects.create()
		canvas_row = CanvasRow.objects.create(block=self.page_block)
		canvas.rows.set([canvas_row.id])
		block = self.create_block(active=True)
		data = {
			'action': 'openmodal',
			'canvas': canvas.id,
			'row': canvas_row.id,
			'page': self.page.id,
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		canvas.refresh_from_db()
		with self.subTest():
			self.assertIn(block.name, resp.json()['template'])

class ContentBlockViewTestCase(BaseViewTestCase):
	'''
	test content_block_view view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'canvascontent'
		super(ContentBlockViewTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_get_request_action_createelement(self):
		block = self.create_page_block(active=True)
		canvas = Canvas.objects.create()
		data = {
			'action': 'createelement',
			'canvas': canvas.id,
			'block': block.id
		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)

	@pytest.mark.django_db
	def test_view_get_request_action_saveelement(self):
		block = self.create_page_block(active=True)
		page_block_element = PageBlockElement.objects.create()
		block.block_elements.add(page_block_element)
		canvas = Canvas.objects.create()
		data = {
			'action': 'saveelement',
			'canvas': canvas.id,
			'block': block.id,
			'block_elem': page_block_element.id,
			'title': 'New Page Block Element'

		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		page_block_element.refresh_from_db()
		# with self.subTest():
		# 	self.assertIn(page_block_element.block_element_title, 
		# 				  resp.json()['template'])


	def test_view_get_request_action_deleteelement(self):
		block = self.create_page_block(active=True)
		page_block_element = PageBlockElement.objects.create()
		block.block_elements.add(page_block_element)
		canvas = Canvas.objects.create()
		data = {
			'action': 'deleteelement',
			'canvas': canvas.id,
			'block': block.id,
			'block_elem': page_block_element.id,
			'title': 'New Page Block Element'

		}
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		block.refresh_from_db()
		with self.subTest():
			self.assertEqual(block.block_elements.count(), 0)



class GetVersionAjaxModalTestCase(BaseViewTestCase):
	'''
	test get_version_ajax_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'pageversionmodal'
		super(GetVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(Page.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_viewpost_request_valid_data(self):
		data = {
			'id': self.page.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		# with self.subTest():
		# 	self.assertIn('Versions', resp.json()['template'])

# class DeleteVersionAjaxModalTestCase(BaseViewTestCase):
# 	'''
# 	test get_delete_version_ajax_modal view
# 	'''

# 	def __init__(self, *args, **kwargs):
# 		self.view_url_conf = 'moduledeleteversionmodal'
# 		super(DeleteVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

# 	def test_view_without_login(self):
# 		url = reverse(self.view_url_conf, args=['module'])
# 		resp = self.client.get(url)
# 		self.assertEqual(resp.status_code, 302)

# 	# def test_view_mode_module_post_request_empty_data(self):
# 	# 	self.client.force_login(self.user)
# 	# 	url = reverse(self.view_url_conf, args=['module'])

# 	# 	with self.assertRaises(ModuleVersion.DoesNotExist):
# 	# 		resp = self.client.post(url, 
# 	# 								data={}, 
# 	# 								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

# 	# def test_view_mode_tab_post_request_empty_data(self):
# 	# 	self.client.force_login(self.user)
# 	# 	url = reverse(self.view_url_conf, args=['tab'])

# 	# 	with self.assertRaises(TabVersion.DoesNotExist):
# 	# 		resp = self.client.post(url, 
# 	# 								data={}, 
# 	# 								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

# 	@pytest.mark.django_db
# 	def test_view_mode_module_post_request_valid_data(self):
# 		revision = ModuleRevision.objects.get(current_instance=self.module)
# 		version = revision.versions.all().first()
# 		data = {
# 			'id': version.id
# 		}

# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['module'])
# 		resp = self.client.post(url, 
# 								data=data,
# 								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

# 		with self.subTest():
# 			self.assertEqual(resp.status_code, 200)
# 		with self.subTest():
# 			text = _('Are you sure you want to delete this version?')
# 			self.assertContains(resp, text)

# 	@pytest.mark.django_db
# 	def test_view_mode_tab_post_request_valid_data(self):
# 		revision = TabRevision.objects.get(current_instance=self.tab)
# 		version = revision.versions.all().first()
# 		data = {
# 			'id': version.id
# 		}

# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['tab'])
# 		resp = self.client.post(url, 
# 								data=data,
# 								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

# 		with self.subTest():
# 			self.assertEqual(resp.status_code, 200)
# 		with self.subTest():
# 			text = _('Are you sure you want to delete this version?')
# 			self.assertContains(resp, text)


# class SelectVersionTestCase(BaseViewTestCase):
# 	'''
# 	test select_version view
# 	'''

# 	def __init__(self, *args, **kwargs):
# 		self.view_url_conf = 'moduleselectversion'
# 		super(SelectVersionTestCase, self).__init__(*args, **kwargs)

# 	@pytest.mark.django_db
# 	def test_select_version_mode_module_with_valid_version_id(self):
# 		revision = ModuleRevision.objects.get(current_instance=self.module)
# 		version = revision.versions.all().first()
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['module', version.id])
# 		resp = self.client.get(url)

# 		with self.subTest(msg='Valid Version id'):
# 			self.assertRedirects(resp, reverse('overviewmodules'))
# 		version.refresh_from_db()
# 		with self.subTest():
# 			self.assertTrue(version.is_current)

# 	@pytest.mark.django_db
# 	def test_select_version_mode_tab_with_valid_version_id(self):
# 		revision = TabRevision.objects.get(current_instance=self.tab)
# 		version = revision.versions.all().first()
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['tab', version.id])
# 		resp = self.client.get(url)

# 		with self.subTest(msg='Valid Version id'):
# 			self.assertRedirects(resp, reverse('overviewtab'))
# 		version.refresh_from_db()
# 		with self.subTest():
# 			self.assertTrue(version.is_current)

# 	def test_select_version_mode_module_with_wrong_id(self):
# 		id = uuid.uuid4()
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['module', id])
# 		resp = self.client.get(url)
# 		self.assertRedirects(resp, reverse('overviewmodules'))


# 	def test_select_version_mode_tab_with_wrong_id(self):
# 		id = uuid.uuid4()
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['tab', id])
# 		resp = self.client.get(url)
# 		self.assertRedirects(resp, reverse('overviewtab'))


# class DeleteVersionTestCase(BaseViewTestCase):
# 	'''
# 	test delete_version view
# 	'''
# 	def __init__(self, *args, **kwargs):
# 		self.view_url_conf = 'moduledeleteversion'
# 		super(DeleteVersionTestCase, self).__init__(*args, **kwargs)

# 	@pytest.mark.django_db
# 	def test_delete_version_mode_module_with_valid_version_id(self):
# 		revision = ModuleRevision.objects.get(current_instance=self.module)
# 		version = revision.versions.all().first()
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['module', version.id])
# 		resp = self.client.get(url, follow=True)
		
# 		with self.subTest():
# 			self.assertRedirects(resp, reverse('overviewmodules'))
# 		with self.subTest(msg='Test contains'):
# 			self.assertContains(resp, _('De versie is succesvol verwijderd'))

# 	@pytest.mark.django_db
# 	def test_delete_version_mode_tab_with_valid_version_id(self):
# 		revision = TabRevision.objects.get(current_instance=self.tab)
# 		version = revision.versions.all().first()
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['tab', version.id])
# 		resp = self.client.get(url, follow=True)
		
# 		with self.subTest():
# 			self.assertRedirects(resp, reverse('overviewtab'))
# 		with self.subTest(msg='Test contains'):
# 			self.assertContains(resp, _('De versie is succesvol verwijderd'))

# 	def test_delete_version_mode_module_with_wrong_version_id(self):
# 		id = uuid.uuid4()
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['module', id])

# 		resp = self.client.get(url)
# 		with self.subTest():
# 			self.assertRedirects(resp, reverse('overviewmodules'))

# 	def test_delete_version_mode_tab_with_wrong_version_id(self):
# 		id = uuid.uuid4()
# 		self.client.force_login(self.user)
# 		url = reverse(self.view_url_conf, args=['tab', id])

# 		resp = self.client.get(url)
# 		with self.subTest():
# 			self.assertRedirects(resp, reverse('overviewtab'))
