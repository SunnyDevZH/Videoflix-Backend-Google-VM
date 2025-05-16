import os
from django.core.management.base import BaseCommand
from google.cloud import storage
from django.conf import settings
from videos.models import Video

class Command(BaseCommand):
    help = 'Synchronize videos from Google Cloud Storage bucket to the Django DB'

    def handle(self, *args, **kwargs):
        # Google Cloud Storage Client mit Credentials laden
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(settings.BASE_DIR, 'core/credentials/service-account-key.json')
        client = storage.Client()

        bucket_name = settings.GS_BUCKET_NAME
        bucket = client.get_bucket(bucket_name)

        blobs = bucket.list_blobs()
        count_new = 0
        count_existing = 0

        for blob in blobs:
            video_path = f"videos/{blob.name}" if not blob.name.startswith('videos/') else blob.name

            # Prüfen ob Video mit genau diesem Pfad schon in DB existiert
            if Video.objects.filter(video_file=video_path).exists():
                count_existing += 1
                continue

            # Neues Video-Objekt anlegen
            title = os.path.splitext(os.path.basename(blob.name))[0]
            video = Video.objects.create(title=title, video_file=video_path)
            count_new += 1
            self.stdout.write(f'Added video: {title}')

        self.stdout.write(self.style.SUCCESS(f'Synchronization complete. {count_new} new videos added, {count_existing} already existed.'))
