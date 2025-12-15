
import React, { useState } from 'react';
import { 
    AnalyticsIcon, MegaphoneIcon, MailIcon, SmsIcon, MmsIcon, WhatsAppIcon, 
    FacebookIcon, InstagramIcon, XIcon, TikTokIcon, YouTubeIcon, TwitchIcon, 
    CheckCircleIcon, XCircleIcon, GlobeAltIcon, TemplateIcon, SaveIcon, 
    DuplicateIcon, CodeBracketIcon, PlusCircleIcon, TrashIcon, SparklesIcon, XMarkIcon
} from './icons';
import { Segment, CampaignAnalytics, MarketingChannel, EmailTemplate, EmailTemplateProductCard } from '../types';

// --- MOCK DATA ---
const mockSegments: Segment[] = [
    { id: 'seg-1', name: 'Leads Calientes (Demo Solicitada)', contactCount: 12, criteria: 'Tags include "demo_solicitada"' },
    { id: 'seg-2', name: 'Clientes Inactivos (90+ días)', contactCount: 45, criteria: 'Last interaction > 90 days ago' },
];

const initialChannels: MarketingChannel[] = [
    { id: 'email', name: 'Email', icon: MailIcon, status: 'connected', category: 'messaging' },
    { id: 'whatsapp', name: 'WhatsApp', icon: WhatsAppIcon, status: 'connected', category: 'messaging' },
    { id: 'sms', name: 'SMS', icon: SmsIcon, status: 'connected', category: 'messaging' },
    { id: 'mms', name: 'MMS', icon: MmsIcon, status: 'connected', category: 'messaging' },
    { id: 'facebook', name: 'Facebook', icon: FacebookIcon, status: 'connected', category: 'social' },
    { id: 'instagram', name: 'Instagram', icon: InstagramIcon, status: 'connected', category: 'social' },
    { id: 'x', name: 'X (Twitter)', icon: XIcon, status: 'connected', category: 'social' },
    { id: 'tiktok', name: 'TikTok', icon: TikTokIcon, status: 'connected', category: 'social' },
    { id: 'youtube', name: 'YouTube', icon: YouTubeIcon, status: 'connected', category: 'social' },
    { id: 'twitch', name: 'Twitch', icon: TwitchIcon, status: 'connected', category: 'social' },
];

const mockAnalytics: CampaignAnalytics[] = [
    { id: 'camp-1', name: 'Lanzamiento Q2', channel: 'Email', sent: 1200, openRate: 25.4, clickRate: 4.1, conversions: 12, date: '2024-05-15' },
    { id: 'camp-2', name: 'Oferta Flash', channel: 'SMS', sent: 500, openRate: 0, clickRate: 15.2, conversions: 25, date: '2024-05-20' },
    { id: 'camp-3', name: 'Newsletter Mayo', channel: 'Email', sent: 2500, openRate: 18.9, clickRate: 2.5, conversions: 5, date: '2024-05-01' },
];

const defaultTemplate: EmailTemplate = {
    header: { logoUrl: 'https://via.placeholder.com/150x50/161b22/c9d1d9?text=TuLogo', menuItems: [{ text: 'Servicios', url: '#' }, { text: 'Contacto', url: '#' }] },
    body: { title: 'Descubre Nuestras Novedades', subtitle: 'Hemos preparado algo especial para ti, {{nombre_cliente}}.', products: [ { id: 'prod-1', imageUrl: 'https://via.placeholder.com/300x200', description: 'Un producto innovador que cambiará tu forma de trabajar.', price: '€99.99', ctaText: 'Ver Más', ctaUrl: '#' } ] },
    footer: { companyName: 'TuEmpresa Inc.', address: '123 Calle Falsa, Ciudad, País', phone: '+123 456 7890', email: 'hola@tuempresa.com' }
};

// --- SUB-COMPONENTS ---

const EmailTemplateEditor: React.FC<{
    template: EmailTemplate;
    onSave: (template: EmailTemplate) => void;
    onClose: () => void;
    channels: MarketingChannel[];
}> = ({ template: initialTemplate, onSave, onClose, channels }) => {
    const [template, setTemplate] = useState(initialTemplate);

    const handleInputChange = (section: keyof EmailTemplate, key: string, value: any, index?: number) => {
        setTemplate(prev => {
            const newTemplate = JSON.parse(JSON.stringify(prev)); // Deep copy
            if (index !== undefined) {
                 (newTemplate[section] as any)[key][index] = { ... (newTemplate[section] as any)[key][index], ...value };
            } else {
                (newTemplate[section] as any)[key] = value;
            }
            return newTemplate;
        });
    };

    const handleProductChange = (index: number, key: keyof EmailTemplateProductCard, value: string) => {
         setTemplate(prev => {
            const newProducts = [...prev.body.products];
            newProducts[index] = {...newProducts[index], [key]: value};
            return {...prev, body: {...prev.body, products: newProducts}};
        });
    }

    const addProduct = () => {
        const newProduct: EmailTemplateProductCard = { id: `prod-${Date.now()}`, imageUrl: 'https://via.placeholder.com/300x200', description: 'Nueva descripción', price: '€0.00', ctaText: 'Comprar', ctaUrl: '#' };
        setTemplate(prev => ({...prev, body: {...prev.body, products: [...prev.body.products, newProduct]}}));
    }
    
    const removeProduct = (id: string) => {
         setTemplate(prev => ({...prev, body: {...prev.body, products: prev.body.products.filter(p => p.id !== id)}}));
    }

    const generateWithAI = () => {
        // AI Simulation
        setTemplate(prev => ({...prev, body: {...prev.body, title: '¡Oferta Exclusiva para Ti!', subtitle: `Hola {{nombre_cliente}}, hemos visto tu interés en nuestros productos y tenemos una oferta que no podrás rechazar.`, products: prev.body.products.map(p => ({...p, description: 'Este producto ha sido mejorado con nuestra última tecnología para ofrecer un rendimiento sin igual.'}))}}));
    }

    const socialChannels = channels.filter(c => c.category === 'social' && c.status === 'connected');

    return (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
            <div className="bg-background rounded-2xl shadow-2xl w-full max-w-5xl h-[90vh] flex flex-col border">
                <header className="p-4 border-b flex justify-between items-center">
                    <div className="flex items-center space-x-2"><TemplateIcon className="w-6 h-6 text-primary" /><h3 className="text-xl font-bold">Editor de Plantillas de Correo</h3></div>
                    <div className="flex items-center space-x-2">
                        <button onClick={generateWithAI} className="flex items-center space-x-2 bg-primary text-primary-foreground px-3 py-1.5 rounded-md text-sm"><SparklesIcon className="w-4 h-4" /><span>Generar con IA</span></button>
                        <button className="bg-muted p-1.5 rounded-md"><SaveIcon className="w-5 h-5"/></button>
                        <button className="bg-muted p-1.5 rounded-md"><DuplicateIcon className="w-5 h-5"/></button>
                        <button className="bg-muted p-1.5 rounded-md"><CodeBracketIcon className="w-5 h-5"/></button>
                        <button onClick={onClose} className="p-1.5 rounded-full hover:bg-muted"><XMarkIcon className="w-5 h-5" /></button>
                    </div>
                </header>
                <div className="flex-1 flex overflow-hidden">
                    {/* Editor Panel */}
                    <div className="w-1/3 bg-background p-4 overflow-y-auto space-y-4">
                        <h4 className="font-bold text-lg">Variables Dinámicas</h4>
                        <div className="flex flex-wrap gap-2">
                            {['{{nombre_cliente}}', '{{nombre_empresa}}', '{{producto_interes}}'].map(v => <code key={v} className="text-xs bg-muted px-2 py-1 rounded">{v}</code>)}
                        </div>
                        <h4 className="font-bold text-lg mt-4">Cuerpo</h4>
                        <input type="text" value={template.body.title} onChange={e => handleInputChange('body', 'title', e.target.value)} className="w-full bg-input p-2 rounded border" />
                        <textarea value={template.body.subtitle} onChange={e => handleInputChange('body', 'subtitle', e.target.value)} className="w-full bg-input p-2 rounded border" rows={3}></textarea>
                        
                        {template.body.products.map((p, i) => (
                            <div key={p.id} className="bg-card p-3 rounded-lg space-y-2 relative border">
                                 <button onClick={() => removeProduct(p.id)} className="absolute top-2 right-2 p-1 bg-destructive/50 rounded-full hover:bg-destructive/80"><TrashIcon className="w-4 h-4"/></button>
                                 <input type="text" placeholder="URL de Imagen" value={p.imageUrl} onChange={e => handleProductChange(i, 'imageUrl', e.target.value)} className="w-full bg-input p-1 rounded text-sm border"/>
                                 <textarea placeholder="Descripción" value={p.description} onChange={e => handleProductChange(i, 'description', e.target.value)} className="w-full bg-input p-1 rounded text-sm border" rows={2}></textarea>
                                 <div className="flex gap-2">
                                    <input type="text" placeholder="Precio" value={p.price} onChange={e => handleProductChange(i, 'price', e.target.value)} className="w-1/2 bg-input p-1 rounded text-sm border"/>
                                    <input type="text" placeholder="Texto CTA" value={p.ctaText} onChange={e => handleProductChange(i, 'ctaText', e.target.value)} className="w-1/2 bg-input p-1 rounded text-sm border"/>
                                 </div>
                            </div>
                        ))}
                         <button onClick={addProduct} className="w-full flex items-center justify-center space-x-2 bg-muted p-2 rounded-lg hover:bg-accent"><PlusCircleIcon className="w-5 h-5"/><span>Añadir Bloque de Producto</span></button>
                    </div>
                    {/* Preview Panel */}
                    <div className="w-2/3 p-4 overflow-y-auto bg-muted">
                        <div className="bg-white text-gray-800 rounded-lg max-w-2xl mx-auto p-4 font-sans">
                            {/* Header */}
                            <header className="border-b pb-4 flex justify-between items-center">
                                <img src={template.header.logoUrl} alt="Logo" className="h-10" />
                                <nav className="space-x-4 text-sm">{template.header.menuItems.map(item => <a key={item.text} href={item.url} className="hover:underline">{item.text}</a>)}</nav>
                            </header>
                            {/* Body */}
                            <main className="py-6">
                                <h1 className="text-3xl font-bold mb-2">{template.body.title}</h1>
                                <p className="text-gray-600 mb-6">{template.body.subtitle}</p>
                                <div className="space-y-4">
                                    {template.body.products.map(p => (
                                        <div key={p.id} className="border rounded-lg flex gap-4 p-2">
                                            <img src={p.imageUrl} className="w-32 h-32 object-cover rounded" />
                                            <div><p>{p.description}</p><p className="font-bold mt-2">{p.price}</p><a href={p.ctaUrl} className="inline-block bg-[#4F46E5] text-white px-4 py-2 rounded-md mt-2 text-sm">{p.ctaText}</a></div>
                                        </div>
                                    ))}
                                </div>
                            </main>
                            {/* Footer */}
                            <footer className="border-t pt-4 text-center text-xs text-gray-500">
                                <p>{template.footer.companyName} - {template.footer.address}</p>
                                <div className="flex justify-center space-x-4 my-2">{socialChannels.map(c => <a key={c.id} href="#"><c.icon className="w-5 h-5 text-gray-500" /></a>)}</div>
                                <a href="#" className="underline">Cancelar suscripción</a>
                            </footer>
                        </div>
                    </div>
                </div>
                 <footer className="p-4 border-t flex justify-end">
                    <button onClick={() => { onSave(template); onClose(); }} className="bg-green-600 px-6 py-2 rounded-lg text-white">Guardar y Cerrar</button>
                </footer>
            </div>
        </div>
    );
};


const ChannelStatusBar = ({ channels }: { channels: MarketingChannel[] }) => (
    <div className="bg-card p-3 rounded-lg flex flex-wrap gap-x-4 gap-y-2 items-center mb-6 border shadow-sm">
        <h3 className="font-semibold text-muted-foreground whitespace-nowrap">Canales Conectados:</h3>
        {channels.map(channel => (
            <div key={channel.id} className="group relative flex items-center space-x-1.5" title={channel.name}>
                <channel.icon className={`w-5 h-5 ${channel.status === 'connected' ? 'text-foreground' : 'text-gray-600'}`} />
                {channel.status === 'connected' 
                    ? <div className="w-2 h-2 bg-green-500 rounded-full" />
                    : <div className="w-2 h-2 bg-red-500 rounded-full" />}
            </div>
        ))}
    </div>
);

const SocialPostPreview: React.FC<{ platform: 'facebook' | 'instagram' | 'x', content: string }> = ({ platform, content }) => {
    const platformStyles = {
        facebook: { icon: FacebookIcon, brandColor: 'text-blue-500' },
        instagram: { icon: InstagramIcon, brandColor: 'text-pink-500' },
        x: { icon: XIcon, brandColor: 'text-foreground' },
    };
    const { icon: Icon, brandColor } = platformStyles[platform] || platformStyles.x;

    return (
        <div className="bg-background rounded-lg shadow-md w-full max-w-sm mx-auto my-2 border">
            <div className="flex items-center p-3 border-b">
                <div className="w-10 h-10 bg-card rounded-full flex items-center justify-center">
                    <Icon className={`w-6 h-6 ${brandColor}`} />
                </div>
                <div className="ml-3">
                    <p className="font-bold text-sm text-foreground">TuEmpresa</p>
                    <p className="text-xs text-muted-foreground">@tuempresa · Ahora</p>
                </div>
            </div>
            <div className="p-3">
                <p className="text-foreground text-sm whitespace-pre-wrap">{content || `Vista previa para ${platform}...`}</p>
            </div>
            <div className="h-48 bg-card flex items-center justify-center">
                <GlobeAltIcon className="w-12 h-12 text-muted-foreground" />
            </div>
            <div className="flex justify-around p-2 border-t text-muted-foreground">
                <span className="text-sm">💬</span><span className="text-sm">🔁</span><span className="text-sm">❤️</span><span className="text-sm">🔗</span>
            </div>
        </div>
    );
};

const CampaignCreator = () => {
    const [channels] = useState<MarketingChannel[]>(initialChannels);
    const [selectedChannels, setSelectedChannels] = useState<Set<string>>(new Set(['email', 'facebook']));
    const [content, setContent] = useState<{ [key: string]: string }>({});
    const [isEditorOpen, setIsEditorOpen] = useState(false);
    const [emailTemplate, setEmailTemplate] = useState<EmailTemplate>(defaultTemplate);

    const handleChannelToggle = (id: string) => {
        const channel = channels.find(c => c.id === id);
        if (channel && channel.status === 'disconnected') {
            alert(`El canal ${channel.name} está desconectado. Conéctalo en Integraciones.`);
            return;
        }
        
        setSelectedChannels(prevSelected => {
            const newSelection = new Set(prevSelected);
            if (newSelection.has(id)) {
                newSelection.delete(id);
            } else {
                newSelection.add(id);
            }
            return newSelection;
        });
    };

    const handleContentChange = (channelId: string, value: string) => {
        setContent(prev => ({ ...prev, [channelId]: value }));
    };

    const handleMasterContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const masterValue = e.target.value;
        const newContent: { [key: string]: string } = {};
        selectedChannels.forEach(channelId => {
            if (channelId !== 'email') {
                newContent[channelId] = masterValue;
            }
        });
        setContent(prev => ({...prev, ...newContent}));
    };

    return (
        <div className="bg-card rounded-lg p-6 border shadow-md">
            {isEditorOpen && <EmailTemplateEditor template={emailTemplate} onSave={setEmailTemplate} onClose={() => setIsEditorOpen(false)} channels={channels}/>}
            <ChannelStatusBar channels={channels} />
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1 space-y-6">
                    <div>
                        <h3 className="font-bold text-lg mb-2">Paso 1: Selecciona Canales</h3>
                        <div className="space-y-2">
                            {channels.map(channel => (
                                <label key={channel.id} className={`flex items-center space-x-3 p-2 bg-background rounded-md ${channel.status === 'connected' ? 'cursor-pointer hover:bg-accent' : 'opacity-50 cursor-not-allowed'}`}>
                                    <input type="checkbox" checked={selectedChannels.has(channel.id)} onChange={() => handleChannelToggle(channel.id)} disabled={channel.status === 'disconnected'} className="h-5 w-5 bg-input border-border rounded text-primary focus:ring-primary" />
                                    <channel.icon className="w-5 h-5" />
                                    <span>{channel.name}</span>
                                </label>
                            ))}
                        </div>
                    </div>
                    <div>
                        <h3 className="font-bold text-lg mb-2">Paso 2: Contenido Maestro (Redes y SMS)</h3>
                        <textarea rows={8} onChange={handleMasterContentChange} placeholder="Escribe el contenido principal para redes sociales, WhatsApp, SMS..." className="w-full bg-input border rounded-md p-2" />
                    </div>
                </div>
                <div className="lg:col-span-2 space-y-4">
                    <h3 className="font-bold text-lg">Paso 3: Personaliza y Previsualiza</h3>
                    <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
                        {[...selectedChannels].map(id => {
                            const channel = channels.find(c => c.id === id)!;
                            if (channel.id === 'email') {
                                return (
                                     <div key={id} className="bg-background p-4 rounded-lg border">
                                        <div className="flex items-center space-x-2 mb-2"><channel.icon className="w-5 h-5" /><h4 className="font-semibold">{channel.name}</h4></div>
                                        <div className="border border-dashed border-muted-foreground rounded-lg p-2 text-center">
                                            <p className="text-sm text-muted-foreground mb-2">Plantilla: "{emailTemplate.body.title}"</p>
                                            <button onClick={() => setIsEditorOpen(true)} className="flex items-center mx-auto space-x-2 bg-primary text-primary-foreground px-3 py-1.5 rounded-md text-sm"><TemplateIcon className="w-4 h-4"/><span>Seleccionar / Editar Plantilla</span></button>
                                        </div>
                                     </div>
                                );
                            }
                            return (
                                <div key={id} className="bg-background p-4 rounded-lg border">
                                    <div className="flex items-center space-x-2 mb-2"><channel.icon className="w-5 h-5" /><h4 className="font-semibold">{channel.name}</h4></div>
                                    <textarea rows={4} value={content[id] || ''} onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleContentChange(id, e.target.value)} className="w-full bg-input border rounded-md p-2" />
                                    {(id === 'facebook' || id === 'instagram' || id === 'x') && (
                                        <div className="mt-2"><h5 className="text-xs font-bold text-muted-foreground mb-1">PREVISUALIZACIÓN</h5><SocialPostPreview platform={id as 'facebook'|'instagram'|'x'} content={content[id] || ''} /></div>
                                    )}
                                </div>
                            );
                        })}
                         {selectedChannels.size === 0 && <p className="text-muted-foreground text-center py-10">Selecciona un canal para empezar a componer tu campaña.</p>}
                    </div>
                </div>
            </div>
             <div className="flex justify-end pt-6 border-t mt-6">
                <button disabled={selectedChannels.size === 0} className="bg-green-600 text-white px-6 py-2 rounded-md hover:opacity-90 disabled:opacity-50">Enviar Campaña Multicanal</button>
            </div>
        </div>
    );
};

const AnalyticsDashboard: React.FC = () => (
    <div className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-card p-4 rounded-xl border shadow-sm"><p className="text-sm text-muted-foreground">Tasa de Apertura (Promedio)</p><p className="text-2xl font-bold">21.3%</p></div>
            <div className="bg-card p-4 rounded-xl border shadow-sm"><p className="text-sm text-muted-foreground">Tasa de Clics (Promedio)</p><p className="text-2xl font-bold">3.8%</p></div>
            <div className="bg-card p-4 rounded-xl border shadow-sm"><p className="text-sm text-muted-foreground">Conversiones (Últimos 30d)</p><p className="text-2xl font-bold">42</p></div>
            <div className="bg-card p-4 rounded-xl border shadow-sm"><p className="text-sm text-muted-foreground">Nuevos Leads (Últimos 30d)</p><p className="text-2xl font-bold">112</p></div>
        </div>
        <div className="bg-card rounded-xl border shadow-md">
            <h4 className="p-4 font-bold text-foreground">Rendimiento por Campaña</h4>
            <table className="w-full text-left">
                <thead className="border-b border-t text-sm text-muted-foreground">
                    <tr><th className="p-4">Campaña</th><th className="p-4">Canal</th><th className="p-4">Tasa Apertura</th><th className="p-4">Tasa Clics</th><th className="p-4">Conversiones</th></tr>
                </thead>
                <tbody>
                    {mockAnalytics.map(c => (
                        <tr key={c.id} className="border-b">
                            <td className="p-4 font-semibold">{c.name}</td><td className="p-4">{c.channel}</td><td className="p-4">{c.openRate}%</td><td className="p-4">{c.clickRate}%</td><td className="p-4">{c.conversions}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    </div>
);

const Level1_Communication: React.FC = () => {
    const [view, setView] = useState<'campaigns' | 'analytics'>('campaigns');

    return (
        <div className="p-8 h-full overflow-y-auto">
            <div className="flex space-x-2 border-b mb-6">
                <button onClick={() => setView('campaigns')} className={`flex items-center space-x-2 py-2 px-4 font-medium ${view === 'campaigns' ? 'border-b-2 border-primary text-foreground' : 'text-muted-foreground hover:text-foreground'}`}>
                    <MegaphoneIcon className="w-5 h-5" /><span>Campañas</span>
                </button>
                <button onClick={() => setView('analytics')} className={`flex items-center space-x-2 py-2 px-4 font-medium ${view === 'analytics' ? 'border-b-2 border-primary text-foreground' : 'text-muted-foreground hover:text-foreground'}`}>
                    <AnalyticsIcon className="w-5 h-5" /><span>Analíticas</span>
                </button>
            </div>
            
            {view === 'campaigns' ? <CampaignCreator /> : <AnalyticsDashboard />}
        </div>
    );
};

export default Level1_Communication;