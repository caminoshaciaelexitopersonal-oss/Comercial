# infrastructure/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

# Sobrescribimos el modelo Tenant para añadir los nuevos campos
class Tenant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre de la Cadena")
    primary_color = models.CharField(max_length=7, default="#FFFFFF", verbose_name="Color Primario")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Mantenemos los modelos de usuario y rol para la autenticación
class Role(models.Model):
    name = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='roles')
    def __str__(self):
        return f"{self.name} ({self.tenant.name})"

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    groups = None
    user_permissions = None
    def __str__(self):
        return self.username

# --- Nuevos modelos para el Arquitecto de Embudos ---

class Categoria(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='categorias')
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.categoria.nombre} > {self.nombre}"

class LandingPage(models.Model):
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, related_name='landing_pages')
    slug = models.SlugField(unique=True)
    estado = models.CharField(max_length=10, choices=[('borrador', 'Borrador'), ('publicado', 'Publicado')], default='borrador')

    def __str__(self):
        return self.slug

class Embudo(models.Model):
    landing_page = models.OneToOneField(LandingPage, on_delete=models.CASCADE, related_name='embudo')
    nombre = models.CharField(max_length=255)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.nombre

class Pagina(models.Model):
    embudo = models.ForeignKey(Embudo, on_delete=models.CASCADE, related_name='paginas')
    tipo = models.CharField(max_length=50) # 'oferta', 'pago', 'gracias', etc.
    orden = models.PositiveIntegerField()
    history = HistoricalRecords()

    class Meta:
        ordering = ['orden']
    def __str__(self):
        return f"Página tipo {self.tipo} en {self.embudo.nombre}"

class Bloque(models.Model):
    pagina = models.ForeignKey(Pagina, on_delete=models.CASCADE, related_name='bloques')
    tipo = models.CharField(max_length=50) # 'hero', 'precios', 'faq', etc.
    orden = models.PositiveIntegerField()
    config_json = models.JSONField()
    history = HistoricalRecords()

    class Meta:
        ordering = ['orden']
    def __str__(self):
        return f"Bloque tipo {self.tipo} en página {self.pagina.id}"
