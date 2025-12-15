// src/core/ai/providers/OllamaProvider.ts
import axios from 'axios';
import { IAiProvider, GenerateTextParams, GenerateImageParams } from '../IAiProvider';

export class OllamaProvider implements IAiProvider {
  private endpoint: string;

  constructor(endpoint: string) {
    if (!endpoint) {
      throw new Error('Ollama endpoint is required.');
    }
    this.endpoint = endpoint;
  }

  async generateText(params: GenerateTextParams): Promise<string> {
    try {
      const response = await axios.post(`${this.endpoint}/api/generate`, {
        model: params.model,
        prompt: params.prompt,
        stream: false, // Desactivamos el streaming para obtener la respuesta completa
        options: {
          temperature: params.temperature,
          num_predict: params.maxTokens,
        },
      });
      return response.data.response;
    } catch (error) {
      console.error('Error generating text with Ollama:', error);
      throw new Error('Failed to generate text using Ollama.');
    }
  }

  async generateImage(params: GenerateImageParams): Promise<string | null> {
    // Ollama soporta modelos de imagen como 'llava' o el futuro 'moondream'.
    // Sin embargo, la generación directa de imágenes desde un prompt de texto (sin imagen de entrada)
    // es menos común que en APIs como DALL-E. Aquí asumimos que se está usando un modelo multimodal
    // que puede generar una representación textual o una imagen si el modelo lo soporta.
    // Para la mayoría de los casos, la generación de imágenes no es la función principal de los modelos estándar de Ollama.

    console.warn(`Image generation with Ollama provider is highly dependent on the model used.
                   Attempting to generate with model '${params.model}'. This may not be supported.`);

    // Esta es una implementación conceptual. El payload real podría necesitar ajustes.
    // Por ejemplo, algunos modelos pueden requerir un formato de prompt específico.
    try {
        // La API para imágenes podría ser diferente; esto es una suposición basada en /api/generate
        const response = await axios.post(`${this.endpoint}/api/generate`, {
            model: params.model, // ej. 'llava'
            prompt: `Generate an image of: ${params.prompt}`,
            stream: false,
        });

        // La respuesta de Ollama para imágenes puede ser un array de bytes o base64.
        // Aquí asumimos que si devuelve un array de enteros (bytes), lo convertimos a base64.
        if (Array.isArray(response.data.images) && response.data.images.length > 0) {
            const imageData = response.data.images[0];
            const base64Image = Buffer.from(imageData).toString('base64');
            return `data:image/jpeg;base64,${base64Image}`;
        }

        // Si no devuelve un campo 'images', no podemos procesarlo como imagen.
        console.error('Ollama model did not return image data.');
        return null;

    } catch (error) {
        console.error('Error generating image with Ollama:', error);
        throw new Error('Failed to generate image using Ollama. Ensure the model supports image generation.');
    }
  }
}
