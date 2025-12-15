// src/services/OllamaService.ts
import axios from 'axios';
import { aiConfig } from '../config/ai-config';

interface OllamaModel {
  name: string;
  modified_at: string;
  size: number;
}

interface OllamaPullStatus {
  status: string;
  digest: string;
  total: number;
  completed: number;
}

class OllamaService {
  private endpoint: string | undefined;
  private isConfigured: boolean;

  constructor() {
    const ollamaConf = aiConfig.ollama;
    this.isConfigured = ollamaConf.enabled && !!ollamaConf.endpoint;
    if (this.isConfigured) {
      this.endpoint = ollamaConf.endpoint;
    }
  }

  private ensureConfigured() {
    if (!this.isConfigured) {
      throw new Error('Ollama service is not configured. Please set OLLAMA_ENDPOINT in your .env file.');
    }
  }

  /**
   * Obtiene la lista de modelos que han sido descargados localmente en el servidor de Ollama.
   * @returns Una promesa que se resuelve con un array de modelos.
   */
  public async listLocalModels(): Promise<OllamaModel[]> {
    this.ensureConfigured();
    try {
      const response = await axios.get(`${this.endpoint}/api/tags`);
      return response.data.models;
    } catch (error) {
      console.error('Error fetching local models from Ollama:', error);
      throw new Error('Could not fetch local models from Ollama.');
    }
  }

  /**
   * Descarga un nuevo modelo desde el registro de Ollama.
   * Esta operación puede ser larga. No se espera a que termine.
   * @param modelName - El nombre del modelo a descargar (ej. 'llama3').
   * @returns Una promesa que se resuelve cuando la solicitud de descarga ha comenzado.
   */
  public async pullModel(modelName: string): Promise<{ status: string }> {
    this.ensureConfigured();
    try {
      // La API de pull responde con un stream de estados.
      // Para no bloquear la respuesta, hacemos la petición y devolve-mos un mensaje de inmediato.
      // En un sistema de producción, se podría implementar un sistema de notificación (WebSockets, etc.)
      // para informar al cliente del progreso en tiempo real.
      axios.post(`${this.endpoint}/api/pull`, {
        name: modelName,
        stream: false, // Usamos false para que espere a que termine
      }).then(response => {
        console.log(`Successfully pulled Ollama model: ${modelName}`, response.data);
      }).catch(err => {
        console.error(`Error pulling Ollama model '${modelName}':`, err);
      });

      return { status: `Model pull for '${modelName}' initiated.` };
    } catch (error) {
      console.error(`Error initiating model pull for '${modelName}':`, error);
      throw new Error(`Failed to initiate model pull for '${modelName}'.`);
    }
  }
}

export const ollamaService = new OllamaService();
