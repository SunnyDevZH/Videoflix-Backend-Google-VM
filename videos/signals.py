from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Video
from .tasks import generate_resolutions

@receiver(post_save, sender=Video)
def trigger_resolution_generation(sender, instance, created, **kwargs):
    if created and instance.video_file:
        from django_rq import get_queue 
        queue = get_queue('default')
        queue.enqueue(generate_resolutions, instance.id)
        print(f"Enqueued generate_resolutions für Video {instance.id}")