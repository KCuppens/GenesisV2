import pytest
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.mail.models import (
	MailTemplate,
	MailConfig,
	MailTemplateRevision,
	MailTemplateVersion,
	MailConfigRevision, 
	MailConfigVersion,
	Attachment
)

class BaseModelTestCase(TestCase):

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


class MailTemplateModelTestCase(BaseModelTestCase):

	def test_model_instance_type(self):
		mail_template = self.create_mail_template()
		self.assertIsInstance(mail_template, MailTemplate)

		with self.subTest(msg='Test title'):
			self.assertEqual(mail_template.title, 'Test Mail Template')

	@pytest.mark.django_db
	def test_model_m2m_attachments_field(self):
		mail_template = self.create_mail_template()
		attachment = self.create_attachment()
		mail_template.attachments.set([attachment.pk])
		self.assertEqual(mail_template.attachments.count(), 1)

	@pytest.mark.django_db
	def test_model_revision(self):
		mail_template = self.create_mail_template()
		revision = MailTemplateRevision.objects.get(current_instance=mail_template)
		self.assertIsInstance(revision, MailTemplateRevision)


	@pytest.mark.django_db
	def test_model_version(self):
		mail_template = self.create_mail_template()
		revision = MailTemplateRevision.objects.get(current_instance=mail_template)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 1)

		with self.subTest():
			self.assertIsInstance(versions.first(), MailTemplateVersion)


class MailConfigModelTest(BaseModelTestCase):

	def test_model_instance_type(self):
		mail_template = self.create_mail_template()
		mail_config = self.create_mail_config(mailtemplate=mail_template)
		self.assertIsInstance(mail_config, MailConfig)

		with self.subTest(msg='Test title'):
			self.assertEqual(mail_config.title, 'Test mail config')

	def test_model_without_mailtemplate(self):
		with self.assertRaises(ValueError):
			mail_config = self.create_mail_config(mailtemplate='')

	@pytest.mark.django_db
	def test_model_revision(self):
		mail_template = self.create_mail_template()
		mail_config = self.create_mail_config(mailtemplate=mail_template)
		revision = MailConfigRevision.objects.get(current_instance=mail_config)
		self.assertIsInstance(revision, MailConfigRevision)

	@pytest.mark.django_db
	def test_model_version(self):
		mail_template = self.create_mail_template()
		mail_config = self.create_mail_config(mailtemplate=mail_template)
		revision = MailConfigRevision.objects.get(current_instance=mail_config)
		versions = revision.versions.all()
		self.assertEqual(versions.count(), 1)

		with self.subTest():
			self.assertIsInstance(versions.first(), MailConfigVersion)

