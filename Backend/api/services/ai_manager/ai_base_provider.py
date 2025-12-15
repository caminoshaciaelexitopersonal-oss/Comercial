# api/services/ai_manager/ai_base_provider.py
from abc import ABC, abstractmethod
from typing import Optional, Literal

class AIBaseProvider(ABC):
    """
    Clase base abstracta que define la interfaz para cualquier proveedor de IA.
    """

    @abstractmethod
    def generate_text(self, prompt: str, model: str, **kwargs) -> str:
        """
        Genera texto a partir de un prompt.
        """
        pass

    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        model: str,
        size: Optional[Literal['256x256', '512x512', '1024x1024']] = None,
        **kwargs
    ) -> Optional[str]:
        """
        Genera una imagen a partir de un prompt.
        Devuelve la URL o datos en base64 de la imagen.
        """
        pass
