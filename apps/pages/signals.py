from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.pages.models import Canvas, Page

@receiver(post_save, sender=Page)
def create_canvas(sender, instance, created, **kwargs):
    """Create a canvas whenever a page object is created."""
    print('x')
    if created or not instance.canvas: 
        print('xx')
        new_canvas = Canvas.objects.create()
        instance.canvas = new_canvas
        instance.save()


