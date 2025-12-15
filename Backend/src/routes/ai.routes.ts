// src/routes/ai.routes.ts
import { Router } from 'express';
import { aiManager } from '../core/ai/AIManager';

const router = Router();

/**
 * @route   GET /api/ai/providers
 * @desc    Obtener la lista de proveedores de IA disponibles
 * @access  Public
 */
router.get('/providers', (req, res) => {
  try {
    const providers = aiManager.getAvailableProviders();
    res.json(providers);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching AI providers.' });
  }
});

export default router;
