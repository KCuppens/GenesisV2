from django.contrib.sitemaps import Sitemap
from apps.pages.models import Page

class PageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Page.objects.filter(date_deleted=None, active=True)

    def lastmod(self, obj):
        return obj.date_published