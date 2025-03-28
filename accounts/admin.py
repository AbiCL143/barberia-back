from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('email','first_name', 'last_name', 'phone_number')}),
        ('Rol y permisos', {'fields': ('role', 'is_staff', 'is_superuser', 'is_active')}),
        ('Otros datos', {'fields': ('reward_points', 'salary')}),
    )

    list_display = ('username','email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    #ordering = ('email',)  # Cambiamos username por email
