from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from infrastructure.models import Tenant

class Insight(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='insights')
    title = models.CharField(max_length=255) # Ej: "Caída de Conversión en Funnel X"
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES)
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic Foreign Key para apuntar a cualquier objeto
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title
