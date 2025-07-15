from django.core.files import File
from .models import Video
import subprocess
import os

def generate_resolutions(video_id):
    """
    Generates multiple video resolutions for a given video.
    - Fetches the video by ID.
    - Uses ffmpeg to create 360p, 480p, 720p, and 1080p versions.
    - Saves the generated files to the corresponding fields in the Video model.
    - Removes temporary files after saving.
    - Prints success or error messages for logging/debugging.
    """
    try:
        video = Video.objects.get(id=video_id)
        input_path = video.video_file.path  # Lokaler Pfad zum Originalvideo

        resolutions = {
            '360p': '640x360',
            '480p': '854x480',
            '720p': '1280x720',
            '1080p': '1920x1080',
        }

        for label, size in resolutions.items():
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_{label}.mp4"

            # FFMPEG: skaliert Video, Audio kopiert
            subprocess.run([
                'ffmpeg', '-i', input_path, '-vf', f'scale={size}', '-c:a', 'copy', output_path
            ], check=True)

            with open(output_path, 'rb') as f:
                django_file = File(f)
                if label == '360p':
                    video.video_360p.save(os.path.basename(output_path), django_file, save=False)
                elif label == '480p':
                    video.video_480p.save(os.path.basename(output_path), django_file, save=False)
                elif label == '720p':
                    video.video_720p.save(os.path.basename(output_path), django_file, save=False)
                elif label == '1080p':
                    video.video_1080p.save(os.path.basename(output_path), django_file, save=False)

            # Datei löschen nach Speicherung (optional)
            os.remove(output_path)

        video.save()

        print(f"Video {video_id} erfolgreich in mehrere Auflösungen umgewandelt.")

    except Exception as e:
        print(f"Fehler beim Generieren der Auflösungen für Video {video_id}: {e}")
