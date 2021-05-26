import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from apps.mail.models import (
	MailTemplate,
	MailConfig,
	Attachment
)
from apps.mail.forms import MailTemplateForm, MailConfigForm


class BaseFormTestCase(TestCase):

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


class MailTemplateFormTestCase(BaseFormTestCase):
	'''
	test MailTemplateForm
	'''

	def test_with_empty_data(self):
		form = MailTemplateForm(data={})
		self.assertFalse(form.is_valid())

	def test_with_empty_data_error_msgs(self):
		form = MailTemplateForm(data={})
		self.assertFalse(form.is_valid())
		with self.subTest(msg='Test key_name error msg'):
			self.assertEqual(form.errors['key_name'][0], 
							_('Please enter a unique keyname'))
		with self.subTest(msg='Test title error msg'):
			self.assertEqual(form.errors['title'][0], 
							_('Please enter a title'))

	def test_with_partial_data(self):
		data = {
			'title': 'Test Mail Template',
			'key_name': 'test_mail_template'
		}
		form = MailTemplateForm(data=data)
		self.assertTrue(form.is_valid())

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'title': 'Test Mail Template',
			'key_name': 'test_mail_template',
			'active': False,
			'subject': 'Test Subject',
			'content_html': '<h1>Hello</h1>',
			'attachments': [self.create_attachment().id]
		}
		form = MailTemplateForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form, MailTemplateForm)
		with self.subTest():
			self.assertIsInstance(form.save(), MailTemplate)

	@pytest.mark.django_db
	def test_partial_update_with_instance(self):
		mail_template = self.create_mail_template()
		data = {
			'title': 'New Mail Template'
		}
		form = MailTemplateForm(data=data, instance=mail_template)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of name'):
			self.assertEqual(form.save().title, data['title'])



class MailConfigFormTestCase(BaseFormTestCase):
	'''
	test MailConfigForm
	'''

	def test_with_empty_data(self):
		form = MailConfigForm(data={})
		self.assertFalse(form.is_valid())

	def test_with_empty_data_error_msgs(self):
		form = MailConfigForm(data={})
		self.assertFalse(form.is_valid())
		with self.subTest(msg='Test key_name error msg'):
			self.assertEqual(form.errors['key_name'][0], 
							_('Please enter a unique keyname'))
		with self.subTest(msg='Test title error msg'):
			self.assertEqual(form.errors['title'][0], 
							_('Please enter a title'))

	def test_with_partial_data(self):
		data = {
			'title': 'Test Mail config',
			'key_name': 'test_mail_config'
		}
		form = MailConfigForm(data=data)
		self.assertTrue(form.is_valid())

	@pytest.mark.django_db
	def test_with_valid_data(self):
		data = {
			'title': 'Test Mail Config',
			'key_name': 'test_mail_config',
			'active': False,
			'mailtemplate': self.create_mail_template()
		}
		form = MailConfigForm(data=data)
		
		with self.subTest():
			self.assertTrue(form.is_valid())
		with self.subTest():
			self.assertIsInstance(form, MailConfigForm)
		with self.subTest():
			self.assertIsInstance(form.save(), MailConfig)

	@pytest.mark.django_db
	def test_partial_update_with_instance(self):
		mail_template = self.create_mail_template()
		mail_config = self.create_mail_config()
		data = {
			'title': 'New Mail Config',
			'key_name': mail_config.key_name,
			'active': mail_config.active,
			'mailtemplate': mail_template
		}
		form = MailConfigForm(data=data, instance=mail_config)
		
		with self.subTest(msg='Test validity'):
			self.assertTrue(form.is_valid())
		with self.subTest(msg='Test change of name'):
			self.assertEqual(form.save().title, data['title'])
		with self.subTest(msg='Test mailtemplate instance'):
			self.assertIsInstance(form.save().mailtemplate, 
								  MailTemplate)
