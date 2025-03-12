from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Dependiendo de lo que quieras exponer, puedes filtrar campos
        fields = (
            'id', 'username', 'email', 'role',
            'name', 'reward_points', 'salary',
        )
        read_only_fields = ('id',)
