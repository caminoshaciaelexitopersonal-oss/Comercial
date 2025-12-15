# api/services/ai_manager/ai_manager.py
import os
from dotenv import load_dotenv
from .providers.gemini_provider import GeminiProvider
from .providers.ollama_provider import OllamaProvider

load_dotenv()

class AIManager:
    """
    Gestiona y proporciona acceso a los diferentes proveedores de IA.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIManager, cls).__new__(cls)
            cls._instance.providers = {}
            cls._instance._initialize_providers()
        return cls._instance

    def _initialize_providers(self):
        print("Initializing AI providers...")

        # Inicializar Gemini
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            try:
                self.providers["gemini"] = GeminiProvider(api_key=gemini_api_key)
                print("Gemini provider initialized.")
            except Exception as e:
                print(f"Failed to initialize Gemini provider: {e}")

        # Inicializar Ollama
        ollama_endpoint = os.getenv("OLLAMA_ENDPOINT")
        if ollama_endpoint:
            try:
                self.providers["ollama"] = OllamaProvider(endpoint=ollama_endpoint)
                print("Ollama provider initialized.")
            except Exception as e:
                print(f"Failed to initialize Ollama provider: {e}")

        if not self.providers:
            print("Warning: No AI providers were initialized. Check your .env file.")

    def get_provider(self, provider_name: str):
        provider = self.providers.get(provider_name)
        if not provider:
            raise ValueError(f"AI provider '{provider_name}' is not available or configured.")
        return provider

    def get_available_providers(self) -> list[str]:
        return list(self.providers.keys())

# Instancia singleton para ser usada en la aplicación
ai_manager = AIManager()
