# accounts/views.py
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response  # IMPORTANTE: Importar Response
from rest_framework.permissions import AllowAny
from .models import CustomUser, BarberSchedule, Service, Reservation, Payment, UserCard
from .serializers import ServiceSerializer, ReservationSerializer, PaymentSerializer, UserCardSerializer
from .serializers import CustomUserSerializer, BarberScheduleSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from accounts.permissions import IsAdmin, IsBarberOrAdmin, UserPermissionsHelper
from rest_framework.decorators import action 


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
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        return UserPermissionsHelper.get_permissions(self)

    def perform_create(self, serializer):
        response = UserPermissionsHelper.perform_create(serializer, self.request)
        if response:  # Si hay error, devolverlo
            return response
        serializer.save()

    def perform_update(self, serializer):
        UserPermissionsHelper.perform_update(serializer, self.request, self.get_object())

    def get_queryset(self):
        return UserPermissionsHelper.get_filtered_queryset(self, super().get_queryset())
        serializer.save(role=role, is_active=True)

    def perform_update(self, serializer):
        """Restringe la edición de `is_active`, `role` y `salary` solo para admin."""
        user = self.get_object()

        if self.request.user.role != 0:  # No es Admin
            restricted_fields = ['is_active', 'role', 'salary']
            for field in restricted_fields:
                serializer.validated_data.pop(field, None)  # Eliminar si está presente

        serializer.save()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        
        if role is not None:
            queryset = queryset.filter(role=role)
            
        return queryset
    
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        """
        Permite acceso de solo lectura a todos, pero restringe modificaciones
        solo a barberos y administradores.
        """
        if self.action in ['list', 'retrieve']:  # GET permitido para todos
            return [AllowAny()]
        return [IsBarberOrAdmin()]  # Restricción en POST, PUT, DELETE

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        service = self.get_object()
        adapter = ServicePaymentAdapter()
        method = request.data.get('method', 'cash')
        return Response(adapter.process_service_payment(service.id, method))

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 0:  # Admin
            return Reservation.objects.all()
        elif user.role == 1:  # Barbero
            return Reservation.objects.filter(id_barber=user.id)
        elif user.role == 2:  # Cliente
            return Reservation.objects.filter(id_client=user.id)
        return Reservation.objects.none()  # No devuelve nada si no es un usuario válido

    def perform_create(self, serializer):
        """Realiza la creación de la reserva, asignando cliente y barbero."""
        
        # Determinar el cliente: usa el usuario autenticado si está disponible
        if self.request.user.is_authenticated:
            client = self.request.user  # El cliente autenticado es el usuario actual
        else:
            # Asigna el cliente predeterminado (id=8) si no está autenticado
            client = CustomUser.objects.get(id=8)

        # Obtener el id del barbero desde la solicitud
        barber_id = self.request.data.get('id_barber')
        if barber_id:
            try:
                # Intentamos obtener el barbero por su id
                barber = CustomUser.objects.get(id=barber_id, role=1)  # Solo barberos (role=1)
            except CustomUser.DoesNotExist:
                # Si no encontramos al barbero, retornamos un error
                return Response({"detail": "El barbero no existe."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Si no se proporciona el id del barbero, retornamos un error
            return Response({"detail": "Se requiere el id del barbero."}, status=status.HTTP_400_BAD_REQUEST)

        # Ahora guardamos la reserva con los datos de cliente y barbero
        serializer.save(id_client=client, id_barber=barber)
        print(f"Guardando reserva con cliente: {client.id} y barbero: {barber.first_name} {barber.last_name}")
        
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()  # ✅ Agregar queryset
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        return Payment.objects.filter(reservation__id_client=1)
    
class UserCardViewSet(viewsets.ModelViewSet):
    queryset = UserCard.objects.all()  # ✅ Agregar queryset
    serializer_class = UserCardSerializer
    
    def get_queryset(self):
        return UserCard.objects.filter(user=1)
    