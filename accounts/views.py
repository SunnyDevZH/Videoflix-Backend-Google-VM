from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .serializers import RegisterSerializer

import random

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=201)
        return Response(serializer.errors, status=400)


# Hier Deine CustomTokenObtainPairView, CustomTokenRefreshView unverändert

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


# Neues PasswordResetCode Model brauchen wir noch (s.u.), aber hier die Views:

from .models import PasswordResetCode


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'E-Mail wird benötigt'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Sicherheitsgründe: Nicht verraten, ob Email existiert
            return Response({'message': 'Wenn die E-Mail existiert, wird ein Code versandt.'})

        # Code generieren
        code = f"{random.randint(100000, 999999)}"

        # Code speichern (alte Codes bleiben, prüfen wir beim Confirm)
        PasswordResetCode.objects.create(user=user, code=code)

        # Link zu deiner Frontend-Seite, auf der der Code eingegeben wird
        reset_link = "http://localhost:5173/forgot-password"

        # E-Mail senden mit Link und Code
        send_mail(
            subject='Passwort zurücksetzen – Dein Videoflix Team',
            message=(
                f"Hallo,\n\n"
                f"du hast eine Anfrage zum Zurücksetzen deines Passworts gestellt.\n"
                f"Dein Code lautet: {code}\n\n"
                f"Bitte gib den Code auf folgender Seite ein, um dein Passwort zurückzusetzen:\n"
                f"{reset_link}\n\n"
                f"Dieser Code ist 15 Minuten lang gültig.\n\n"
                f"Viele Grüße,\n"
                f"Dein Videoflix Team"
            ),
            from_email='noreply@deineapp.com',
            recipient_list=[email],
        )

        return Response({'message': 'Wenn die E-Mail existiert, wird ein Code versandt.'})



@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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

        # Ablaufzeit prüfen (15 Minuten)
        if timezone.now() > reset_code.created_at + timezone.timedelta(minutes=15):
            return Response({'error': 'Code ist abgelaufen'}, status=400)

        # Passwort setzen
        user.set_password(new_password)
        user.save()

        # Code als verwendet markieren
        reset_code.is_used = True
        reset_code.save()

        return Response({'message': 'Passwort wurde zurückgesetzt'}, status=200)
