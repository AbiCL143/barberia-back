from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BarberSchedule

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('email','first_name', 'last_name', 'phone_number')}),
        ('Rol y permisos', {'fields': ('role', 'is_staff', 'is_superuser', 'is_active')}),
        ('Otros datos', {'fields': ('reward_points', 'salary')}),
    )

    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)  # Cambiamos username por email
    
@admin.register(BarberSchedule)
class BarberScheduleAdmin(admin.ModelAdmin):
    list_display = ('id_barber', 'days', 'start_time', 'end_time')  # Campos visibles en la lista
    list_filter = ('days',)  # Filtro en el panel de admin
    search_fields = ('id_barber__username',)  # Permite buscar por el nombre del barbero
    ordering = ('id_barber',)  # Ordenar por barbero
