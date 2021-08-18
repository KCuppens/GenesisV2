from django.db import models
from apps.base.models import (
    BaseModel, 
    AdminModel,
    BaseRevision,
    BaseVersion
)
from collections import namedtuple
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from apps.mail.validators import validate_template_syntax, validate_email_with_name
from apps.mail.fields import CommaSeparatedEmailField
from apps.mail.settings import context_field_class, get_log_level, get_template_engine
from jsonfield import JSONField

# Create your models here.
class MailTemplateManager(models.Manager):
    def get_by_key_name(self, keyname):
        return self.filter(key_name=keyname).first()

class Attachment(models.Model):
    """
    A model describing an email attachment.
    """
    file = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255, default='', blank=True)

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return self.name

class MailTemplate(BaseModel, AdminModel):
    key_name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True,
        verbose_name=_("Subject"), validators=[validate_template_syntax])
    image = models.CharField(max_length=255, null=True, blank=True)
    content_html = models.TextField(null=True, blank=True,
        verbose_name=_("Content"), validators=[validate_template_syntax])
    content_plain = models.TextField(null=True, blank=True,
        verbose_name=_("Content"), validators=[validate_template_syntax])
    content_json = models.TextField(null=True, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)

    objects = MailTemplateManager()

    def __str__(self):
        return self.title




class MailConfig(BaseModel, AdminModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    key_name = models.CharField(max_length=255, null=True, blank=True)
    mailtemplate = models.ForeignKey(MailTemplate, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

PRIORITY = namedtuple('PRIORITY', 'low medium high now')._make(range(4))
STATUS = namedtuple('STATUS', 'sent failed queued requeued')._make(range(4))

class Email(models.Model):
    """
    A model to hold email information.
    """

    PRIORITY_CHOICES = [(PRIORITY.low, _("low")), (PRIORITY.medium, _("medium")),
                        (PRIORITY.high, _("high")), (PRIORITY.now, _("now"))]
    STATUS_CHOICES = [(STATUS.sent, _("sent")), (STATUS.failed, _("failed")),
                      (STATUS.queued, _("queued")), (STATUS.requeued, _("requeued"))]

    from_email = models.CharField(_("Email From"), max_length=254,
                                  validators=[validate_email_with_name])
    to = CommaSeparatedEmailField(_("Email To"))
    cc = CommaSeparatedEmailField(_("Cc"))
    bcc = CommaSeparatedEmailField(_("Bcc"))
    subject = models.CharField(_("Subject"), max_length=989, blank=True)
    message = models.TextField(_("Message"), blank=True)
    html_message = models.TextField(_("HTML Message"), blank=True)
    """
    Emails with 'queued' status will get processed by ``send_queued`` command.
    Status field will then be set to ``failed`` or ``sent`` depending on
    whether it's successfully delivered.
    """
    status = models.PositiveSmallIntegerField(
        _("Status"),
        choices=STATUS_CHOICES, db_index=True,
        blank=True, null=True)
    priority = models.PositiveSmallIntegerField(_("Priority"),
                                                choices=PRIORITY_CHOICES,
                                                blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(db_index=True, auto_now=True)
    scheduled_time = models.DateTimeField(_("Scheduled Time"),
                                          blank=True, null=True, db_index=True,
                                          help_text=_("The scheduled sending time"))
    expires_at = models.DateTimeField(_("Expires"),blank=True, null=True)
    number_of_retries = models.PositiveIntegerField(null=True, blank=True)
    headers = JSONField(_('Headers'), blank=True, null=True)
    template = models.ForeignKey(MailTemplate, blank=True,
                                 null=True, verbose_name=_("Email template"),
                                 on_delete=models.CASCADE)
    context = context_field_class(_('Context'), blank=True, null=True)
    backend_alias = models.CharField(_("Backend alias"), blank=True, default='',
                                     max_length=64)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_email_message = None

    def __str__(self):
        return '%s' % self.to

    def email_message(self):
        """
        Returns Django EmailMessage object for sending.
        """
        if self._cached_email_message:
            return self._cached_email_message

        return self.prepare_email_message()

    def prepare_email_message(self):
        """
        Returns a django ``EmailMessage`` or ``EmailMultiAlternatives`` object,
        depending on whether html_message is empty.
        """
        if self.template is not None:
            engine = get_template_engine()
            subject = engine.from_string(self.template.subject).render(self.context)
            plaintext_message = engine.from_string(self.template.content_plain).render(self.context)
            multipart_template = engine.from_string(self.template.content_html)
            html_message = multipart_template.render(self.context)

        else:
            subject = smart_str(self.subject)
            plaintext_message = self.message
            multipart_template = None
            html_message = self.html_message

        connection = connections[self.backend_alias or 'default']
        if isinstance(self.headers, dict) or self.expires_at or self.message_id:
            headers = dict(self.headers or {})
        else:
            headers = None

        if html_message:
            if plaintext_message:
                msg = EmailMultiAlternatives(
                    subject=subject, body=plaintext_message, from_email=self.from_email,
                    to=self.to, bcc=self.bcc, cc=self.cc,
                    headers=headers, connection=connection)
                msg.attach_alternative(html_message, "text/html")
            else:
                msg = EmailMultiAlternatives(
                    subject=subject, body=html_message, from_email=self.from_email,
                    to=self.to, bcc=self.bcc, cc=self.cc,
                    headers=headers, connection=connection)
                msg.content_subtype = 'html'
            if hasattr(multipart_template, 'attach_related'):
                multipart_template.attach_related(msg)

        else:
            msg = EmailMessage(
                subject=subject, body=plaintext_message, from_email=self.from_email,
                to=self.to, bcc=self.bcc, cc=self.cc,
                headers=headers, connection=connection)

        for attachment in self.attachments.all():
            if attachment.headers:
                mime_part = MIMENonMultipart(*attachment.mimetype.split('/'))
                mime_part.set_payload(attachment.file.read())
                for key, val in attachment.headers.items():
                    try:
                        mime_part.replace_header(key, val)
                    except KeyError:
                        mime_part.add_header(key, val)
                msg.attach(mime_part)
            else:
                msg.attach(attachment.name, attachment.file.read(), mimetype=attachment.mimetype or None)
            attachment.file.close()

        self._cached_email_message = msg
        return msg

    def dispatch(self, log_level=None,
                 disconnect_after_delivery=True, commit=True):
        """
        Sends email and log the result.
        """
        try:
            self.email_message().send()
            status = STATUS.sent
            message = ''
            exception_type = ''
        except Exception as e:
            status = STATUS.failed
            message = str(e)
            exception_type = type(e).__name__

            # If run in a bulk sending mode, reraise and let the outer
            # layer handle the exception
            if not commit:
                raise

        if disconnect_after_delivery:
            connections.close()

        if commit:
            self.status = status
            self.save(update_fields=['status'])

            if log_level is None:
                log_level = get_log_level()

            # If log level is 0, log nothing, 1 logs only sending failures
            # and 2 means log both successes and failures
            if log_level == 1:
                if status == STATUS.failed:
                    self.logs.create(status=status, message=message,
                                     exception_type=exception_type)
            elif log_level == 2:
                self.logs.create(status=status, message=message,
                                 exception_type=exception_type)

        return status

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class MailTemplateRevision(BaseRevision):
    current_instance = models.OneToOneField(MailTemplate, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, default="mail_temp")


class MailTemplateVersion(BaseVersion):
    revision = models.ForeignKey(MailTemplateRevision, on_delete=models.CASCADE, related_name="versions")

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        if not self.is_current:
            return super(self._meta.model, self).save(*args, **kwargs)
        with transaction.atomic():
            self.revision.versions.filter(
                is_current=True).update(is_current=False)
            return super(self._meta.model, self).save(*args, **kwargs)


class MailConfigRevision(BaseRevision):
    current_instance = models.OneToOneField(MailConfig, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, default="mail_conf")


class MailConfigVersion(BaseVersion):
    revision = models.ForeignKey(MailConfigRevision, on_delete=models.CASCADE, related_name="versions")

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        if not self.is_current:
            return super(self._meta.model, self).save(*args, **kwargs)
        with transaction.atomic():
            self.revision.versions.filter(
                is_current=True).update(is_current=False)
            return super(self._meta.model, self).save(*args, **kwargs)