from rest_framework.permissions import BasePermission

class HasPermission(BasePermission):
    """
    Permiso de DRF para verificar si un usuario tiene los permisos requeridos por una vista.

    Uso en un ViewSet:
    permission_classes = [IsAuthenticated, HasPermission]
    required_permissions = ['funnels:create'] # Para todo el ViewSet

    O dentro de un método de acción:
    @action(detail=True, methods=['post'], permission_classes=[HasPermission], required_permissions=['funnels:publish'])
    def publish(...):
        ...
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        user_permissions = getattr(user, 'permissions', set())

        # La vista debe implementar get_required_permissions(action)
        if not hasattr(view, 'get_required_permissions'):
            return False # Denegar si la vista no está configurada para RBAC

        required_permissions = view.get_required_permissions(view.action)

        return all(perm in user_permissions for perm in required_permissions)

    def has_object_permission(self, request, view, obj):
        # La lógica de permisos a nivel de objeto puede ser más compleja y
        # por ahora, delegamos en el permiso a nivel de vista.
        return self.has_permission(request, view)
