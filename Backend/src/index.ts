// src/index.ts
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import aiRoutes from './routes/ai.routes';
import contentStudioRoutes from './components/contentStudio/contentStudio.routes';
import ollamaRoutes from './routes/ollama.routes';

// Cargar variables de entorno
dotenv.config();

// Inicializar AIManager para que cargue los proveedores al iniciar.
import './core/ai/AIManager';

const app = express();
const PORT = process.env.PORT || 3001;

// Middlewares
app.use(cors()); // Habilita CORS para permitir peticiones desde el frontend
app.use(express.json()); // Parsea bodies de peticiones como JSON

// Rutas de la API
app.use('/api/ai', aiRoutes);
app.use('/api/content-studio', contentStudioRoutes);
app.use('/api/ollama', ollamaRoutes);

// Ruta de bienvenida
app.get('/', (req, res) => {
  res.send('Welcome to the AI-Powered Commercial Platform Backend!');
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
