# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'role', 'password',
            'first_name', 'last_name',
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
