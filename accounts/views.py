# accounts/views.py
from rest_framework import viewsets
from rest_framework.response import Response  # IMPORTANTE: Importar Response
from rest_framework.permissions import AllowAny
from .models import CustomUser, BarberSchedule
from .serializers import CustomUserSerializer, BarberScheduleSerializer
from django.shortcuts import render, redirect
from allauth.socialaccount.providers.google.views import OAuth2LoginView
from django.contrib.auth import logout
from accounts.permissions import IsAdmin, CanEditOwnProfile

#Eliminar cuando termine prueba
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('/') 

# Sección de vistas para los usuarios y horarios de los barberos
class BarberScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = BarberScheduleSerializer
    queryset = BarberSchedule.objects.all()  # Define la consulta base
    
    def get_permissions(self):
        """Definir permisos: Solo admin puede editar/agregar, todos pueden ver."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]  # Solo admin puede modificar
        return [AllowAny()]  # Cualquiera puede ver horarios

    def list(self, request, *args, **kwargs):
        barber_id = request.query_params.get('barber_id')

        if barber_id:
            schedules = BarberSchedule.objects.filter(id_barber=barber_id)
        else:
            schedules = BarberSchedule.objects.all()

        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)
    
class UserViewSet(viewsets.ModelViewSet):
    # Listar todos los usuarios
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        """Restringe la eliminación de usuarios solo al admin."""
        if self.action == 'destroy':  # Si es DELETE
            return [IsAdmin()]  # Solo admin puede eliminar usuarios
        if self.action in ['update', 'partial_update']:
            return [CanEditOwnProfile()]  # Los usuarios pueden editar su propio perfil
        return [AllowAny()]

    def perform_update(self, serializer):
        """Restringe la edición de `is_active`, `role` y `salary` solo para admin."""
        user = self.get_object()

        # Si NO es admin, eliminamos estos campos de la actualización
        if self.request.user.role != 0:  # No es Admin
            restricted_fields = ['is_active', 'role', 'salary']
            for field in restricted_fields:
                serializer.validated_data.pop(field, None)  # Eliminar si está presente

        serializer.save()
    
    # Filtrar por rol
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        
        if role is not None:
            queryset = queryset.filter(role=role)
            
        return queryset
