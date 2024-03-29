from django.db import models
from apps.base.models import BaseModel, AdminModel, SeoModel, SortableModel, BaseRevision, BaseVersion
from apps.formbuilder.models import Form
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
    is_homepage = models.BooleanField(default=False, verbose_name=_('Is a homepage'))
    in_main_menu = models.BooleanField(default=False, db_index=True, verbose_name=_('In main menu'))
    in_topnav_menu = models.BooleanField(default=False, db_index=True, verbose_name=_('In Top menu'))
    in_quicklinks_menu = models.BooleanField(default=False, db_index=True, verbose_name=_('In Quicklink menu'))
    in_marked_menu = models.BooleanField(default=False, db_index=True, verbose_name=_('In gemarkeerd menu'))
    
    page_title = models.CharField(max_length=55, db_index=True, blank=True, verbose_name=_('Page title'))
    menu_title = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Menu title'))

    image = models.CharField(max_length=255, null=True, blank=True)
    #forms
    canvas = models.ForeignKey('canvas', on_delete=models.CASCADE, null=True, blank=True)
    url_type = models.CharField(default=URL_TYPE_GENERATED, choices=URL_TYPES, max_length=55, verbose_name=_('URL Type'))
    slug = AutoSlugField(populate_from='page_title', null=True)
    linkthrough = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Linkthrough'))
    full_slug = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Full route'))
    parent = models.ForeignKey("self", blank=True, on_delete=models.CASCADE, related_name="children", null=True, verbose_name=_('Bovenstaande pagina'))

    has_detailpage = models.BooleanField(default=False)
    detailpage_models = models.CharField(max_length=255, null=True, blank=True)
    is_deletable = models.BooleanField(null=True, default=True)
    
    
    def __str__(self):
        return self.page_title

    def is_link_through(self):
        if self.url_type == self.URL_TYPE_LINK_THROUGH:
            return True
        return False

    def get_url(self):
        return 'editpage'

    def fetch_seo_title(self):
        if self.meta_title:
            return self.meta_title
        else:
            return self.page_title

    def fetch_seo_description(self):
        if self.meta_description:
            return self.meta_description

    def fetch_seo_keywords(self):
        return self.meta_keywords

    def fetch_seo_image(self):
        if self.image:
            return settings.AWS_CLOUDFRONT_DOMAIN + self.image
        return ''
    
    def has_children(self):
        return self.children.exists()
    
    def get_active_children(self):
        return self.children.filter(active=True, date_deleted=None)
    
    class Meta:
        verbose_name = _('Page')

class Canvas(BaseModel, AdminModel):
    rows = models.ManyToManyField('canvasrow', blank=True)

    class Meta:
        verbose_name = _('Canvas')

class CanvasRow(SortableModel, BaseModel, AdminModel):
    block = models.ForeignKey('pageblock', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('Canvas row')
        ordering = ['-position']

class PageBlock(SeoModel, SortableModel, AdminModel, BaseModel):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)

    #Text blocks
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    image_second = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    url_text = models.CharField(max_length=255, null=True, blank=True)
    video = models.CharField(max_length=255, null=True, blank=True)
    embed = models.CharField(max_length=255, null=True, blank=True)
    block_elements = models.ManyToManyField('pageblockelement', blank=True)
    is_deletable = models.BooleanField(null=True, default=True)

    #Module blocks
    SORT_ORDER_ASC = 'asc'
    SORT_ORDER_DESC = 'desc'

    GET_SORT_ORDER = [
        (SORT_ORDER_ASC, _('Ascending')),
        (SORT_ORDER_DESC, _('Descending'))
    ]

    SORT_TYPE_DATE = 'date'
    SORT_TYPE_NAME = 'name'

    GET_SORT_TYPE = [
        (SORT_TYPE_DATE, _('Gesorteerd op datum')),
        (SORT_TYPE_NAME, _('Gesorteerd op naam'))
    ]
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True, blank=True)
    sort = models.CharField(max_length=255, choices=GET_SORT_TYPE , default=SORT_TYPE_DATE, blank=True, null=True)
    limit = models.IntegerField(default=0, blank=True, null=True)
    sort_order = models.CharField(max_length=255, choices=GET_SORT_ORDER, default=SORT_ORDER_ASC, blank=True, null=True)
    paginated = models.IntegerField(default=0, blank=True, null=True)
    detailpage = models.BooleanField(default=True, blank=True, null=True)   


    class Meta:
        verbose_name = _('Page block')

class PageBlockElement(BaseModel, SeoModel, SortableModel):
    block_element_title = models.CharField(max_length=255, null=True, blank=True)
    block_element_image = models.CharField(max_length=255, null=True, blank=True)
    block_element_content = models.TextField(null=True, blank=True)
    block_element_subtitle = models.CharField(max_length=255, null=True, blank=True)
    block_element_image_second = models.CharField(max_length=255, null=True, blank=True)
    block_element_url = models.CharField(max_length=255, null=True, blank=True)
    block_element_url_text = models.CharField(max_length=255, null=True, blank=True)

    def get_actives(self):
        return self.filter(date_deleted=None)

    class Meta:
        ordering = ['position']
  
class DetailPage(models.Model):
    object_id = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    default = models.BooleanField(default=False)
    canvas = models.ForeignKey(Canvas, on_delete=models.CASCADE)
    overridden = models.BooleanField(default=False)


class PageRevision(BaseRevision):
    current_instance = models.OneToOneField(Page, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, default="page")

class PageVersion(BaseVersion):
    revision = models.ForeignKey(PageRevision, on_delete=models.CASCADE, related_name='versions')

    def save(self, *args, **kwargs):
        try:
            pageversion = PageVersion.objects.get(id=self.id)
            for version in pageversion.revision.versions.all().exclude(id=self.id):
                if self.is_current:
                    version.is_current = False
                    version.save()
        except:
            for version in PageVersion.objects.exclude(id=self.id):
                version.is_current = False
                version.save()
        super().save(*args, **kwargs)
