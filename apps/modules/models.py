from django.db import models
from apps.base.models import BaseModel, AdminModel, SortableModel, BaseRevision, BaseVersion
from django_extensions.db.fields import AutoSlugField
from apps.feathericons.models import Icon
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Module(BaseModel, AdminModel, SortableModel):
    urlpicker = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
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
        ordering = ['position']

class ModulePage(BaseModel, AdminModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    route = models.CharField(max_length=255, null=True, blank=True)
    show_nav = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Modulepage')


class Tab(BaseModel, AdminModel, SortableModel):
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


class ModuleRevision(BaseRevision):
    current_instance = models.OneToOneField(Module, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, default="module")


class ModuleVersion(BaseVersion):
    revision = models.ForeignKey(ModuleRevision, on_delete=models.CASCADE, related_name="versions")

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        try:
            moduleversion = ModuleVersion.objects.get(id=self.id)
            for version in moduleversion.revision.versions.all().exclude(id=self.id):
                if self.is_current:
                    version.is_current = False
                    version.save()
        except:
            for version in ModuleVersion.objects.exclude(id=self.id):
                version.is_current = False
                version.save()
        super().save(*args, **kwargs)


class TabRevision(BaseRevision):
    current_instance = models.OneToOneField(Tab, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, default="tab")


class TabVersion(BaseVersion):
    revision = models.ForeignKey(TabRevision, on_delete=models.CASCADE, related_name="versions")

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        try:
            tabversion = TabVersion.objects.get(id=self.id)
            for version in tabversion.revision.versions.all().exclude(id=self.id):
                if self.is_current:
                    version.is_current = False
                    version.save()
        except:
            for version in TabVersion.objects.exclude(id=self.id):
                version.is_current = False
                version.save()
        super().save(*args, **kwargs)



