// src/routes/ollama.routes.ts
import { Router, Request, Response } from 'express';
import { ollamaService } from '../services/OllamaService';

const router = Router();

/**
 * @route   GET /api/ollama/models
 * @desc    Obtiene la lista de modelos de Ollama descargados localmente.
 * @access  Public
 */
router.get('/models', async (req: Request, res: Response) => {
  try {
    const models = await ollamaService.listLocalModels();
    res.json(models);
  } catch (error: any) {
    console.error('Error fetching Ollama local models:', error);
    if (error.message.includes('not configured')) {
      return res.status(503).json({ message: error.message });
    }
    res.status(500).json({ message: error.message || 'Failed to fetch Ollama local models.' });
  }
});

/**
 * @route   POST /api/ollama/models/pull
 * @desc    Inicia la descarga de un nuevo modelo de Ollama.
 * @access  Public
 * @body    { "modelName": "llama3" }
 */
router.post('/models/pull', async (req: Request, res: Response) => {
  const { modelName } = req.body;

  if (!modelName) {
    return res.status(400).json({ message: 'modelName is required.' });
  }

  try {
    const result = await ollamaService.pullModel(modelName);
    res.status(202).json(result); // 202 Accepted, ya que la operación es asíncrona
  } catch (error: any) {
    console.error(`Error pulling Ollama model '${modelName}':`, error);
    if (error.message.includes('not configured')) {
      return res.status(503).json({ message: error.message });
    }
    res.status(500).json({ message: error.message || `Failed to pull Ollama model '${modelName}'.` });
  }
});

export default router;
