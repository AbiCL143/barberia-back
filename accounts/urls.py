from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Crea un router y registra la vista del ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas del ViewSet
]
