from django.urls import path, include
from .views import UserRegistrationView, TokenValidationView

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/register', UserRegistrationView.as_view(), name="register"),
    path('auth/token/validate/', TokenValidationView.as_view(), name="register")
]