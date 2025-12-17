from sales.models import Opportunity
from ..models import LeadClosenessPrediction

class LeadPredictorService:
    @staticmethod
    def predict_closeness(opportunity: Opportunity):
        """
        Calcula la probabilidad de cierre de una oportunidad.
        Inicialmente, es un modelo heurístico simple basado en el score.
        """
        score = opportunity.lead_score

        # Heurística: cada punto de score aumenta la probabilidad. Normalizamos a 0-1.
        # Asumimos que un score de 100 es una probabilidad muy alta.
        confidence = min(score / 100.0, 1.0)

        variables = {
            'lead_score': score,
            'value': float(opportunity.value) # Asegurarse de que sea serializable a JSON
        }

        # Crear o actualizar la predicción
        prediction, created = LeadClosenessPrediction.objects.update_or_create(
            opportunity=opportunity,
            defaults={
                'confidence': confidence,
                'variables_considered': variables
            }
        )
        return prediction
