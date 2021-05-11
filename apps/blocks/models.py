from django.db import models
from apps.base.models import BaseModel, AdminModel, BaseRevision, BaseVersion
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Block(BaseModel, AdminModel):
    name = models.CharField(max_length=55, db_index=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to="blocks/images")
    category = models.ManyToManyField('blockcategory', blank=True)
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

    has_block_elements = models.BooleanField(default=False)
    has_block_element_title = models.BooleanField(default=False)
    has_block_element_image = models.BooleanField(default=False)
    has_block_element_content = models.BooleanField(default=False)
    has_block_element_subtitle = models.BooleanField(default=False)
    has_block_element_image_second = models.BooleanField(default=False)

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class BlockCategory(BaseModel, AdminModel):
    name = models.CharField(max_length=55, db_index=True, blank=True)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = _('Blockcategory')

    def __str__(self):
        return self.name


class BlocksRevision(BaseRevision):
    current_instance = models.OneToOneField(Block, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, default="block")


class BlocksVersion(BaseVersion):
    revision = models.ForeignKey(BlocksRevision, on_delete=models.CASCADE, related_name="versions")

    def save(self, *args, **kwargs):
        try:
            blocksversion = BlocksVersion.objects.get(id=self.id)
            for version in BlocksVersion.objects.exclude(id=self.id):
                if self.is_current:
                    version.is_current = False
                    version.save()
        except:
            for version in BlocksVersion.objects.exclude(id=self.id):
                version.is_current = False
                version.save()
        super().save(*args, **kwargs)
