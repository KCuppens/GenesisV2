from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import glob, os
from apps.formbuilder.models import Form, FormPage, FormElement, FormElementOption


class Command(BaseCommand):
    help = 'Cleanup unused objects from form'

    def handle(self, *args, **kwargs):
        used_pages = []
        forms = Form.objects.filter(date_deleted=None)
        for form in forms:
            for page in form.pages.all():
                if not page in used_pages:
                    used_pages.append(page.id)
        element_count = 0
        option_count = 0
        page_count = 0
        all_pages = FormPage.objects.filter()
        for page in all_pages:
            if not page.id in used_pages:
                if page.elements.exists():
                    for element in page.elements.all():
                        if element.options.exists():
                            for option in element.options.all():
                                option.delete()
                                option_count+=1
                    element.delete()
                    element_count+=1
                page.delete()
                page_count+=1
        print(str(element_count) + ' element objects deleted')
        print(str(option_count) + ' option objects deleted')
        print(str(page_count) + ' page objects deleted')
