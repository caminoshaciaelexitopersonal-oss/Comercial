from .models import Opportunity

class LeadScoringService:
    @staticmethod
    def calculate_score(opportunity: Opportunity) -> int:
        score = 0

        # Ejemplo de reglas simples
        if opportunity.value > 10000:
            score += 50

        # Aquí se añadiría lógica más compleja, como analizar eventos pasados
        # del lead, que no tenemos aún modelados.

        return score

    @staticmethod
    def assign_priority(score: int) -> str:
        if score > 80:
            return 'High'
        elif score > 49:
            return 'Medium'
        else:
            return 'Low'

    @classmethod
    def update_opportunity_score(cls, opportunity: Opportunity):
        new_score = cls.calculate_score(opportunity)
        new_priority = cls.assign_priority(new_score)

        opportunity.lead_score = new_score
        opportunity.priority = new_priority
        opportunity.save()

        # Podríamos emitir un evento 'lead.score.updated' aquí en el futuro
