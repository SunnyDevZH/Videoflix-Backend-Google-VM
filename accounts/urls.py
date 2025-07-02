from django.urls import path
from .views import RegisterView, ActivateAccountView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Registrierung
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (JWT)
    path('activate/<str:activation_code>/', ActivateAccountView.as_view(), name='activate_account'),  # Aktivierung
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token erneuern

    
]