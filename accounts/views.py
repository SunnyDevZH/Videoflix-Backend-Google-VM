from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string#
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .serializers import RegisterSerializer
from .models import PasswordResetCode, ActivationCode

import random

User = get_user_model()

class RegisterView(APIView):
    """
    Allows a new user to register.
    - Creates an inactive user account.
    - Generates an activation code and sends a confirmation email with a link.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        """
        Handles user registration.
        Sends an activation email after successful registration.
        """
        email = request.data.get("email")
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Benutzer mit dieser E-Mail existiert bereits."},
                status=409
            )

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Account noch nicht aktiv
            user.save()

            # ActivationCode generieren und speichern
            code = get_random_string(64)
            ActivationCode.objects.create(user=user, code=code)

            activation_link = f"http://localhost:5173/videoflix/activate/{code}"
            username = user.email.split("@")[0]

            send_mail(
                subject="Bestätige deine Registrierung – Videoflix",
                message=(
                    f"Hallo {username}\n\n"
                    f"Nur noch ein kleiner Schritt: Bitte aktiviere deinen Account über den folgenden Link:\n\n"
                    f"{activation_link}\n\n"
                    f"Liebe Grüsse\n"
                    f"Dein Videoflix Team\n"
                    f"Yannick"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response({'message': 'Bitte bestätige deine E-Mail. Prüfe dein Postfach.'}, status=201)

        return Response(serializer.errors, status=400)


# Aktivierung der Registrierung (via ActivationCode)
class ActivateAccountView(APIView):
    """
    Activates a user account using a valid activation code.
    - Checks if the code is valid and not expired.
    - Sets the user as active and marks the code as used.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, activation_code):
        """
        Handles account activation via activation code.
        """
        try:
            activation = ActivationCode.objects.get(code=activation_code, is_used=False)
        except ActivationCode.DoesNotExist:
            return Response({'error': 'Ungültiger oder bereits verwendeter Aktivierungslink.'}, status=400)

        if activation.is_expired():
            return Response({'error': 'Aktivierungslink ist abgelaufen.'}, status=400)

        user = activation.user
        if user.is_active:
            return Response({'message': 'Dein Account ist bereits aktiviert.'}, status=200)

        # User aktivieren
        user.is_active = True
        user.save()

        # Aktivierungscode als verwendet markieren
        activation.is_used = True
        activation.save()

        return Response({'message': 'Dein Account wurde aktiviert. Du kannst dich jetzt einloggen.'}, status=200)


# Login (blockiert inaktive Accounts)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that blocks inactive accounts.
    - Returns an error if the account has not been activated yet.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles login and checks if the user account is active.
        """
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    raise AuthenticationFailed('Bitte bestätige zuerst deine E-Mail-Adresse.')
            except User.DoesNotExist:
                pass  # Fehler bei ungültigem Benutzer kommt sowieso von SimpleJWT

        return super().post(request, *args, **kwargs)


# Token Refresh bleibt unverändert
class CustomTokenRefreshView(TokenRefreshView):
    """
    Standard token refresh view from SimpleJWT.
    """
    permission_classes = [AllowAny]


# Passwort-Zurücksetzen: Code anfordern
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestAPIView(APIView):
    """
    Allows users to request a password reset code.
    - Sends a 6-digit code via email if the address exists.
    - The code is valid for 15 minutes.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles password reset code request.
        """
        email = request.data.get('email')
        if not email:
            return Response({'error': 'E-Mail wird benötigt'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Wenn die E-Mail existiert, wird ein Code versandt.'})

        code = f"{random.randint(100000, 999999)}"
        PasswordResetCode.objects.create(user=user, code=code)

        reset_link = "http://localhost:5173/videoflix/reset-password"
        username = user.email.split("@")[0]

        send_mail(
            subject='Passwort zurücksetzen – Videoflix',
            message=(
                f"Hallo {username}\n\n"
                f"du hast eine Anfrage zum Zurücksetzen deines Passworts gestellt.\n"
                f"Dein Code lautet: {code}\n\n"
                f"Bitte gib den Code auf folgender Seite ein:\n"
                f"{reset_link}\n\n"
                f"Dieser Code ist 15 Minuten lang gültig.\n\n"
                f"Viele Grüsse,\n"
                f"Dein Videoflix Team\n"
                f"Yannick"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({'message': 'Wenn die E-Mail existiert, wird ein Code versandt.'})


# Passwort-Zurücksetzen: Code bestätigen
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmAPIView(APIView):
    """
    Resets the password if a valid code and new password are provided.
    - Checks code, expiration, and sets the new password.
    - Marks the code as used.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles password reset confirmation and sets the new password.
        """
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')

        if not email or not code or not new_password:
            return Response({'error': 'E-Mail, Code und neues Passwort werden benötigt'}, status=400)

        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).latest('created_at')
        except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
            return Response({'error': 'Ungültiger Code oder Benutzer'}, status=400)

        if timezone.now() > reset_code.created_at + timezone.timedelta(minutes=15):
            return Response({'error': 'Code ist abgelaufen'}, status=400)

        user.set_password(new_password)
        user.save()

        reset_code.is_used = True
        reset_code.save()

        return Response({'message': 'Passwort wurde zurückgesetzt'}, status=200)
