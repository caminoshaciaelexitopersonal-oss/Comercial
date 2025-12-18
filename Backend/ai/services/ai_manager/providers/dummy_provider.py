# ai/services/ai_manager/providers/dummy_provider.py
from .ai_base_provider import AIBaseProvider

class DummyProvider(AIBaseProvider):
    def __init__(self):
        super().__init__("Dummy", ["text"])

    def execute_text_generation(self, prompt: str, model: str) -> str:
        return "Esta es una respuesta de prueba desde el DummyProvider."
