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


class Customer(models.Model):
    """
    Representa un cliente o lead en el CRM.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='customers')
    email = models.EmailField()
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Campaign(models.Model):
    """
    Una campaña de marketing.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    goal = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Funnel(models.Model):
    """
    Un embudo de marketing dentro de una campaña.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='funnels')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='funnels')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FunnelPage(models.Model):
    """
    Una página dentro de un embudo (ej. Landing, Oferta, Gracias).
    """
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=255)
    content_json = models.JSONField(default=dict) # Para almacenar la estructura de la página
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Asset(models.Model):
    """
    Un activo digital (imagen, video, texto) generado por la IA.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video')])
    content = models.TextField() # URL, base64 o texto
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset_type} Asset ({self.id})"


class AIInteraction(models.Model):
    """
    Registra cada interacción con el módulo de IA.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='ai_interactions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ai_interactions')
    provider = models.CharField(max_length=100)
    prompt = models.TextField()
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction by {self.user.username} with {self.provider} at {self.created_at}"
