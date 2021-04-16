from apps.logs.models import Message 
import datetime 
now = datetime.datetime.now()
from django.utils.translation import ugettext_lazy as _

def create_message_log(recipient, subject, type):
    return Message.objects.create(recipient=recipient, subject=subject, type=type)

def set_message_invoiced(message):
    message.invoiced = now
    message.save()