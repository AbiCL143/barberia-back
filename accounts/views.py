# accounts/views.py
import random
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response  # IMPORTANTE: Importar Response
from rest_framework.permissions import AllowAny
from .models import CustomUser, BarberSchedule
from .serializers import CustomUserSerializer, BarberScheduleSerializer
from django.shortcuts import render, redirect
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
    
class PasswordRecoveryCodeView(APIView):
    def post(self, request):
            email = request.data.get("email")
            
            # Validar si el usuario existe
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"detail": "Email no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # Generar el código aleatorio de 5 dígitos
            recovery_code = random.randint(10000, 99999)
            
            # Guardar el código de recuperación en el usuario (deberías tener un campo para esto, lo agregamos a continuación)
            user.password_recovery_code = recovery_code
            user.save()

            # Enviar el correo con el código
            send_mail(
                subject="Código de recuperación de contraseña",
                message=f"Tu código de recuperación es: {recovery_code}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({"detail": "Código enviado a tu correo."}, status=status.HTTP_200_OK)
        
class ValidateRecoveryCodeView(APIView):
        def post(self, request):
            email = request.data.get("email")
            code = request.data.get("code")
            
            # Validar si el usuario existe
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"detail": "Email no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # Validar si el código de recuperación es correcto
            if user.password_recovery_code == int(code):
                return Response({"detail": "Código correcto."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Código incorrecto."}, status=status.HTTP_400_BAD_REQUEST)
    