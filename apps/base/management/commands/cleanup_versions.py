from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import glob, os
from datetime import datetime, timedelta
d = datetime.today() - timedelta(days=settings.VERSION_DELETE_DAYS)
from apps.pages.models import PageVersion
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.blocks.models import BlockCategory, BlocksVersion
from apps.filemanager.models import DirectoryVersion, MediaVersion
from apps.formbuilder.models import FormVersion
from apps.mail.models import MailTemplateVersion, MailConfigVersion
from apps.modules.models import ModuleVersion, TabVersion
from apps.news.models import Article, NewsVersion

class Command(BaseCommand):
    help = 'Cleanup versions with date_created older than settings.VERSION_DELETE_DAYS'

    def handle(self, *args, **kwargs):
        models = ['BlocksVersion', 'FormVersion', 'MailTemplateVersion',
        		  'MailConfigVersion', 'ModuleVersion', 'TabVersion',
        		  'NewsVersion', 'PageVersion', 'DirectoryVersion',
                  'MediaVersion']
        count = 0
        for model in models:
            qs = eval(model).objects.filter(date_created__lt=d, is_current=False)
            for object in qs:
                object.delete()
                count += 1
        print(str(count) + ' objects deleted')
