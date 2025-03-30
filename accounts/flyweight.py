from django.contrib.auth import get_user_model
from .models import Service

User = get_user_model()

class BarberFlyweight:
    _cache = {}
    
    @classmethod
    def get_barber(cls, barber_id):
        if barber_id not in cls._cache:
            try:
                barber = User.objects.get(id=barber_id)
                cls._cache[barber_id] = {
                    'name': barber.username,
                    'specialties': list(barber.services_offered.all().values_list('name', flat=True))
                }
            except User.DoesNotExist:
                return None
        return cls._cache[barber_id]
    
class ServiceFlyweight:
    _cache = {}
    
    @classmethod
    def get_service(cls, service_id):
        if service_id not in cls._cache:
            try:
                service = Service.objects.get(id=service_id)
                cls._cache[service_id] = {
                    'name': service.name,
                    'price': float(service.price),
                    'duration': service.time
                }
            except Service.DoesNotExist:
                return None
        return cls._cache[service_id]
    
class PaymentFlyweight:
    _cache = {}
    
    @classmethod
    def get_payment_data(cls, payment_id):
        """Cachea datos de pagos recurrentes"""
        if payment_id not in cls._cache:
            from .models import Payment
            payment = Payment.objects.get(id=payment_id)
            cls._cache[payment_id] = {
                'amount': float(payment.amount),
                'service': payment.reservation.id_service.name,
                'date': payment.created_at
            }
        return cls._cache[payment_id]