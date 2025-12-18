from django.db import models
from infrastructure.models import Tenant
from django.conf import settings

class Opportunity(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='opportunities')
    name = models.CharField(max_length=255)
    # Etapas del pipeline: New, Contacted, Proposal, Negotiation, Won, Lost
    stage = models.CharField(max_length=50, default='New')
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='opportunities')

    def __str__(self):
        return self.name

class StageHistory(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='stage_history')
    from_stage = models.CharField(max_length=50)
    to_stage = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.opportunity.name}: {self.from_stage} -> {self.to_stage}"
