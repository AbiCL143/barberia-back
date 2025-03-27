from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from . import views
from django.contrib.auth.views import LogoutView

# Crea un router y registra la vista del ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas del ViewSet
    path('google-login/', views.google_login, name='google-login'), #Eliminar cuando termine prueba
    path('dashboard/', views.dashboard, name='dashboard'),
    #path('logout/', views.logout_view, name='logout'),  # Usar la vista personalizada
]
