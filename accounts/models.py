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

    #Se crea un campo de nombre con un maximo de 255 caracteres
    name = models.CharField(max_length=255, blank=True, null=True)

    #Se crea el email único por usuario
    email = models.EmailField(unique=True)

    #Puntos de recompensa
    reward_points = models.PositiveIntegerField(default=0)

    #Salario (solo aplicable a Barbers, pero por simplicidad ponemos null)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'users' #La tabla en la BD se llame users

    def __str__(self):
        #Muestra el nombre de usuario y el rol
        return f"{self.username} ({self.get.role_display()})"