from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Permite acceso solo a los administradores.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 0  # 0 = Admin
    
from rest_framework.permissions import BasePermission

class CanEditOwnProfile(BasePermission):
    """
    Permite a los usuarios editar sus propios datos, excepto los campos restringidos.
    Solo los administradores pueden editar `is_active`, `role` y `salary`.
    """

    def has_object_permission(self, request, view, obj):
        # Solo los admins pueden editar `is_active`, `role` y `salary`
        if request.user.role == 0:  # 0 = Admin
            return True

        # Si no es admin, solo puede editar su propio perfil
        return obj == request.user

