from django.db import models
from apps.base.models import BaseModel, AdminModel
from django_extensions.db.fields import AutoSlugField
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
        (TYPE_COL_12, 'Twaal kolommen'),
    ]
    name = models.CharField(max_length=55, db_index=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to="blocks/images")
    category = models.ManyToManyField('blockcategory', blank=True)
    col_size = models.IntegerField(choices=COL_TYPES, default=TYPE_COL_4)

    
    def __str__(self):
        return self.name


class BlockCategory(BaseModel, AdminModel):
    name = models.CharField(max_length=55, db_index=True, blank=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name
