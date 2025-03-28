from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Barber'),
        (2, 'Client'),
    )
        
    #Se crea un campo de rol con las opciones de ROLE_CHOICES
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)
    
    #Se crea un campo de activo
    is_active = models.BooleanField(default=True)


    #Puntos de recompensa
    reward_points = models.PositiveIntegerField(default=0)
    
    #Número de teléfono
    phone_number = models.CharField(max_length=10, default="0000000000", blank=False, null=False)

    #Salario (solo aplicable a Barbers, pero por simplicidad ponemos null)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    
    REQUIRED_FIELDS = []  # Si quieres agregar más campos requeridos para superusuarios, agréguelos aquí

    class Meta:
        db_table = 'users' #La tabla en la BD se llame users

    def __str__(self):
        #Muestra el nombre de usuario y el rol
        return f"{self.username} ({self.get_role_display()})"
