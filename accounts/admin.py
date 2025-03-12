# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Personaliza la visualización en el admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('name', 'email')}),
        ('Rol y permisos', {'fields': ('role', 'is_staff', 'is_superuser')}),
        ('Otros datos', {'fields': ('reward_points', 'salary')}),
    )

    list_display = ('username', 'email', 'role', 'is_staff')
    search_fields = ('username', 'email', 'name')
