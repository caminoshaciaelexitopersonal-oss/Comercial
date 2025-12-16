from django.db import models
from infrastructure.models import Tenant
from django.conf import settings

class Campaign(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # Estados posibles: draft, scheduled, sending, sent, failed
    status = models.CharField(max_length=50, default='draft')

    def __str__(self):
        return self.name

class CampaignChannel(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='channels')
    # Tipos de canal: email, sms, instagram, facebook
    channel_type = models.CharField(max_length=50)
    # Aquí iría la configuración específica del canal, ej. la cuenta a usar
    config_json = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.channel_type} for {self.campaign.name}"

class MessageVariant(models.Model):
    channel = models.ForeignKey(CampaignChannel, on_delete=models.CASCADE, related_name='variants')
    content = models.TextField()
    # Para A/B testing u otras variaciones
    variant_name = models.CharField(max_length=100, default='A')

    def __str__(self):
        return f"Variant {self.variant_name} for {self.channel}"

class SendLog(models.Model):
    variant = models.ForeignKey(MessageVariant, on_delete=models.CASCADE, related_name='logs')
    sent_at = models.DateTimeField(auto_now_add=True)
    recipient = models.CharField(max_length=255) # ej. email, phone number, user_id
    # Estados: pending, success, failed
    status = models.CharField(max_length=50, default='pending')
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Log for {self.variant} to {self.recipient} - {self.status}"
