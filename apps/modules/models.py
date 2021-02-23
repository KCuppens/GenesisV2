from django.db import models
from apps.base.models import BaseModel, AdminModel
from django_extensions.db.fields import AutoSlugField
from apps.feathericons.models import Icon
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Module(BaseModel, AdminModel):
    urlpicker = models.BooleanField(default=False)
    appname = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    route = models.CharField(max_length=255, null=True, blank=True)
    models = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        if self.name:
            return self.name
        return ''

    class Meta:
        verbose_name = _('Module')

class ModulePage(BaseModel, AdminModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    route = models.CharField(max_length=255, null=True, blank=True)
    show_nav = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Modulepage')


class Tab(BaseModel, AdminModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    icon = models.ForeignKey(Icon, on_delete=models.CASCADE, blank=True, null=True)
    modules = models.ManyToManyField(Module, blank=True)

    def get_active_modules(self):
        tabs = []
        for tab in self.modules.all():
            if tab.active and not tab.date_deleted:
                tabs.append(tab)
        return tabs

    class Meta:
        verbose_name = _('Tab')

