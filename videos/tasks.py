import subprocess
from .models import Video
from django.conf import settings
import os

def generate_resolutions(video_id):
    try:
        video = Video.objects.get(id=video_id)
        input_path = video.video_file.path  # Lokaler Pfad zum Originalvideo

        # Definiere die Auflösungen
        resolutions = {
            '360p': '640x360',
            '480p': '854x480',
            '720p': '1280x720',
        }

        for label, size in resolutions.items():
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_{label}.mp4"

            # ffmpeg-Befehl ausführen (Video skalieren, Audio kopieren)
            subprocess.run([
                'ffmpeg', '-i', input_path, '-vf', f'scale={size}', '-c:a', 'copy', output_path
            ], check=True)

            # TODO: Speichere output_path in einem neuen FileField im Video-Modell
            # Oder lade Datei in Cloud hoch, wenn du GCS o.Ä. nutzt.

        print(f"Video {video_id} erfolgreich in mehrere Auflösungen umgewandelt.")

    except Exception as e:
        print(f"Fehler beim Generieren der Auflösungen für Video {video_id}: {e}")
