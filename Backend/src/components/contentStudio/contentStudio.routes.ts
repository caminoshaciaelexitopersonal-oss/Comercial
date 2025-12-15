// src/components/contentStudio/contentStudio.routes.ts
import { Router, Request, Response } from 'express';
import { aiManager } from '../../core/ai/AIManager';
import { GenerateTextParams, GenerateImageParams } from '../../core/ai/IAiProvider';

const router = Router();

interface AiRequest<T> extends Request {
  body: {
    provider: string;
    params: T;
  };
}

/**
 * @route   POST /api/content-studio/generate-text
 * @desc    Genera texto usando un proveedor de IA específico.
 * @access  Public
 * @body    { "provider": "gemini" | "ollama", "params": { "prompt": "...", "model": "..." } }
 */
router.post('/generate-text', async (req: AiRequest<GenerateTextParams>, res: Response) => {
  const { provider, params } = req.body;

  if (!provider || !params || !params.prompt || !params.model) {
    return res.status(400).json({ message: 'Provider, prompt, and model are required.' });
  }

  try {
    const aiProvider = aiManager.getProvider(provider);
    const result = await aiProvider.generateText(params);
    res.json({ result });
  } catch (error: any) {
    console.error(`Error generating text with ${provider}:`, error);
    res.status(500).json({ message: error.message || 'Failed to generate text.' });
  }
});

/**
 * @route   POST /api/content-studio/generate-image
 * @desc    Genera una imagen usando un proveedor de IA específico.
 * @access  Public
 * @body    { "provider": "gemini", "params": { "prompt": "...", "model": "..." } }
 */
router.post('/generate-image', async (req: AiRequest<GenerateImageParams>, res: Response) => {
  const { provider, params } = req.body;

  if (!provider || !params || !params.prompt || !params.model) {
    return res.status(400).json({ message: 'Provider, prompt, and model are required.' });
  }

  try {
    const aiProvider = aiManager.getProvider(provider);
    const result = await aiProvider.generateImage(params);
    if (result) {
      res.json({ imageUrl: result });
    } else {
      res.status(500).json({ message: 'Failed to generate image, no result was returned.' });
    }
  } catch (error: any) {
    console.error(`Error generating image with ${provider}:`, error);
    res.status(500).json({ message: error.message || 'Failed to generate image.' });
  }
});

export default router;
