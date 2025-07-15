from google.cloud import storage
from datetime import timedelta
from django.conf import settings

def generate_signed_url(blob_name, expiration_minutes=15):
    """
    Generates a signed URL for accessing a file in Google Cloud Storage.
    - blob_name: The name of the file (blob) in the bucket.
    - expiration_minutes: How long the signed URL should be valid (default: 15 minutes).
    Returns a signed URL string that allows temporary access to the file.
    """
    storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
    )

    return url