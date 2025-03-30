class PaymentAdapter:
    def process_payment(self, method, amount):
        if method == 'card':
            return self._process_credit_card(amount)
        elif method == 'cash':
            return {'status': 'success', 'method': 'cash'}
    
    def _process_credit_card(self, amount):
        """Lógica adaptada para procesamiento de tarjeta"""
        return {'status': 'success', 'method': 'card'}
    
class ServicePaymentAdapter:
    def process_service_payment(self, service_id, method):
        from .flyweight import ServiceFlyweight
        service_data = ServiceFlyweight.get_service(service_id)
        
        if not service_data:
            return {'status': 'error', 'message': 'Servicio no encontrado'}
            
        if method == 'cash':
            return {
                'status': 'success',
                'method': 'cash',
                'service': service_data['name'],
                'amount': service_data['price']
            }
        elif method == 'card':
            return self._process_card_payment(service_data)
    
    def _process_card_payment(self, service_data):
        return {
            'status': 'success',
            'method': 'card',
            'service': service_data['name'],
            'amount': service_data['price'],
            'fee': service_data['price'] * 0.02  # 2% de comisión
        }
from datetime import datetime

class CardValidationAdapter:
    @staticmethod
    def validate_expiration(month, year):
        """Adapta validaciones de tarjeta a formato reusable"""
        errors = {}
        
        if not 1 <= int(month) <= 12:
            errors['expiration_month'] = "El mes debe estar entre 1 y 12."
        
        current_year = datetime.now().year
        if int(year) < current_year:
            errors['expiration_year'] = "El año no puede ser menor al actual."
        
        return errors

class PaymentProcessingAdapter:
    def process_payment(self, payment_data):
        """Adaptador para procesamiento de pagos"""
        from .factories import PaymentFactory
        
        # Lógica de procesamiento
        if payment_data.get('save_card'):
            self._save_card(payment_data)
        
        return PaymentFactory.create_payment(
            payment_data,
            payment_data['reservation'].id_service.price
        )
    
    def _save_card(self, data):
        """Lógica para guardar tarjeta"""
        from .factories import CardFactory
        card_data = {
            'card_number': data['card_number'],
            'expiration_month': data['expiration_month'],
            'expiration_year': data['expiration_year'],
            'nickname': data.get('card_nickname', '')
        }
        CardFactory.create_card(card_data)