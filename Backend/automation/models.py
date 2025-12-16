from django.db import models
from infrastructure.models import Tenant
from django.conf import settings

class Workflow(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='workflows')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Node(models.Model):
    NODE_TYPES = [
        ('trigger', 'Trigger'),
        ('action', 'Action'),
        ('condition', 'Condition'),
        ('delay', 'Delay'),
    ]
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='nodes')
    node_type = models.CharField(max_length=50, choices=NODE_TYPES)
    config_json = models.JSONField(default=dict) # Parámetros, ej: { "action_type": "send_email", "subject": "..." }
    # Posición en el frontend para la visualización
    position_x = models.FloatField(default=0)
    position_y = models.FloatField(default=0)

    def __str__(self):
        return f"{self.get_node_type_display()} Node ({self.id}) for Workflow {self.workflow.id}"

class Edge(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='edges')
    source_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    target_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')
    # Para nodos de condición, ej: 'true_path', 'false_path'
    condition_path = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Edge from {self.source_node.id} to {self.target_node.id}"

class ExecutionInstance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='executions')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    trigger_context = models.JSONField(default=dict) # Datos que iniciaron el workflow, ej: el lead creado
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Execution {self.id} of {self.workflow.name} - {self.status}"

class ExecutionLog(models.Model):
    instance = models.ForeignKey(ExecutionInstance, on_delete=models.CASCADE, related_name='logs')
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)
    log_message = models.TextField()
    executed_at = models.DateTimeField(auto_now_add=True)
    # Datos de entrada y salida del nodo para debug
    input_data = models.JSONField(default=dict)
    output_data = models.JSONField(default=dict)
    is_error = models.BooleanField(default=False)

    def __str__(self):
        return f"Log for Instance {self.instance.id} at Node {self.node.id if self.node else 'N/A'}"
