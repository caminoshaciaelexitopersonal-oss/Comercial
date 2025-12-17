def get_user_permissions(user):
    if user.is_authenticated and hasattr(user, 'roles'):
        # El prefetch_related('roles') es importante para optimizar
        permissions = set()
        for role in user.roles.all():
            permissions.update(role.permissions)
        return permissions
    return set()

class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Calculamos los permisos directamente. Es más simple y robusto para los tests.
        # En un escenario de alta carga, se podría reintroducir el LazyObject con más cuidado.
        request.user.permissions = get_user_permissions(request.user)
        response = self.get_response(request)
        return response
