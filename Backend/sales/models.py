# sales/models.py
from django.db import models
from django.utils import timezone
from infrastructure.models import Tenant, User

class Opportunity(models.Model):
    STAGE_CHOICES = [
        ('new', 'Nuevo'), ('contacted', 'Contactado'), ('proposal', 'Propuesta Enviada'),
        ('negotiation', 'En Negociación'), ('won', 'Ganada'), ('lost', 'Perdida'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='opportunities')
    lead = models.ForeignKey('funnels.Lead', on_delete=models.CASCADE, related_name='opportunities', null=True, blank=True)
    name = models.CharField(max_length=255)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='new')
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    priority = models.CharField(max_length=20, default='medium', choices=[('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta')])
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='opportunities')
    last_activity_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Ticket(models.Model):
    STATUS_CHOICES = [('new', 'Nuevo'), ('in-progress', 'En Progreso'), ('resolved', 'Resuelto')]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tickets')
    lead = models.ForeignKey('funnels.Lead', on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tickets')
    sla_deadline = models.DateTimeField(help_text="Fecha y hora límite para la resolución (SLA)")
    csat_score = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Ticket #{self.id}: {self.subject}"
