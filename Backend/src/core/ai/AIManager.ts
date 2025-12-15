// src/core/ai/AIManager.ts
import { IAiProvider } from './IAiProvider';
import { aiConfig } from '../../config/ai-config';

// Importa las clases concretas de los proveedores
import { GeminiProvider } from './providers/GeminiProvider';
// import { OpenAIProvider } from './providers/OpenAIProvider'; // Se añadirá después
import { OllamaProvider } from './providers/OllamaProvider';

/**
 * Gestiona y proporciona acceso a los diferentes proveedores de IA configurados en el sistema.
 */
class AIManager {
  private providers: Map<string, IAiProvider> = new Map();

  constructor() {
    this.initializeProviders();
  }

  /**
   * Carga e inicializa los proveedores de IA basados en el archivo de configuración.
   */
  private initializeProviders() {
    console.log('Initializing AI providers...');

    // Inicializar Gemini si está habilitado
    if (aiConfig.gemini.enabled && aiConfig.gemini.apiKey) {
      try {
        const geminiProvider = new GeminiProvider(aiConfig.gemini.apiKey);
        this.providers.set('gemini', geminiProvider);
        console.log('Gemini provider initialized successfully.');
      } catch (error) {
        console.error('Failed to initialize Gemini provider:', error);
      }
    }

    // Inicializar OpenAI si está habilitado (descomentar cuando se implemente)
    /*
    if (aiConfig.openai.enabled && aiConfig.openai.apiKey) {
      try {
        const openAIProvider = new OpenAIProvider(aiConfig.openai.apiKey);
        this.providers.set('openai', openAIProvider);
        console.log('OpenAI provider initialized successfully.');
      } catch (error) {
        console.error('Failed to initialize OpenAI provider:', error);
      }
    }
    */

    // Inicializar Ollama si está habilitado
    if (aiConfig.ollama.enabled && aiConfig.ollama.endpoint) {
      try {
        const ollamaProvider = new OllamaProvider(aiConfig.ollama.endpoint);
        this.providers.set('ollama', ollamaProvider);
        console.log('Ollama provider initialized successfully.');
      } catch (error) {
        console.error('Failed to initialize Ollama provider:', error);
      }
    }

    if (this.providers.size === 0) {
      console.warn('Warning: No AI providers were initialized. Check your .env file and configuration.');
    }
  }

  /**
   * Obtiene un proveedor de IA por su nombre.
   * @param providerName - El nombre del proveedor (ej. 'gemini', 'openai').
   * @returns La instancia del proveedor de IA.
   * @throws Si el proveedor no se encuentra o no está inicializado.
   */
  public getProvider(providerName: string): IAiProvider {
    const provider = this.providers.get(providerName);
    if (!provider) {
      throw new Error(`AI provider "${providerName}" is not available or not configured.`);
    }
    return provider;
  }

  /**
   * Lista los nombres de todos los proveedores de IA que se han inicializado correctamente.
   * @returns Un array de strings con los nombres de los proveedores disponibles.
   */
  public getAvailableProviders(): string[] {
    return Array.from(this.providers.keys());
  }
}

// Exportamos una instancia singleton del AIManager para que sea usada en toda la aplicación.
export const aiManager = new AIManager();
