# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser, BarberSchedule, Service, Reservation, Payment, UserCard

# serializers.py
from datetime import datetime, time  
from .factories import ReservationFactory, CardFactory
from .flyweight import PaymentFlyweight, ServiceFlyweight
from django.contrib.auth import get_user_model  # Agrega esta línea al inicio del archivo
from .factories import ServiceFactory
from .adapters import ServicePaymentAdapter, CardValidationAdapter, PaymentProcessingAdapter, PaymentAdapter

# Sección de serializadores para los horarios de los barberos
class BarberScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberSchedule
        fields = '__all__' 
    def validate_id_barber(self, value):
        """Valida que el usuario asignado sea un barbero."""
        if value.role != 1:
            raise serializers.ValidationError("Solo los barberos pueden tener un horario.")
        return value

# Sección de serializadores para los usuarios
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'role', 'password',
            'first_name', 'last_name', 'is_active',
            'reward_points', 'salary', 'phone_number',
           
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},  # Oculta la contraseña en la respuesta
        }

    def create(self, validated_data):
        """
        Crear un usuario nuevo con contraseña hasheada.
        """
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)  # Hashea la contraseña
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Actualizar un usuario existente, manejando correctamente la contraseña.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hashea la contraseña
        instance.save()
        return instance

# Sección de serializadores para los servicios    
class ServiceSerializer(serializers.ModelSerializer):
    cached_details = serializers.SerializerMethodField() ## Campo para almacenar los detalles en caché
    _factory = ServiceFactory() ## Factory para crear servicios
    _payment_adapter = ServicePaymentAdapter() ## Adaptador para el pago de servicios

    class Meta:
        model = Service
        fields = ['id', 'category', 'name',  'description', 'time', 'price', 
                 'active_service', 'cached_details']
        read_only_fields = ['cached_details']

    def get_cached_details(self, obj):
        return ServiceFlyweight.get_service(obj.id) ## Método para obtener los detalles del servicio desde el flyweight

    def create(self, validated_data):
        return self._factory.create_service(validated_data)

# Sección de serializadores para las reservas
class ReservationSerializer(serializers.ModelSerializer):
    barber_name = serializers.CharField(source='id_barber.first_name', read_only=True)
    id_client = serializers.IntegerField(source='id_client.id', read_only=True)  # Añadido para mostrar el email del cliente OPCIONAL NO RECOMENDABLE

    _factory = ReservationFactory() # Factory para crear reservas
    _payment_adapter = PaymentAdapter() ## Adaptador para el pago de reservas

    class Meta:
        model = Reservation
        fields = ('id_barber', 'barber_name', 'id_service', 'date', 'status', 'pay', 'id', "id_client")
        read_only_fields = ('status', 'barber_name')

    def create(self, validated_data):
        """Usa el Factory para crear la reserva asignando automáticamente el cliente autenticado"""
        try:
            # Obtener el cliente autenticado desde el contexto del serializer
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                client = request.user  # El cliente autenticado es el usuario actual
            else:
                raise serializers.ValidationError({"error": "El usuario debe estar autenticado"})

            # Asignar el cliente autenticado al validated_data
            validated_data['id_client'] = client  # Usamos el cliente autenticado en lugar de un ID hardcodeado
            
            # Usar el factory para crear la reserva
            return self._factory.create_reservation(validated_data)
        
        except Exception as e:
            raise serializers.ValidationError({
                "error": "Error creando reservación",
                "details": str(e),
                "solution": "Asegúrate que el usuario esté autenticado"
            })

# Sección de serializadores para las tarjetas de usuario   
class UserCardSerializer(serializers.ModelSerializer):
    _validation_adapter = CardValidationAdapter() # Adaptador para validar tarjetas de usuario
    
    class Meta:
        model = UserCard
        fields = ['id', 'card_number', 'expiration_month', 'expiration_year', 'nickname', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        errors = self._validation_adapter.validate_expiration(
            data.get('expiration_month'),
            data.get('expiration_year')
        )
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        return CardFactory.create_card(validated_data)

class PaymentSerializer(serializers.ModelSerializer):
    _processing_adapter = PaymentProcessingAdapter() # Adaptador para procesar pagos
    _flyweight = PaymentFlyweight() # Flyweight para almacenar detalles de pagos
    
    reservation_id = serializers.IntegerField(source='reservation.id', read_only=True)
    service_name = serializers.CharField(source='reservation.id_service.name', read_only=True)
    cached_details = serializers.SerializerMethodField()
    
    # Campos write-only
    card_number = serializers.CharField(write_only=True, required=False)
    expiration_month = serializers.CharField(write_only=True, required=False)
    expiration_year = serializers.CharField(write_only=True, required=False)
    save_card = serializers.BooleanField(write_only=True, default=False)
    card_nickname = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'amount')

    def get_cached_details(self, obj):
        return self._flyweight.get_payment_data(obj.id)

    def create(self, validated_data):
        # Eliminar campos no relacionados al modelo
        validated_data.pop('save_card', None)
        validated_data.pop('card_number', None)
        validated_data.pop('expiration_month', None)
        validated_data.pop('expiration_year', None)
        validated_data.pop('card_nickname', None)
        
        return self._processing_adapter.process_payment(validated_data)
