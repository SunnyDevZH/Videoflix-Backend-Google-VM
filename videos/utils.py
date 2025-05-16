from google.cloud import storage
from datetime import timedelta
from django.conf import settings

def generate_signed_url(blob_name, expiration_minutes=15):
    storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
    )

    return url