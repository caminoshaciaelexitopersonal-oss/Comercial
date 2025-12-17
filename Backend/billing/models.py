from django.db import models
from infrastructure.models import Tenant

class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True) # Ej: Free, Pro, Business
    # Límites
    limit_funnels = models.PositiveIntegerField(default=1)
    limit_leads = models.PositiveIntegerField(default=100)
    limit_ai_tokens = models.PositiveIntegerField(default=50000)
    limit_automations = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT) # Evitar borrar un plan si hay suscriptores
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.name}'s Subscription to {self.plan.name}"

class UsageRecord(models.Model):
    RESOURCES = [
        ('funnels', 'Funnels'),
        ('leads', 'Leads'),
        ('ai_tokens', 'AI Tokens'),
        ('automations', 'Automations'),
    ]
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='usage_records')
    resource_type = models.CharField(max_length=50, choices=RESOURCES)
    usage = models.PositiveIntegerField(default=0)
    cycle_start_date = models.DateField()
    cycle_end_date = models.DateField()

    class Meta:
        unique_together = ('subscription', 'resource_type', 'cycle_start_date')

    def __str__(self):
        return f"Usage of {self.resource_type} for {self.subscription.tenant.name}"

class Invoice(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.subscription.tenant.name}"
