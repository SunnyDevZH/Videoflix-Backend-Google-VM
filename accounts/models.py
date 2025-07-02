from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=15)


class ActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Activation code for {self.user.email}"

    def is_expired(self):
        # Optional: z.B. 24 Stunden gültig
        return timezone.now() > self.created_at + timezone.timedelta(hours=24)
