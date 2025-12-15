
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Chat, FunctionDeclaration, Type, LiveServerMessage, LiveSession } from '@google/genai';
import { createChat, sendMessageToChat, groundedSearch, groundedMapsSearch, connectLive } from '../services/geminiService';
import { LoadingSpinner, CalendarPlusIcon, BotIcon, MailIcon, MessageIcon, PlusIcon, WorkflowIcon } from './icons';
import type { ChatMessage, GroundingChunk } from '../types';
import { useSettings } from '../context/SettingsContext';


// --- Helper Functions for Live API ---
function decode(base64: string) {
    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
  }
  
async function decodeAudioData(
    data: Uint8Array,
    ctx: AudioContext,
    sampleRate: number,
    numChannels: number,
  ): Promise<AudioBuffer> {
    const dataInt16 = new Int16Array(data.buffer);
    const frameCount = dataInt16.length / numChannels;
    const buffer = ctx.createBuffer(numChannels, frameCount, sampleRate);
  
    for (let channel = 0; channel < numChannels; channel++) {
      const channelData = buffer.getChannelData(channel);
      for (let i = 0; i < frameCount; i++) {
        channelData[i] = dataInt16[i * numChannels + channel] / 32768.0;
      }
    }
    return buffer;
  }

function encode(bytes: Uint8Array) {
    let binary = '';
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

const Chatbot: React.FC = () => {
    // Note: This chatbot implementation maintains its own state and does not yet
    // use the hybrid llmService for chat streaming. For now, it defaults to Gemini's
    // chat implementation for simplicity. A future update could abstract this.
    const [chat, setChat] = useState<Chat | null>(null);
    const [history, setHistory] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [groundingChunks, setGroundingChunks] = useState<GroundingChunk[]>([]);
    const chatEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        setChat(createChat("Eres un asistente comercial útil y amigable."));
    }, []);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [history]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;
        const userMessage: ChatMessage = { role: 'user', parts: [{ text: input }] };
        setHistory(prev => [...prev, userMessage]);
        setIsLoading(true);
        setGroundingChunks([]);
        
        const currentInput = input;
        setInput('');

        try {
            let responseText = '';
            let chunks: GroundingChunk[] = [];
            
            if (currentInput.toLowerCase().includes('busca en la web') || currentInput.toLowerCase().includes('noticias')) {
                const result = await groundedSearch(currentInput);
                responseText = result.text;
                chunks = result.chunks;
            } else if (currentInput.toLowerCase().includes('cerca de mí') || currentInput.toLowerCase().includes('restaurantes')) {
                const result = await groundedMapsSearch(currentInput);
                responseText = result.text;
                chunks = result.chunks;
            } else if (chat) {
                const response = await sendMessageToChat(chat, currentInput);
                responseText = response.text;
            } else {
                responseText = "El chat no está inicializado.";
            }

            const modelMessage: ChatMessage = { role: 'model', parts: [{ text: responseText }] };
            setHistory(prev => [...prev, modelMessage]);
            setGroundingChunks(chunks);

        } catch (error: any) {
            const errorMessage: ChatMessage = { role: 'model', parts: [{ text: `Error: ${error.text || error.message}` }] };
            setHistory(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };
    
    return (
        <div className="bg-card p-6 rounded-lg shadow-lg flex flex-col h-full border">
            <h3 className="text-xl font-bold mb-4">Chat Inteligente (Gemini)</h3>
            <div className="flex-1 overflow-y-auto mb-4 pr-2 space-y-4">
                {history.map((msg, index) => (
                    <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xl p-3 rounded-lg ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'}`}>
                            <p className="whitespace-pre-wrap">{msg.parts[0].text}</p>
                        </div>
                    </div>
                ))}
                {isLoading && <div className="flex justify-start"><LoadingSpinner /></div>}
                <div ref={chatEndRef} />
            </div>
             {groundingChunks.length > 0 && (
                <div className="mb-4 p-2 border-t">
                    <p className="text-sm text-muted-foreground mb-2">Fuentes:</p>
                    <ul className="text-xs space-y-1">
                        {groundingChunks.map((chunk, i) => (
                            <li key={i}>
                                {chunk.web && <a href={chunk.web.uri} target="_blank" rel="noreferrer" className="text-primary hover:underline">{chunk.web.title}</a>}
                                {chunk.maps && <a href={chunk.maps.uri} target="_blank" rel="noreferrer" className="text-primary hover:underline">{chunk.maps.title}</a>}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            <div className="flex space-x-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Pregunta algo..."
                    className="flex-grow bg-input border rounded-md p-2"
                    disabled={isLoading}
                />
                <button onClick={handleSend} disabled={isLoading || !input.trim()} className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 disabled:opacity-50">
                    Enviar
                </button>
            </div>
        </div>
    );
};

const scheduleAppointmentTool: FunctionDeclaration = {
  name: 'scheduleAppointment',
  parameters: {
    type: Type.OBJECT,
    description: 'Agenda una cita o reunión en el calendario.',
    properties: {
      title: { type: Type.STRING, description: 'El título o motivo de la cita.' },
      date: { type: Type.STRING, description: 'La fecha de la cita, ej: "2024-08-15"' },
      time: { type: Type.STRING, description: 'La hora de la cita, ej: "15:30"' },
    },
    required: ['title', 'date', 'time'],
  },
};

const LiveAssistant: React.FC = () => {
    const { provider } = useSettings();
    const [isSessionActive, setIsSessionActive] = useState(false);
    const [status, setStatus] = useState('Listo para conectar');
    const [transcriptions, setTranscriptions] = useState<{source: 'user' | 'model' | 'tool', text: string}[]>([]);
    
    const sessionPromiseRef = useRef<Promise<LiveSession> | null>(null);
    const inputAudioContextRef = useRef<AudioContext | null>(null);
    const outputAudioContextRef = useRef<AudioContext | null>(null);
    const mediaStreamRef = useRef<MediaStream | null>(null);
    const scriptProcessorRef = useRef<ScriptProcessorNode | null>(null);

    const nextStartTimeRef = useRef(0);
    const audioSourcesRef = useRef(new Set<AudioBufferSourceNode>());
    
    const currentInputTranscriptionRef = useRef('');
    const currentOutputTranscriptionRef = useRef('');

    const onMessage = useCallback(async (message: LiveServerMessage) => {
        if (message.serverContent?.outputTranscription) {
            currentOutputTranscriptionRef.current += message.serverContent.outputTranscription.text;
        } else if (message.serverContent?.inputTranscription) {
            currentInputTranscriptionRef.current += message.serverContent.inputTranscription.text;
        }

        if(message.serverContent?.turnComplete){
            const fullInput = currentInputTranscriptionRef.current.trim();
            const fullOutput = currentOutputTranscriptionRef.current.trim();
            const newTurn = [];
            if(fullInput) newTurn.push({source: 'user', text: fullInput} as const);
            if(fullOutput) newTurn.push({source: 'model', text: fullOutput} as const);
            
            if(newTurn.length > 0) {
                setTranscriptions(prev => [...prev, ...newTurn]);
            }

            currentInputTranscriptionRef.current = '';
            currentOutputTranscriptionRef.current = '';
        }

        if (message.toolCall) {
            for (const fc of message.toolCall.functionCalls) {
                if (fc.name === 'scheduleAppointment') {
                    const { title, date, time } = fc.args;
                    const toolResponseText = `Cita agendada: "${title}" el ${date} a las ${time}.`;
                    setTranscriptions(prev => [...prev, {source: 'tool', text: toolResponseText}]);

                    if (sessionPromiseRef.current) {
                        sessionPromiseRef.current.then(session => {
                            session.sendToolResponse({
                                functionResponses: {
                                    id: fc.id,
                                    name: fc.name,
                                    response: { result: "ok, la cita ha sido agendada con éxito" }
                                }
                            })
                        });
                    }
                }
            }
        }

        const base64Audio = message.serverContent?.modelTurn?.parts[0]?.inlineData.data;
        if(base64Audio && outputAudioContextRef.current) {
            nextStartTimeRef.current = Math.max(nextStartTimeRef.current, outputAudioContextRef.current.currentTime);
            const audioBuffer = await decodeAudioData(decode(base64Audio), outputAudioContextRef.current, 24000, 1);
            const source = outputAudioContextRef.current.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(outputAudioContextRef.current.destination);
            source.addEventListener('ended', () => audioSourcesRef.current.delete(source));
            source.start(nextStartTimeRef.current);
            nextStartTimeRef.current += audioBuffer.duration;
            audioSourcesRef.current.add(source);
        }

        if (message.serverContent?.interrupted) {
            for (const source of audioSourcesRef.current.values()) {
                source.stop();
                audioSourcesRef.current.delete(source);
            }
            nextStartTimeRef.current = 0;
        }
    }, []);

    const onError = (e: ErrorEvent) => {
        console.error("Live API Error:", e);
        setStatus(`Error: ${e.message}`);
        stopSession();
    };

    const onClose = (e: CloseEvent) => {
        console.log("Live API Closed:", e);
        setStatus('Conexión cerrada');
        stopSession();
    };

    const startSession = async () => {
        try {
            setStatus('Solicitando permiso del micrófono...');
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaStreamRef.current = stream;
            
            setStatus('Iniciando sesión...');
            inputAudioContextRef.current = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
            outputAudioContextRef.current = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 24000 });
            
            sessionPromiseRef.current = connectLive(onMessage, onError, onClose, [{functionDeclarations: [scheduleAppointmentTool]}]);
            
            const source = inputAudioContextRef.current.createMediaStreamSource(stream);
            const scriptProcessor = inputAudioContextRef.current.createScriptProcessor(4096, 1, 1);
            scriptProcessorRef.current = scriptProcessor;

            scriptProcessor.onaudioprocess = (audioEvent) => {
                const inputData = audioEvent.inputBuffer.getChannelData(0);
                const l = inputData.length;
                const int16 = new Int16Array(l);
                for (let i = 0; i < l; i++) int16[i] = inputData[i] * 32768;
                
                const pcmBlob = {
                    data: encode(new Uint8Array(int16.buffer)),
                    mimeType: 'audio/pcm;rate=16000',
                };

                if (sessionPromiseRef.current) {
                    sessionPromiseRef.current.then((session) => {
                        session.sendRealtimeInput({ media: pcmBlob });
                    });
                }
            };
            source.connect(scriptProcessor);
            scriptProcessor.connect(inputAudioContextRef.current.destination);

            setIsSessionActive(true);
            setStatus('Conectado. ¡Habla ahora!');
        } catch (err) {
            console.error(err);
            setStatus('Error al iniciar: No se pudo acceder al micrófono.');
        }
    };
    
    const stopSession = useCallback(() => {
        if (sessionPromiseRef.current) {
            sessionPromiseRef.current.then(session => session.close());
            sessionPromiseRef.current = null;
        }
        if (mediaStreamRef.current) {
            mediaStreamRef.current.getTracks().forEach(track => track.stop());
            mediaStreamRef.current = null;
        }
        if(scriptProcessorRef.current) {
            scriptProcessorRef.current.disconnect();
            scriptProcessorRef.current = null;
        }
        if (inputAudioContextRef.current) {
            inputAudioContextRef.current.close();
            inputAudioContextRef.current = null;
        }
        if (outputAudioContextRef.current) {
            outputAudioContextRef.current.close();
            outputAudioContextRef.current = null;
        }
        setIsSessionActive(false);
        setStatus('Listo para conectar');
    }, []);

    useEffect(() => {
        return () => stopSession();
    }, [stopSession]);

    if (provider === 'ollama') {
        return (
            <div className="bg-card p-6 rounded-lg shadow-lg flex flex-col h-full items-center justify-center text-center border">
                 <BotIcon className="w-16 h-16 text-muted-foreground mb-4" />
                <h2 className="text-2xl font-bold text-foreground mb-2">Funcionalidad No Disponible</h2>
                <p className="text-muted-foreground max-w-md">
                    El asistente de voz en tiempo real es una función avanzada que requiere la API 'Live' de Google Gemini.
                </p>
                <p className="text-muted-foreground max-w-md mt-2">
                    Por favor, cambie al proveedor 'Gemini' en la pantalla de <span className="font-bold text-primary">Ajustes</span> para utilizar este asistente.
                </p>
            </div>
        );
    }
    
    const renderTranscription = (item: {source: 'user' | 'model' | 'tool', text: string}, index: number) => {
        switch(item.source) {
            case 'user':
                return <div key={index} className="p-2 bg-primary/10 rounded-lg"><span className="font-bold text-primary">Tú:</span> {item.text}</div>;
            case 'model':
                return <div key={index} className="p-2 bg-muted/50 rounded-lg"><span className="font-bold text-teal-400">Asistente:</span> {item.text}</div>;
            case 'tool':
                return <div key={index} className="flex items-start space-x-2 p-2 my-2 bg-yellow-900/40 border border-yellow-500/30 rounded-lg text-yellow-300">
                    <CalendarPlusIcon className="w-5 h-5 mt-1 text-yellow-400 flex-shrink-0" />
                    <p className="text-sm whitespace-pre-wrap"><span className="font-bold">Acción Realizada:</span> {item.text}</p>
                </div>;
            default:
                return null;
        }
    };

    return (
        <div className="bg-card p-6 rounded-lg shadow-lg flex flex-col h-full border">
            <h3 className="text-xl font-bold mb-4">Asistente Virtual por Voz</h3>
            <div className="flex items-center justify-between mb-4">
                <button
                    onClick={isSessionActive ? stopSession : startSession}
                    className={`px-4 py-2 rounded-md text-white ${isSessionActive ? 'bg-destructive hover:bg-destructive/90' : 'bg-green-600 hover:bg-green-700'}`}
                >
                    {isSessionActive ? 'Desconectar' : 'Conectar'}
                </button>
                <div className="flex items-center space-x-2">
                    <span className={`w-3 h-3 rounded-full ${isSessionActive ? 'bg-green-400 animate-pulse' : 'bg-muted-foreground'}`}></span>
                    <p>{status}</p>
                </div>
            </div>
            <div className="flex-1 overflow-y-auto bg-background rounded p-4 space-y-2">
                 {transcriptions.length === 0 && <p className="text-muted-foreground text-center">La transcripción de la conversación aparecerá aquí.</p>}
                 {transcriptions.map(renderTranscription)}
            </div>
        </div>
    );
};

const MarketingWorkflows: React.FC = () => {

    const Node: React.FC<{ icon: React.FC<{className?: string}>, title: string, description: string, color: string, children?: React.ReactNode }> = ({ icon: Icon, title, description, color, children }) => (
        <div className="flex flex-col items-center">
            <div className={`w-48 bg-background border-l-4 ${color} rounded-r-lg shadow-lg p-3`}>
                <div className="flex items-center space-x-2">
                    <Icon className="w-5 h-5" />
                    <h5 className="font-bold">{title}</h5>
                </div>
                <p className="text-xs text-muted-foreground mt-1">{description}</p>
            </div>
            {children}
        </div>
    );

    const Connector = () => <div className="h-8 w-px bg-border" />;

    const Condition: React.FC<{ children: React.ReactNode }> = ({ children }) => (
        <div className="flex items-center justify-center space-x-4 mt-8">
            {children}
        </div>
    );
    
    return (
        <div className="bg-card p-6 rounded-lg shadow-lg flex flex-col h-full border">
            <h3 className="text-xl font-bold mb-4 flex items-center"><WorkflowIcon className="w-6 h-6 mr-2" /> Workflows de Marketing</h3>
            <div className="flex-1 overflow-auto bg-background p-6 rounded-lg relative">
                <div className="flex flex-col items-center">
                    <Node icon={PlusIcon} title="Disparador" description="Lead añadido al segmento 'Nuevos Leads'" color="border-green-500" />
                    <Connector />
                    <Node icon={MailIcon} title="Enviar Email" description="Plantilla: 'Bienvenida a Bordo'" color="border-blue-500" />
                    <Connector />
                    <Node icon={BotIcon} title="Condición" description="¿Abrió el email?" color="border-yellow-500" >
                        <div className="h-px w-24 bg-border mt-4" />
                        <div className="flex">
                            <div className="flex flex-col items-center">
                                <div className="h-8 w-px bg-border" />
                                <span className="text-xs text-green-400 bg-muted px-2 rounded-full">SÍ</span>
                                <div className="h-8 w-px bg-border" />
                                <Node icon={PlusIcon} title="Acción" description="Añadir etiqueta 'Interesado'" color="border-green-500" />
                            </div>
                            <div className="w-32" />
                            <div className="flex flex-col items-center">
                                <div className="h-8 w-px bg-border" />
                                <span className="text-xs text-red-400 bg-muted px-2 rounded-full">NO</span>
                                 <div className="h-8 w-px bg-border" />
                                <Node icon={CalendarPlusIcon} title="Espera" description="Esperar 2 días" color="border-purple-500" />
                                <Connector />
                                <Node icon={MessageIcon} title="Enviar SMS" description="Recordatorio de oferta" color="border-blue-500" />
                            </div>
                        </div>
                    </Node>
                </div>
                 <button className="absolute top-4 right-4 flex items-center space-x-2 bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90"><PlusIcon className="w-5 h-5"/> <span>Nuevo Workflow</span></button>
            </div>
        </div>
    );
}

const Level5_AutomationSuite: React.FC = () => {
    const [view, setView] = useState<'agent' | 'workflows'>('workflows');
    return (
        <div className="p-8 h-full flex flex-col bg-background">
            <div className="flex space-x-2 border-b mb-6">
                <button onClick={() => setView('workflows')} className={`flex items-center space-x-2 py-2 px-4 font-medium ${view === 'workflows' ? 'border-b-2 border-primary text-foreground' : 'text-muted-foreground hover:text-foreground'}`}>
                    <WorkflowIcon className="w-5 h-5" /><span>Workflows de Marketing</span>
                </button>
                <button onClick={() => setView('agent')} className={`flex items-center space-x-2 py-2 px-4 font-medium ${view === 'agent' ? 'border-b-2 border-primary text-foreground' : 'text-muted-foreground hover:text-foreground'}`}>
                    <BotIcon className="w-5 h-5" /><span>Agentes de IA Avanzados</span>
                </button>
            </div>
            
            {view === 'workflows' ? <MarketingWorkflows /> : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 flex-1">
                    <Chatbot />
                    <LiveAssistant />
                </div>
            )}
        </div>
    );
};

export default Level5_AutomationSuite;
