# accounts/views.py
from rest_framework import viewsets
from rest_framework.response import Response  # IMPORTANTE: Importar Response
from .models import CustomUser, BarberSchedule
from .serializers import CustomUserSerializer, BarberScheduleSerializer
from django.shortcuts import render, redirect
from allauth.socialaccount.providers.google.views import OAuth2LoginView
from django.contrib.auth import logout

#Eliminar cuando termine prueba
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('/') 


class BarberScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = BarberScheduleSerializer
    queryset = BarberSchedule.objects.all()  # Define la consulta base

    def list(self, request, *args, **kwargs):
        """
        Si se pasa 'barber_id' en la URL como parámetro de consulta, filtra por ese barbero.
        Ejemplo: /barber-schedules/?barber_id=3
        """
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
    
    # Filtrar por rol
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        
        if role is not None:
            queryset = queryset.filter(role=role)
            
        return queryset
