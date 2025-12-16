import uuid
from django.db import models
from infrastructure.models import Tenant

class Funnel(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='funnels')
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FunnelVersion(models.Model):
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    schema_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False) # Solo una versión puede estar activa para publicación

    class Meta:
        unique_together = ('funnel', 'version_number')
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.funnel.name} - v{self.version_number}"

class FunnelPage(models.Model):
    funnel_version = models.ForeignKey(FunnelVersion, on_delete=models.CASCADE, related_name='pages')
    page_type = models.CharField(max_length=100) # ej. landing, checkout, thank_you
    page_schema_json = models.JSONField(default=dict)
    order_index = models.PositiveIntegerField()

    class Meta:
        ordering = ['order_index']

    def __str__(self):
        return f"Page {self.order_index} ({self.page_type}) for {self.funnel_version}"

class FunnelPublication(models.Model):
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE, related_name='publications')
    version = models.ForeignKey(FunnelVersion, on_delete=models.CASCADE, related_name='publications')
    public_url_slug = models.SlugField(unique=True, default=uuid.uuid4)
    published_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Publication of {self.funnel.name} v{self.version.version_number} at /{self.public_url_slug}"

class LeadCapture(models.Model):
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE, related_name='leads')
    version = models.ForeignKey(FunnelVersion, on_delete=models.CASCADE, related_name='leads')
    page = models.ForeignKey(FunnelPage, on_delete=models.CASCADE, related_name='leads')
    form_data = models.JSONField(default=dict)
    captured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead captured in {self.funnel.name} at {self.captured_at}"

class FunnelEvent(models.Model):
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('submit', 'Form Submit'),
        ('conversion', 'Conversion'),
    ]
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE, related_name='events')
    version = models.ForeignKey(FunnelVersion, on_delete=models.CASCADE, related_name='events')
    experiment = models.ForeignKey('FunnelExperiment', on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    metadata_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event '{self.event_type}' on {self.funnel.name}"


class FunnelExperiment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('finished', 'Finished'),
    ]
    funnel = models.OneToOneField(Funnel, on_delete=models.CASCADE, related_name='experiment')
    version_a = models.ForeignKey(FunnelVersion, on_delete=models.CASCADE, related_name='experiments_as_a')
    version_b = models.ForeignKey(FunnelVersion, on_delete=models.CASCADE, related_name='experiments_as_b')
    traffic_split = models.PositiveIntegerField(default=50) # Porcentaje para la versión A
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A/B Test for {self.funnel.name}"
