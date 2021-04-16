from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import glob, os
from datetime import datetime, timedelta
d = datetime.today() - timedelta(days=30)
from apps.pages.models import Page, Canvas, CanvasRow, CanvasCol, CanvasColBlock, PageBlock
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.blocks.models import Block, BlockCategory
from apps.dashboard.models import DashboardConfiguration
from apps.filemanager.models import Directory, Media 
from apps.formbuilder.models import Form, FormResult
from apps.mail.models import MailTemplate, MailConfig 
from apps.modules.models import Tab, Module, ModulePage
from apps.news.models import Article

class Command(BaseCommand):
    help = 'Cleanup objects with date_deleted older than 30 days'

    def handle(self, *args, **kwargs):
        models = ['Page', 'Canvas', 'CanvasRow', 'CanvasCol', 'CanvasColBlock', 'PageBlock', 'Group', 'User', 'Article', 'Block', 'BlockCategory', 'DashboardConfiguration', 'Directory', 'Media', 'Form', 'FormResult', 'MailTemplate', 'MailConfig', 'Module', 'ModulePage', 'Tab']
        count = 0
        for model in models:
            qs = eval(model).objects.filter(date_deleted__lt=d)
            for object in qs:
                object.delete()
                count += 1
        print(str(count) + ' objects deleted')
