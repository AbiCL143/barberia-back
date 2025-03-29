from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BarberScheduleViewSet
from . import views
from accounts.views import PasswordRecoveryCodeView, ValidateRecoveryCodeView
from django.contrib.auth.views import LogoutView

# Registrar rutas del ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'barber-schedules', BarberScheduleViewSet, basename='barberschedule')



urlpatterns = [
    path('', views.home),  # Incluye las rutas del ViewSet
    path('logout', views.logout_view),  # Usar la vista personalizada
    path('', include(router.urls)),  # Rutas del ViewSet
    path('recovery-code/', PasswordRecoveryCodeView.as_view(), name='password-recovery-code'),
    path('validate-recovery-code/', ValidateRecoveryCodeView.as_view(), name='validate-recovery-code'),
]
