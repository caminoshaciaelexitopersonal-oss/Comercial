// src/config/ai-config.ts
import dotenv from 'dotenv';

dotenv.config();

/**
 * Define la configuración para un único proveedor de IA.
 * Las propiedades opcionales aceptan explícitamente `undefined` para ser compatibles con `exactOptionalPropertyTypes`.
 */
interface AiProviderConfig {
  enabled: boolean;
  apiKey?: string | undefined;
  endpoint?: string | undefined;
}

/**
 * Define la estructura de la configuración completa para todos los proveedores de IA.
 * Las propiedades están definidas explícitamente para proporcionar type-safety.
 */
interface AiConfig {
  gemini: AiProviderConfig;
  openai: AiProviderConfig;
  ollama: AiProviderConfig;
}

/**
 * Configuración central para los proveedores de IA.
 * Lee las credenciales y configuraciones desde las variables de entorno (.env).
 */
export const aiConfig: AiConfig = {
  gemini: {
    enabled: !!process.env.GEMINI_API_KEY,
    apiKey: process.env.GEMINI_API_KEY,
  },
  openai: {
    enabled: !!process.env.OPENAI_API_KEY,
    apiKey: process.env.OPENAI_API_KEY,
  },
  ollama: {
    enabled: !!process.env.OLLAMA_ENDPOINT,
    endpoint: process.env.OLLAMA_ENDPOINT || 'http://localhost:11434',
  },
  // Se pueden añadir fácilmente otros proveedores aquí (ej. Amazon Bedrock)
  // bedrock: {
  //   enabled: !!process.env.AWS_ACCESS_KEY_ID && !!process.env.AWS_SECRET_ACCESS_KEY,
  //   apiKey: process.env.AWS_SECRET_ACCESS_KEY, // Y otras credenciales de AWS
  // }
};
