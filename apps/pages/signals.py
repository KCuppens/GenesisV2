from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.pages.models import Canvas, Page, PageBlock, DetailPage

@receiver(post_save, sender=Page)
def create_canvas(sender, instance, created, **kwargs):
    """Create a canvas whenever a page object is created."""
    if created or not instance.canvas: 
        new_canvas = Canvas.objects.create()
        instance.canvas = new_canvas
        instance.save()

@receiver(post_save, sender=PageBlock)
def update_page_detail(sender, instance, created, **kwargs):
    """Update page to check if it has a block with detailpage"""
    
    if not created and instance.detailpage:
        page = instance.page
        module = instance.module
        if not module == 'Page':
            if not page.detailpage_models:
                page.detailpage_models = module
            elif page.detailpage_models and not module in page.detailpage_models:
                page.detailpage_models += ',' + module
            page.has_detailpage = True 
            page.save()

@receiver(post_save, sender=Canvas)
def update_detailpage_overridden(sender, instance, created, **kwargs):
    """Update detailpage with overridden based on canvas"""
    
    if not created:
        if instance.rows.count() > 0:
            detailpage = DetailPage.objects.filter(canvas=instance.id).first()
            if detailpage:
                detailpage.overridden = True 
                detailpage.save()
        else:
            detailpage = DetailPage.objects.filter(canvas=instance.id).first()
            if detailpage:
                detailpage.overridden = False 
                detailpage.save()


