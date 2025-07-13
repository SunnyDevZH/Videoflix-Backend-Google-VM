from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rq import get_queue

from .models import Video
from .tasks import generate_resolutions

@receiver(post_save, sender=Video)
def trigger_resolution_generation(sender, instance, created, **kwargs):
    # Nur auslösen, wenn ein neues Video erstellt wurde und originalvideo vorhanden
    if created and instance.video_file:
        queue = get_queue('default')
        queue.enqueue(generate_resolutions, instance.id)
        print(f"Enqueued generate_resolutions für Video {instance.id}")
