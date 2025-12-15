# infrastructure/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Tenant(models.Model):
    """
    Representa un Tenant o una organización en el sistema.
    Cada Tenant aísla sus propios datos.
    """
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    """
    Define un rol dentro de un Tenant (ej. Admin, Editor, Viewer).
    """
    name = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='roles')
    # Aquí se podrían añadir permisos específicos si fuera necesario.

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"

class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende el de Django.
    Cada usuario debe pertenecer a un Tenant.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)

    # Sobrescribimos `groups` y `user_permissions` para evitar conflictos.
    # La gestión de permisos se hará a través de `Role`.
    groups = None
    user_permissions = None

    def save(self, *args, **kwargs):
        # Aseguramos que el username sea único globalmente, pero podríamos quererlo
        # único por tenant. Por simplicidad, lo mantenemos global.
        # El email también debería ser único.
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
