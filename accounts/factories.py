from .models import Reservation, Service, Payment, UserCard
from django.contrib.auth import get_user_model
from datetime import datetime

class ReservationFactory:
    @staticmethod
    def create_reservation(validated_data):
        """Crea una reserva ignorando autenticación"""
        reservation_data = validated_data.copy()

        return Reservation.objects.create(**reservation_data)

class ServiceFactory:
    @staticmethod
    def create_service(validated_data):
        """Crea servicios con activación automática"""
        service_data = validated_data.copy()
        service_data['active_service'] = True  # Activo por defecto
        return Service.objects.create(**service_data)

User = get_user_model()

class CardFactory:
    @staticmethod
    def create_card(validated_data):
        """Crea tarjeta asignando usuario ID=1 automáticamente"""
        user = User.objects.get(id=1)
        return UserCard.objects.create(user=user, **validated_data)

class PaymentFactory:
    @staticmethod
    def create_payment(validated_data, service_price):
        """Crea pago con lógica de negocio integrada"""
        payment_data = validated_data.copy()
        payment_data['amount'] = service_price
        return Payment.objects.create(**payment_data)