from django.db import models
from apps.base.models import BaseModel, SortableModel, AdminModel
from django.utils.translation import ugettext_lazy as _
from apps.feathericons.models import Icon

# Create your models here.

class DashboardConfiguration(BaseModel, SortableModel, AdminModel):
    ORDER_TYPE_ASC = 'asc'
    ORDER_TYPE_DESC = 'desc'

    ORDER_TYPES = [
        (ORDER_TYPE_ASC, _('Oplopend')),
        (ORDER_TYPE_DESC, _('Aflopend'))
    ]

    SORT_BY_POSITION = 'position'
    SORT_BY_NAME = 'title'
    SORT_BY_DATE = 'date_published'

    SORT_TYPES = [
        (SORT_BY_POSITION, _('Sorteren op positie')),
        (SORT_BY_NAME, _('Sorteren op naam')),
        (SORT_BY_DATE, _('Sorteren op datum'))
    ]

    METHOD_COUNT_FILES_BY_TYPE = 'count_files_by_type'
    METHOD_COUNT_FILES = 'count_files'
    METHOD_COUNT_DIRS = 'count_dirs'
    METHOD_COUNT_FILEMANAGER_SIZE = 'count_filemanager_size'
    METHOD_LATEST_HISTORY = 'latest_history'
    METHOD_LATEST_PAGES = 'latest_pages'
    METHOD_COUNT_PAGES = 'count_pages'
    METHOD_LATEST_USERS = 'latest_users'
    METHOD_COUNT_USERS = 'count_users'
    

    GET_METHODS = [
        (METHOD_COUNT_FILES_BY_TYPE, _('Count files by media type')),
        (METHOD_COUNT_FILES, _('Count files')),
        (METHOD_COUNT_DIRS, _('Count directories')),
        (METHOD_COUNT_FILEMANAGER_SIZE, _('Count filemanager size')),
        (METHOD_LATEST_HISTORY, _('Latest history')),
        (METHOD_LATEST_PAGES, _('Latest pages')),
        (METHOD_COUNT_PAGES, _('Count pages')),
        (METHOD_LATEST_USERS, _('Latest users')),
        (METHOD_COUNT_USERS, _('Count users'))
    ]

    title = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(choices=GET_METHODS, default=METHOD_COUNT_USERS, max_length=255, null=True, blank=True)
    param1 = models.CharField(max_length=255, null=True, blank=True) 
    sort = models.CharField(choices=SORT_TYPES, default=SORT_BY_NAME, max_length=255, null=True, blank=True) 
    order = models.CharField(choices=ORDER_TYPES, default=ORDER_TYPE_DESC, max_length=255, null=True, blank=True) 
    template = models.CharField(max_length=255, null=True, blank=True) 
    icon = models.ForeignKey(Icon, on_delete=models.CASCADE, blank=True, null=True)

    #modules
    default = models.BooleanField(default=False)

    