from storages.backends.gcloud import GoogleCloudStorage
from django.core.files import File
from .models import Video
import subprocess
import os

def generate_resolutions(video_id):
    """
    Generates multiple video resolutions for a given video.
    - Fetches the video by ID.
    - Uses ffmpeg to create 360p, 480p, 720p, and 1080p versions.
    - Uploads the generated files to Google Cloud Storage.
    - Speichert die Cloud-URLs im Video-Model.
    - Entfernt temporäre Dateien nach dem Upload.
    """
    try:
        video = Video.objects.get(id=video_id)
        input_path = video.video_file.path  # Lokaler Pfad

        resolutions = {
            '360p': '640x360',
            '480p': '854x480',
            '720p': '1280x720',
            '1080p': '1920x1080',
        }

        gcs_storage = GoogleCloudStorage()
        bucket_name = gcs_storage.bucket.name

        for label, size in resolutions.items():
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_{label}.mp4"
            cloud_path = f"videos/{label}/{os.path.basename(output_path)}"

            subprocess.run([
                'ffmpeg', '-i', input_path, '-vf', f'scale={size}', '-c:a', 'copy', output_path
            ], check=True)

            # Datei in Google Cloud Storage hochladen
            with open(output_path, 'rb') as f:
                gcs_storage.save(cloud_path, File(f))

            # Cloud-URL im Model speichern
            url = f"https://storage.googleapis.com/{bucket_name}/{cloud_path}"
            setattr(video, f"video_{label}", url)

            os.remove(output_path)

        video.save()
        print(f"Video {video_id} erfolgreich verarbeitet und URLs im Model gespeichert.")

    except Exception as e:
        print(f"Fehler beim Generieren der Auflösungen für Video {video_id}: {e}")
