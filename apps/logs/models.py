from django.db import models
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple
from django.utils.translation import gettext_lazy as _

PRIORITY = namedtuple('PRIORITY', 'low medium high now')._make(range(4))
STATUS = namedtuple('STATUS', 'sent failed queued requeued')._make(range(4))
# Create your models here.
class MessageLog(models.Model):
    """
    A model to record sending email sending activities.
    """
    TYPE_EMAIL = 'email'
    TYPE_SMS = 'sms'

    STATUS_CHOICES = [(STATUS.sent, _("sent")), (STATUS.failed, _("failed"))]

    GET_TYPES = [
        (TYPE_EMAIL, _('Email')),
        (TYPE_SMS, _('SMS'))
    ]
    date = models.DateTimeField(auto_now_add=True)
    recipient = models.CharField(max_length=255, null=True)
    invoiced = models.DateTimeField(null=True, blank=True)
    subject = models.CharField(max_length=255, null=True) 
    type = models.CharField(max_length=255, null=True, choices=GET_TYPES, default=TYPE_EMAIL)
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS_CHOICES)
    error = models.TextField(blank=True, null=True)
    exception_type = models.CharField(_('Exception type'), max_length=255, blank=True)
