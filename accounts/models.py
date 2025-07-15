from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PasswordResetCode(models.Model):
    """
    Model for storing password reset codes.
    - Stores a 6-digit code for a user.
    - Tracks creation time and whether the code has been used.
    - Codes are valid for 15 minutes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    def is_expired(self):
        """
        Returns True if the code is expired (older than 15 minutes).
        """
        return timezone.now() > self.created_at + timezone.timedelta(minutes=15)


class ActivationCode(models.Model):
    """
    Model for storing account activation codes.
    - Stores a unique 64-character code for a user.
    - Tracks creation time and whether the code has been used.
    - Codes are valid for 24 hours.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Activation code for {self.user.email}"

    def is_expired(self):
        """
        Returns True if the activation code is expired (older than 24 hours).
        """
        return timezone.now() > self.created_at + timezone.timedelta(hours=24)
