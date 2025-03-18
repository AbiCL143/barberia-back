# accounts/views.py
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    # Listar todos los usuarios
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    # Filtrar por rol
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        
        if role is not None:
            queryset = queryset.filter(role=role)
            
        return queryset
