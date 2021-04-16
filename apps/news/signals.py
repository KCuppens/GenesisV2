from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.news.models import Article
from apps.pages.models import DetailPage, Canvas

@receiver(post_save, sender=Article)
def create_detailpage(sender, instance, created, **kwargs):
    """Create a detailpage for every article object"""
    if created:
        model_name = instance.__class__.__name__
        if not DetailPage.objects.filter(model=model_name, object_id__isnull=True, default=True).first():
            canvas_obj = Canvas.objects.create()
            DetailPage.objects.create(model=model_name, default=True, canvas=canvas_obj)
        
        if not DetailPage.objects.filter(model=model_name, object_id=instance.id, default=False).first():
            canvas_obj = Canvas.objects.create()
            DetailPage.objects.create(model=model_name, default=False, canvas=canvas_obj, object_id=instance.id) 






