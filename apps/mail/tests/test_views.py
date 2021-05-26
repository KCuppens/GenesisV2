import pytest
import uuid
import json
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import reverse
from apps.mail.models import (
	MailTemplate,
	MailConfig,
	MailTemplateRevision,
	MailTemplateVersion,
	MailConfigRevision, 
	MailConfigVersion,
	Attachment
)
from apps.mail.forms import MailTemplateForm, MailConfigForm
from django.utils.translation import ugettext_lazy as _


class BaseViewTestCase(TestCase):

	@pytest.mark.django_db
	def create_mail_template(self, key_name='test_mail_template',
							 title='Test Mail Template',
							 subject='Test Subject',
					  		 **kwargs):
		return MailTemplate.objects.create(
			key_name=key_name,
			title=title,
			subject=subject,
			**kwargs
		)

	@pytest.mark.django_db
	def create_mail_config(self, title='Test mail config',
						   key_name='test_mail_config',
					  	   **kwargs):
		return MailConfig.objects.create(
			key_name=key_name,
			title=title,
			**kwargs
		)

	@pytest.mark.django_db
	def create_attachment(self,
					      file='test_file.txt',
					      **kwargs):
		return Attachment.objects.create(
			file=file,
			**kwargs
		)

	@pytest.mark.django_db
	def setUp(self):
		self.user = User.objects.create_superuser('testuser', 
											 'testuser@gmail.com'
											 'testing321')
		self.mail_template = self.create_mail_template()
		self.mail_config = self.create_mail_config(mailtemplate=self.mail_template)
		self.attachment = self.create_attachment()

class OverviewMailConfigTestCase(BaseViewTestCase):
	'''
	test overview_tab view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewmailconfig'
		super(OverviewMailConfigTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'mailconfigs/index.html')
		with self.subTest():
			self.assertContains(resp, _(self.mail_config.title))
		with self.subTest():
			self.assertTrue(resp.context['configs'])


class AddMailConfigTestCase(BaseViewTestCase):
	'''
	test add_mailconfig view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addmailconfig'
		super(AddMailConfigTestCase, self).__init__(*args, **kwargs)

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
			self.assertTemplateUsed(resp, 'mailconfigs/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], MailConfigForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'mailconfigs/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], MailConfigForm)
		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		data = {
			'title': 'Test Mail Config 2',
			'key_name': 'test_mail_config_2',
			'active': False,
			'mailtemplate': self.create_mail_template(key_name='test_mail_temp_2').id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailconfig'))
		with self.subTest():
			self.assertTemplateUsed(resp, 'mailconfigs/index.html')
		with self.subTest():
			self.assertContains(resp, _('The mailconfig has been succesfully added!'))


class EditMailConfigTestCase(BaseViewTestCase):
	'''
	test edit_mailconfig view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'editmailconfig'
		super(EditMailConfigTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.mail_config.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.mail_config.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'mailconfigs/edit.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], MailConfigForm)
		with self.subTest():
			self.assertIsInstance(resp.context['instance'], MailConfig)

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		new_mail_config = self.create_mail_config()
		data = {
			'title': 'New Test Mail Config',
			'key_name': 'new_test_mail_config',
			'active': new_mail_config.active,
			'mailtemplate': self.create_mail_template(key_name='new_mail_config_temp').id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[new_mail_config.id])
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailconfig'))
		new_mail_config.refresh_from_db()
		with self.subTest(msg="Test changed data"):
			self.assertEqual(new_mail_config.title, data['title'])


class DeleteAjaxMailConfigModalTestCase(BaseViewTestCase):
	'''
	test delete_ajax_mailconfig_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodalmailconfig'
		super(DeleteAjaxMailConfigModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(MailConfig.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(MailConfig.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.mail_config.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertIn('Weet u zeker dat u wilt verwijderen?', 
						  resp.json()['template'])

class ToggleMailConfigActivationViewTestCase(BaseViewTestCase):
	'''
	test toggle_mailconfig_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'activate-mailconfig'
		super(ToggleMailConfigActivationViewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.mail_config.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)


	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[id])
		with self.assertRaises(MailConfig.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.mail_config.id])
		resp = self.client.get(url)
		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailconfig'))
		self.mail_config.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.mail_config.active)

class DeleteMailConfigTestCase(BaseViewTestCase):
	'''
	test delete_mailconfig view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemailconfig'
		super(DeleteMailConfigTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.mail_config.pk])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.mail_config.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailconfig'))
		self.mail_config.refresh_from_db()
		with self.subTest(msg='Test date deleted'):
			self.assertTrue(self.mail_config.date_deleted)

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(MailConfig.DoesNotExist):
			resp = self.client.get(url)

class OverviewMailTemplateTestCase(BaseViewTestCase):
	'''
	test overview_mail_templates view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url = 'overviewmailtemplate'
		super(OverviewMailTemplateTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_view_with_login(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url)
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'mailtemplates/index.html')
		with self.subTest():
			self.assertContains(resp, _(self.mail_template.title))
		with self.subTest():
			self.assertTrue(resp.context['templates'])


class AddMailTemplateTestCase(BaseViewTestCase):
	'''
	test add_mailtemplate view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'addmailtemplate'
		super(AddMailTemplateTestCase, self).__init__(*args, **kwargs)

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
			self.assertTemplateUsed(resp, 'mailtemplates/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], MailTemplateForm)

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data={})

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'mailtemplates/add.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], MailTemplateForm)
		with self.subTest():
			self.assertFalse(resp.context['form'].is_valid())
		form = resp.context['form']
		with self.subTest(msg='Test key_name error msg'):
			self.assertEqual(form.errors['key_name'][0], 
							_('Please enter a unique keyname'))
		with self.subTest(msg='Test title error msg'):
			self.assertEqual(form.errors['title'][0], 
							_('Please enter a title'))

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		data = {
			'title': 'Test Mail Template',
			'key_name': 'test_mail_template_updated',
			'active': False,
			'subject': 'Test Subject',
			'content_html': '<h1>Hello</h1>',
			'attachments': [self.create_attachment().id]
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)
		resp = self.client.post(url, data=data, follow=True)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailtemplate'))
		with self.subTest():
			self.assertContains(resp, _('The mailtemplate has been succesfully added!'))


class EditMailTempalteTestCase(BaseViewTestCase):
	'''
	test edit_mailtemplate view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'editmailtemplate'
		super(EditMailTempalteTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.mail_template.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.mail_template.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			self.assertTemplateUsed(resp, 'mailtemplates/edit.html')
		with self.subTest():
			self.assertIsInstance(resp.context['form'], MailTemplateForm)
		with self.subTest():
			self.assertIsInstance(resp.context['instance'], MailTemplate)

	@pytest.mark.django_db
	def test_view_post_request_valid_data(self):
		new_mail_template = self.create_mail_template(key_name='new_mail_template_key')
		data = {
			'title': 'New Mail Template',
			'key_name': 'new_mail_template_key_updated',
			'active': new_mail_template.active,
			'subject': new_mail_template.subject,
			'content_html': new_mail_template.content_html or '',
			'attachments': [att.id for att in new_mail_template.attachments.all()]
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[new_mail_template.id])
		resp = self.client.post(url, data=data)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailtemplate'))
		new_mail_template.refresh_from_db()
		with self.subTest(msg="Test changed data"):
			self.assertEqual(new_mail_template.title, data['title'])

class DeleteAjaxMailTemplateModalTestCase(BaseViewTestCase):
	'''
	test delete_ajax_mailtemplate_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemodalmailtemplate'
		super(DeleteAjaxMailTemplateModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(MailTemplate.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf)

		with self.assertRaises(MailTemplate.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_post_request_valid_data(self):
		data = {
			'id': self.mail_template.id
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


class ToggleMailTemplateActivationViewTestCase(BaseViewTestCase):
	'''
	test toggle_mailconfig_activation_view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'activate-mailtemplates'
		super(ToggleMailTemplateActivationViewTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.mail_template.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_with_wrong_pk(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[id])
		with self.assertRaises(MailTemplate.DoesNotExist):
			resp = self.client.get(url)

	@pytest.mark.django_db
	def test_view_with_valid_pk(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.mail_template.id])
		resp = self.client.get(url)
		with self.subTest(msg='Status code'):
			self.assertEqual(resp.status_code, 302)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailtemplate'))
		self.mail_template.refresh_from_db()
		with self.subTest():
			self.assertTrue(self.mail_template.active)

class DeleteMailTemplateTestCase(BaseViewTestCase):
	'''
	test delete_mailtemplate view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'deletemailtemplate'
		super(DeleteMailTemplateTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=[self.mail_template.pk])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[self.mail_template.id])
		resp = self.client.get(url)

		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailtemplate'))
		self.mail_template.refresh_from_db()
		with self.subTest(msg='Test date deleted'):
			self.assertTrue(self.mail_template.date_deleted)

	def test_view_post_request_wrong_pk(self):
		pk = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=[pk])

		with self.assertRaises(MailTemplate.DoesNotExist):
			resp = self.client.get(url)


class GetVersionAjaxModalTestCase(BaseViewTestCase):
	'''
	test get_version_ajax_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf_1 = 'mailtemplateversionmodal'
		self.view_url_conf_2 = 'mailconfigversionmodal'
		super(GetVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

	def test_view_mode_template_without_login(self):
		url = reverse(self.view_url_conf_1)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_mode_config_without_login(self):
		url = reverse(self.view_url_conf_2)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	def test_view_mode_template_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf_1)

		with self.assertRaises(MailTemplate.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_config_get_request(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf_2)

		with self.assertRaises(MailConfig.DoesNotExist):
			resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_template_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf_1)

		with self.assertRaises(MailTemplate.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_view_mode_config_post_request_empty_data(self):
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf_2)

		with self.assertRaises(MailConfig.DoesNotExist):
			resp = self.client.post(url, 
									data={}, 
									HTTP_X_REQUESTED_WITH='XMLHttpRequest')


	def test_view_mode_template_post_request_valid_data(self):
		data = {
			'id': self.mail_template.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf_1)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Versions')
			self.assertContains(resp, text)

	def test_view_mode_tab_post_request_valid_data(self):
		data = {
			'id': self.mail_config.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf_2)
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Versions')
			self.assertContains(resp, text)


class DeleteVersionAjaxModalTestCase(BaseViewTestCase):
	'''
	test get_delete_version_ajax_modal view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'maildeleteversionmodal'
		super(DeleteVersionAjaxModalTestCase, self).__init__(*args, **kwargs)

	def test_view_without_login(self):
		url = reverse(self.view_url_conf, args=['module'])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)

	# def test_view_mode_module_post_request_empty_data(self):
	# 	self.client.force_login(self.user)
	# 	url = reverse(self.view_url_conf, args=['module'])

	# 	with self.assertRaises(ModuleVersion.DoesNotExist):
	# 		resp = self.client.post(url, 
	# 								data={}, 
	# 								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	# def test_view_mode_tab_post_request_empty_data(self):
	# 	self.client.force_login(self.user)
	# 	url = reverse(self.view_url_conf, args=['tab'])

	# 	with self.assertRaises(TabVersion.DoesNotExist):
	# 		resp = self.client.post(url, 
	# 								data={}, 
	# 								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	@pytest.mark.django_db
	def test_view_mode_template_post_request_valid_data(self):
		revision = MailTemplateRevision.objects.get(current_instance=self.mail_template)
		version = revision.versions.all().first()
		data = {
			'id': version.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['template'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Are you sure you want to delete this version?')
			self.assertContains(resp, text)

	@pytest.mark.django_db
	def test_view_mode_config_post_request_valid_data(self):
		revision = MailConfigRevision.objects.get(current_instance=self.mail_config)
		version = revision.versions.all().first()
		data = {
			'id': version.id
		}

		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['config'])
		resp = self.client.post(url, 
								data=data,
								HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		with self.subTest():
			self.assertEqual(resp.status_code, 200)
		with self.subTest():
			text = _('Are you sure you want to delete this version?')
			self.assertContains(resp, text)


class SelectVersionTestCase(BaseViewTestCase):
	'''
	test select_version view
	'''

	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'mailselectversion'
		super(SelectVersionTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_select_version_mode_template_with_valid_version_id(self):
		revision = MailTemplateRevision.objects.get(current_instance=self.mail_template)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['template', version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('overviewmailtemplate'))
		version.refresh_from_db()
		with self.subTest():
			self.assertTrue(version.is_current)

	@pytest.mark.django_db
	def test_select_version_mode_config_with_valid_version_id(self):
		revision = MailConfigRevision.objects.get(current_instance=self.mail_config)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['config', version.id])
		resp = self.client.get(url)

		with self.subTest(msg='Valid Version id'):
			self.assertRedirects(resp, reverse('overviewmailconfig'))
		version.refresh_from_db()
		with self.subTest():
			self.assertTrue(version.is_current)

	def test_select_version_mode_template_with_wrong_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['template', id])
		resp = self.client.get(url)
		self.assertRedirects(resp, reverse('overviewmailtemplate'))


	def test_select_version_mode_config_with_wrong_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['config', id])
		resp = self.client.get(url)
		self.assertRedirects(resp, reverse('overviewmailconfig'))


class DeleteVersionTestCase(BaseViewTestCase):
	'''
	test delete_version view
	'''
	def __init__(self, *args, **kwargs):
		self.view_url_conf = 'maildeleteversion'
		super(DeleteVersionTestCase, self).__init__(*args, **kwargs)

	@pytest.mark.django_db
	def test_delete_version_mode_template_with_valid_version_id(self):
		revision = MailTemplateRevision.objects.get(current_instance=self.mail_template)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['template', version.id])
		resp = self.client.get(url, follow=True)
		
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailtemplate'))
		with self.subTest(msg='Test contains'):
			self.assertContains(resp, _('De versie is succesvol verwijderd'))

	@pytest.mark.django_db
	def test_delete_version_mode_config_with_valid_version_id(self):
		revision = MailConfigRevision.objects.get(current_instance=self.mail_config)
		version = revision.versions.all().first()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['config', version.id])
		resp = self.client.get(url, follow=True)
		
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailconfig'))
		with self.subTest(msg='Test contains'):
			self.assertContains(resp, _('De versie is succesvol verwijderd'))

	def test_delete_version_mode_template_with_wrong_version_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['template', id])

		resp = self.client.get(url)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailtemplate'))

	def test_delete_version_mode_config_with_wrong_version_id(self):
		id = uuid.uuid4()
		self.client.force_login(self.user)
		url = reverse(self.view_url_conf, args=['config', id])

		resp = self.client.get(url)
		with self.subTest():
			self.assertRedirects(resp, reverse('overviewmailconfig'))
