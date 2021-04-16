from django.db import models
from apps.base.models import BaseModel, AdminModel
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Block(BaseModel, AdminModel):
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
        (TYPE_COL_12, 'Twaalf kolommen'),
    ]
    name = models.CharField(max_length=55, db_index=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to="blocks/images")
    category = models.ManyToManyField('blockcategory', blank=True)
    col_size = models.IntegerField(choices=COL_TYPES, default=TYPE_COL_4)
    template =  models.CharField(max_length=255, null=True, blank=True)
    detailpage_only = models.BooleanField(default=False)

    has_title = models.BooleanField(default=True)
    has_subtitle = models.BooleanField(default=False)
    has_content = models.BooleanField(default=True)
    has_image = models.BooleanField(default=True)
    has_image_second = models.BooleanField(default=False)
    has_url = models.BooleanField(default=False) 
    has_url_text = models.BooleanField(default=False)    
    has_video = models.BooleanField(default=False)
    has_embed = models.BooleanField(default=False)
    has_form = models.BooleanField(default=False)

    has_sort_method = models.BooleanField(default=False)
    has_limit = models.BooleanField(default=False)
    has_sort_order = models.BooleanField(default=False)
    has_pagination = models.BooleanField(default=False)
    has_module = models.BooleanField(default=False)
    has_detailpage = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Block')
    
    def __str__(self):
        return self.name


class BlockCategory(BaseModel, AdminModel):
    name = models.CharField(max_length=55, db_index=True, blank=True)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = _('Blockcategory')

    def __str__(self):
        return self.name
