// src/core/ai/IAiProvider.ts

/**
 * Representa los parámetros comunes para una solicitud de generación de texto.
 */
export interface GenerateTextParams {
  prompt: string;
  model: string;
  temperature?: number;
  maxTokens?: number;
}

/**
 * Representa los parámetros para una solicitud de generación de imágenes.
 */
export interface GenerateImageParams {
  prompt: string;
  model: string;
  n?: number;
  size?: '256x256' | '512x512' | '1024x1024' | '1792x1024' | '1024x1792'; // Formatos de OpenAI DALL-E 3
  aspectRatio?: '1:1' | '16:9' | '9:16'; // Formatos de Gemini
}

/**
 * Define el contrato que todos los proveedores de IA deben seguir.
 * Esto permite intercambiar proveedores (Gemini, OpenAI, Ollama) sin cambiar el código que los utiliza.
 */
export interface IAiProvider {
  /**
   * Genera texto a partir de un prompt.
   * @param params - Los parámetros para la generación de texto.
   * @returns Una promesa que se resuelve con el texto generado.
   */
  generateText(params: GenerateTextParams): Promise<string>;

  /**
   * Genera una imagen a partir de un prompt.
   * @param params - Los parámetros para la generación de la imagen.
   * @returns Una promesa que se resuelve con la URL o el string base64 de la imagen generada.
   */
  generateImage(params: GenerateImageParams): Promise<string | null>;

  // Futuros métodos como generateVideo, analyzeText, etc. podrían añadirse aquí.
}
