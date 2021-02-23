from django.db import models
from apps.base.models import BaseModel, AdminModel, SeoModel, SortableModel
from apps.blocks.models import Block
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Page(BaseModel, AdminModel, SeoModel, SortableModel):
    URL_TYPE_GENERATED = 'generated'
    URL_TYPE_OWN = 'own'
    URL_TYPE_LINK_THROUGH = 'link-through'

    URL_TYPES = [
        (URL_TYPE_GENERATED, _('Gegenereerde slug')),
        (URL_TYPE_OWN, _('Eigen slug')),
        (URL_TYPE_LINK_THROUGH, _('Doorlink pagina'))
    ]
    is_homepage = models.BooleanField(default=False)
    in_main_menu = models.BooleanField(default=False, db_index=True)
    page_title = models.CharField(max_length=55, db_index=True, blank=True)
    menu_title = models.CharField(max_length=55, blank=True, null=True)
    #forms
    canvas = models.ForeignKey('canvas', on_delete=models.CASCADE, null=True, blank=True)
    url_type = models.CharField(default=URL_TYPE_GENERATED, choices=URL_TYPES, max_length=55)
    slug = models.SlugField(null=True, blank=True)
    full_slug = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey("self", blank=True, on_delete=models.CASCADE, related_name="children", null=True)
    depth = models.PositiveIntegerField(null=True, default=0, blank=True)

    def __str__(self):
        return self.page_title

    def is_link_through(self):
        if self.url_type == self.URL_TYPE_LINK_THROUGH:
            return True
        return False
    
    class Meta:
        verbose_name = _('Page')

class Canvas(BaseModel, AdminModel):
    rows = models.ManyToManyField('canvasrow', blank=True)

    class Meta:
        verbose_name = _('Canvas')

class CanvasRow(SortableModel, BaseModel, AdminModel):
    DEFAULT_CONTAINER = 'default'
    CONTAINER_TYPES = [
        (DEFAULT_CONTAINER, _('Default container'))
    ]
    colblock = models.ForeignKey('canvascolblock', on_delete=models.CASCADE, null=True, blank=True)
    container_class = models.CharField(default=DEFAULT_CONTAINER, choices=CONTAINER_TYPES, max_length=55)

    class Meta:
        verbose_name = _('Canvas row')

class CanvasCol(SortableModel, BaseModel, AdminModel):
    TYPE_COL_1 = 1
    TYPE_COL_2 = 2
    TYPE_COL_3 = 3
    TYPE_COL_4 = 4
    TYPE_COL_5 = 5
    TYPE_COL_6 = 6
    TYPE_COL_7 = 7
    TYPE_COL_8 = 8
    TYPE_COL_9 = 9
    TYPE_COL_10 = 10
    TYPE_COL_11 = 11
    TYPE_COL_12 = 12
    COL_TYPES = [
        (TYPE_COL_1, 'Een kolom'),
        (TYPE_COL_2, 'Twee kolommen'),
        (TYPE_COL_3, 'Drie kolommen'),
        (TYPE_COL_4, 'Vier kolommen'),
        (TYPE_COL_5, 'Vijf kolommen'),
        (TYPE_COL_6, 'Zes kolommen'),
        (TYPE_COL_7, 'Zeven kolommen'),
        (TYPE_COL_8, 'Acht kolommen'),
        (TYPE_COL_9, 'Negen kolommen'),
        (TYPE_COL_10, 'Tien kolommen'),
        (TYPE_COL_11, 'Elf kolommen'),
        (TYPE_COL_12, 'Twaal kolommen'),
    ]
    block = models.ForeignKey('pageblock', on_delete=models.CASCADE, null=True, blank=True)
    col_size = models.CharField(max_length=2, choices=COL_TYPES, default=TYPE_COL_4)

    class Meta:
        verbose_name = _('Canvas column')

class CanvasColBlock(SortableModel, BaseModel, AdminModel):
    COLBLOCK_4_4_4 = '4-4-4'
    COLBLOCK_6_6 = '6-6'
    COLBLOCK_3_3_3_3 = '3-3-3-3'
    COLBLOCK_12 = '12'
    COLBLOCK_8_4 = '8-4'
    COLBLOCK_4_8 = '4-8'
    COLBLOCK_9_3 = '9-3'
    COLBLOCK_3_9 = '3-9'
    COLBLOCK_5_2_5 = '5-2-5'
    COLBLOCK_3_6_3 = '3-6-3'
    COLBLOCK_10_2 = '10-2'
    COLBLOCK_2_10 = '2-10'

    COLBLOCKS_TYPES = [
        (COLBLOCK_4_4_4, _('Row with 3 columns')),
        (COLBLOCK_6_6, _('Row with 2 columns')),
        (COLBLOCK_3_3_3_3, _('Row with 4 columns')),
        (COLBLOCK_12, _('Row with 1 column')),
        (COLBLOCK_8_4, _('Row with 1 big and 1 small column')),
        (COLBLOCK_4_8, _('Row with 1 small and 1 big columns')),
        (COLBLOCK_9_3, _('Row with 1 very big and 1 small column')),
        (COLBLOCK_3_9, _('Row with 1 small and 1 very big column')),
        (COLBLOCK_5_2_5, _('Row with 1 medium and 1 very small and 1 medium column')),
        (COLBLOCK_3_6_3, _('Row with 1 small and 1 big and 1 small column')),
        (COLBLOCK_10_2, _('Row with 1 very large and 1 very small column')),
        (COLBLOCK_2_10, _('Row with 1 very small and 1 very large column')),
    ]

    cols = models.ManyToManyField(CanvasCol, blank=True)

    class Meta:
        verbose_name = _('Canvas column block')

class PageBlock(SeoModel, SortableModel, AdminModel, BaseModel):
    TYPE_COL_1 = 1
    TYPE_COL_2 = 2
    TYPE_COL_3 = 3
    TYPE_COL_4 = 4
    TYPE_COL_5 = 5
    TYPE_COL_6 = 6
    TYPE_COL_7 = 7
    TYPE_COL_8 = 8
    TYPE_COL_9 = 9
    TYPE_COL_10 = 10
    TYPE_COL_11 = 11
    TYPE_COL_12 = 12
    COL_TYPES = [
        (TYPE_COL_1, 'Een kolom'),
        (TYPE_COL_2, 'Twee kolommen'),
        (TYPE_COL_3, 'Drie kolommen'),
        (TYPE_COL_4, 'Vier kolommen'),
        (TYPE_COL_5, 'Vijf kolommen'),
        (TYPE_COL_6, 'Zes kolommen'),
        (TYPE_COL_7, 'Zeven kolommen'),
        (TYPE_COL_8, 'Acht kolommen'),
        (TYPE_COL_9, 'Negen kolommen'),
        (TYPE_COL_10, 'Tien kolommen'),
        (TYPE_COL_11, 'Elf kolommen'),
        (TYPE_COL_12, 'Twaal kolommen'),
    ]
    col_size = models.CharField(max_length=2, choices=COL_TYPES, default=TYPE_COL_4)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=True)

    has_title = models.BooleanField(default=True)
    has_subtitle = models.BooleanField(default=True)
    has_content = models.BooleanField(default=True)
    has_image = models.BooleanField(default=True)
    
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="blocks/", null=True, blank=True)

    class Meta:
        verbose_name = _('Page block')
  