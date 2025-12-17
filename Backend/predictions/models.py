from django.db import models
from sales.models import Opportunity

class LeadClosenessPrediction(models.Model):
    opportunity = models.OneToOneField(Opportunity, on_delete=models.CASCADE, related_name='prediction')
    confidence = models.FloatField() # Probabilidad de 0.0 a 1.0
    variables_considered = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.opportunity.name}: {self.confidence * 100:.1f}%"
