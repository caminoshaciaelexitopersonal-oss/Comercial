
import React, { useState } from 'react';
import { Customer, PipelineStage, Seller, Task, Segment, Ticket, KnowledgeBaseArticle, TicketStatus, TicketMessage, Integration, IntegrationCategory, Quote } from '../types';
import {
    TrendingUpIcon, EuroIcon, CheckCircleIcon, UsersIcon, ClipboardListIcon,
    PipelineIcon, DashboardIcon, PlusIcon, SearchIcon, PhoneIcon, MailIcon, 
    BriefcaseIcon, XMarkIcon, AlertTriangleIcon, LinkedInIcon, CalendarPlusIcon, 
    MessageIcon, TargetIcon, FormIcon, SupportIcon, BookOpenIcon, 
    ChatBubbleLeftRightIcon, KanbanIcon, ListIcon, TicketIcon, HourglassIcon, 
    PaperAirplaneIcon, ArchiveBoxIcon, GoogleIcon, PinterestIcon, SnapchatIcon, 
    WhatsAppIcon, TelegramIcon, ZoomIcon, TeamsIcon, SmsIcon, TwitchIcon, 
    FacebookIcon, InstagramIcon, TikTokIcon, YouTubeIcon, XIcon, StarIcon, 
    InvoiceIcon, SapIcon, QuickbooksIcon, ShopifyIcon, ChevronRightIcon,
    ContactsIcon
} from './icons';

// --- MOCK DATA (EXPANDED) ---
const sellers: Seller[] = [
    { id: 'seller-1', name: 'Ana Gómez', avatarUrl: 'https://randomuser.me/api/portraits/women/68.jpg' },
    { id: 'seller-2', name: 'Carlos Díaz', avatarUrl: 'https://randomuser.me/api/portraits/men/68.jpg' },
    { id: 'support-1', name: 'Laura Pausini', avatarUrl: 'https://randomuser.me/api/portraits/women/69.jpg' },
];

const initialTickets: Ticket[] = [
    { id: 'TKT-001', subject: 'Problema con la facturación', customerId: 1, status: 'in-progress', priority: 'high', category: 'Facturación', assigneeId: 'support-1', createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), slaExpiresAt: new Date(Date.now() + 1 * 24 * 60 * 60 * 1000).toISOString(), conversation: [{id:'tm-1', author: 'Elena Rodriguez', text: 'No veo la última factura en mi portal.', timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), type: 'reply'}]},
    { id: 'TKT-002', subject: 'Consulta sobre integración API', customerId: 4, status: 'new', priority: 'medium', category: 'Técnico', createdAt: new Date().toISOString(), slaExpiresAt: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(), conversation: []},
    { id: 'TKT-003', subject: 'El producto llegó dañado', customerId: 2, status: 'resolved', priority: 'urgent', category: 'Reclamo', assigneeId: 'support-1', createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), slaExpiresAt: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(), conversation: [], satisfactionRating: 4},
];

const initialCustomers: Customer[] = [
    {
        id: 1, name: 'Elena Rodriguez', company: 'Innovatech Solutions', avatarUrl: 'https://randomuser.me/api/portraits/women/71.jpg',
        socials: { linkedin: '#', x: '#', facebook: '#' }, priority: 'high', tags: ['lead_caliente', 'demo_solicitada'],
        pipelineStage: 'proposal', opportunityValue: 15000, assignedTo: 'seller-1', lastUpdated: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
        interactions: [
            { id: 'int-1', type: 'meeting', date: '2024-05-20T10:00:00Z', notes: 'Reunión de demo exitosa. Interesados en el paquete premium.' },
            { id: 'int-2', type: 'email', date: '2024-05-21T15:30:00Z', notes: 'Enviada propuesta y cotización #Q-24-001.' }
        ],
        contacts: [{ id: 'con-1', name: 'Elena Rodriguez', role: 'CTO', email: 'elena.r@innovatech.com', phone: '+1-202-555-0149' }],
        quotes: [{ id: 'q-1', number: 'Q-24-001', date: '2024-05-21', amount: 15000, status: 'accepted', paid: true }],
        tasks: [{ id: 'task-1', title: 'Seguimiento de propuesta', dueDate: '2024-05-28', completed: false }],
        tickets: [initialTickets[0]]
    },
    {
        id: 2, name: 'Marco Vega', company: 'Quantum Dynamics', avatarUrl: 'https://randomuser.me/api/portraits/men/75.jpg',
        socials: { linkedin: '#' }, priority: 'medium', tags: ['networking', 'B2B'],
        pipelineStage: 'contacted', opportunityValue: 8000, assignedTo: 'seller-2', lastUpdated: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
        interactions: [{ id: 'int-3', type: 'call', date: '2024-05-18T14:00:00Z', notes: 'Primera llamada de contacto. Mostró interés inicial.' }],
        contacts: [], quotes: [], tasks: [{ id: 'task-2', title: 'Agendar llamada de descubrimiento', dueDate: '2024-05-25', completed: true }],
        tickets: [initialTickets[2]]
    },
    {
        id: 4, name: 'Javier Morales', company: 'HealthPlus Labs', avatarUrl: 'https://randomuser.me/api/portraits/men/80.jpg',
        socials: { linkedin: '#' }, priority: 'high', tags: ['referido'],
        pipelineStage: 'negotiation', opportunityValue: 25000, assignedTo: 'seller-2', lastUpdated: new Date().toISOString(),
        interactions: [{ id: 'int-4', type: 'meeting', date: '2024-05-22T11:00:00Z', notes: 'Negociando términos del contrato. Piden un descuento del 10%.' }],
        contacts: [], quotes: [{id: 'q-2', number: 'Q-24-002', date: '2024-05-23', amount: 22500, status: 'sent'}], tasks: [{ id: 'task-3', title: 'Preparar contraoferta', dueDate: '2024-05-24', completed: false }],
        tickets: [initialTickets[1]]
    },
    {
        id: 3, name: 'Sofia Castillo', company: 'NextGen Logistics', avatarUrl: 'https://randomuser.me/api/portraits/women/76.jpg',
        socials: { linkedin: '#' }, priority: 'low', tags: ['lead_frio'],
        pipelineStage: 'new', opportunityValue: 5000, assignedTo: 'seller-1', lastUpdated: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
        interactions: [], contacts: [], quotes: [], tasks: [], tickets: []
    },
    {
        id: 5, name: 'Lucia Fernandez', company: 'EcoWear Apparel', avatarUrl: 'https://randomuser.me/api/portraits/women/81.jpg',
        socials: { linkedin: '#' }, priority: 'medium', tags: ['sostenibilidad'],
        pipelineStage: 'won', opportunityValue: 12000, assignedTo: 'seller-1', lastUpdated: new Date().toISOString(),
        interactions: [], contacts: [], quotes: [], tasks: [], tickets: []
    }
];

const mockSegments: Segment[] = [
    { id: 'seg-1', name: 'Leads Calientes (Demo Solicitada)', contactCount: 1, criteria: 'Tags include "demo_solicitada"' },
    { id: 'seg-2', name: 'Clientes Inactivos (90+ días)', contactCount: 0, criteria: 'Last interaction > 90 days ago' },
    { id: 'seg-3', name: 'Clientes VIP (Valor > €20k)', contactCount: 1, criteria: 'Total value > 20000' },
];

const mockKbArticles: KnowledgeBaseArticle[] = [
    { id: 'kb-1', title: '¿Cómo actualizar mis datos de facturación?', category: 'Facturación', excerpt: 'Accede a tu perfil y haz clic en la sección de facturación para...' },
    { id: 'kb-2', title: 'Guía de inicio rápido para la API', category: 'Guías', excerpt: 'Para empezar a usar nuestra API, primero genera una clave desde...' },
    { id: 'kb-3', title: 'Política de devoluciones', category: 'Reclamos', excerpt: 'Puedes solicitar una devolución dentro de los 30 días posteriores a tu...' },
];

const initialIntegrations: Integration[] = [
    { id: 'meta-ads', name: 'Meta Ads', category: 'ads', status: 'connected' },
    { id: 'google-ads', name: 'Google Ads', category: 'ads', status: 'disconnected' },
    { id: 'linkedin-ads', name: 'LinkedIn Ads', category: 'ads', status: 'disconnected' },
    { id: 'tiktok-ads', name: 'TikTok Ads', category: 'ads', status: 'disconnected' },
    { id: 'x-ads', name: 'X Ads', category: 'ads', status: 'disconnected' },
    { id: 'pinterest-ads', name: 'Pinterest Ads', category: 'ads', status: 'disconnected' },
    { id: 'snapchat-ads', name: 'Snapchat Ads', category: 'ads', status: 'disconnected' },
    { id: 'youtube-ads', name: 'YouTube Ads', category: 'ads', status: 'disconnected' },
    { id: 'whatsapp', name: 'WhatsApp Business', category: 'communication', status: 'connected' },
    { id: 'sms', name: 'SMS (Twilio)', category: 'communication', status: 'disconnected' },
    { id: 'telegram', name: 'Telegram Bot', category: 'communication', status: 'disconnected' },
    { id: 'gmail', name: 'Gmail', category: 'communication', status: 'connected' },
    { id: 'outlook', name: 'Outlook 365', category: 'communication', status: 'disconnected' },
    { id: 'zoom', name: 'Zoom', category: 'communication', status: 'disconnected' },
    { id: 'google-meet', name: 'Google Meet', category: 'communication', status: 'disconnected' },
    { id: 'teams', name: 'Microsoft Teams', category: 'communication', status: 'disconnected' },
    { id: 'voip', name: 'VoIP (Aircall)', category: 'communication', status: 'disconnected' },
    { id: 'facebook', name: 'Facebook', category: 'social', status: 'connected' },
    { id: 'instagram', name: 'Instagram', category: 'social', status: 'connected' },
    { id: 'linkedin', name: 'LinkedIn', category: 'social', status: 'disconnected' },
    { id: 'tiktok', name: 'TikTok', category: 'social', status: 'disconnected' },
    { id: 'youtube', name: 'YouTube', category: 'social', status: 'disconnected' },
    { id: 'twitch', name: 'Twitch', category: 'social', status: 'disconnected' },
    { id: 'sap', name: 'SAP S/4HANA', category: 'erp', status: 'disconnected' },
    { id: 'quickbooks', name: 'QuickBooks', category: 'erp', status: 'connected' },
    { id: 'shopify', name: 'Shopify', category: 'erp', status: 'disconnected' },
];

// --- STAGES CONFIG ---
const pipelineStages: { id: PipelineStage, title: string }[] = [ { id: 'new', title: 'Nuevos Leads' }, { id: 'contacted', title: 'Contactados' }, { id: 'proposal', title: 'Propuesta Enviada' }, { id: 'negotiation', title: 'Negociación' }, { id: 'won', title: 'Ganado' }, { id: 'lost', title: 'Perdido' }];
const ticketStages: { id: TicketStatus, title: string }[] = [ { id: 'new', title: 'Nuevo' }, { id: 'in-progress', title: 'En Progreso' }, { id: 'resolved', title: 'Resuelto' }];
const STAGE_COLORS: { [key in PipelineStage]: string } = { new: 'bg-blue-500/20 text-blue-300', contacted: 'bg-cyan-500/20 text-cyan-300', proposal: 'bg-purple-500/20 text-purple-300', negotiation: 'bg-yellow-500/20 text-yellow-300', won: 'bg-green-500/20 text-green-300', lost: 'bg-red-500/20 text-red-300' };
const TICKET_STAGE_COLORS: { [key in TicketStatus]: string } = { new: 'bg-blue-500/20 text-blue-300', 'in-progress': 'bg-yellow-500/20 text-yellow-300', resolved: 'bg-green-500/20 text-green-300' };
const TICKET_PRIORITY_COLORS: { [key: string]: string } = { low: 'bg-gray-500', medium: 'bg-blue-500', high: 'bg-yellow-500', urgent: 'bg-red-500' };

const KpiCard: React.FC<{ icon: React.FC<{className?: string}>, title: string, value: string, change?: string }> = ({ icon: Icon, title, value, change }) => (
    <div className="bg-card p-4 rounded-xl border shadow-sm">
        <div className="flex justify-between items-center mb-2">
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <Icon className="w-5 h-5 text-muted-foreground" />
        </div>
        <div className="flex items-baseline space-x-2">
            <p className="text-3xl font-bold text-foreground">{value}</p>
            {change && <span className={`text-sm font-semibold ${change.startsWith('+') ? 'text-green-400' : 'text-red-400'}`}>{change}</span>}
        </div>
    </div>
);

// --- CRM & SALES VIEWS ---
const Dashboard: React.FC<{ customers: Customer[], tickets: Ticket[] }> = ({ customers, tickets }) => {
    const pipelineValue = customers.filter(c => c.pipelineStage !== 'won' && c.pipelineStage !== 'lost').reduce((sum, c) => sum + c.opportunityValue, 0);
    const pendingTasks = customers.reduce((sum, c) => sum + c.tasks.filter(t => !t.completed).length, 0);
    return (
        <div className="p-8 space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KpiCard icon={UsersIcon} title="Nuevos Leads (30d)" value="12" change="+5%" />
                <KpiCard icon={TrendingUpIcon} title="Valor del Pipeline" value={`€${pipelineValue.toLocaleString('es-ES')}`} />
                <KpiCard icon={ClipboardListIcon} title="Tareas Pendientes" value={pendingTasks.toString()} />
                <KpiCard icon={TicketIcon} title="Tickets Abiertos" value={tickets.filter(t => t.status !== 'resolved').length.toString()} />
            </div>
            {/* Other dashboard widgets can be added here */}
        </div>
    );
};

const PipelineView: React.FC<{ customers: Customer[]; setCustomers: React.Dispatch<React.SetStateAction<Customer[]>>; onSelectCustomer: (customer: Customer) => void; }> = ({ customers, setCustomers, onSelectCustomer }) => {
    const handleDragStart = (e: React.DragEvent<HTMLDivElement>, customerId: number) => {
        e.dataTransfer.setData('customerId', customerId.toString());
    };
    const handleDrop = (e: React.DragEvent<HTMLDivElement>, stageId: PipelineStage) => {
        e.preventDefault();
        const customerId = parseInt(e.dataTransfer.getData('customerId'), 10);
        setCustomers(prev => prev.map(c => c.id === customerId ? { ...c, pipelineStage: stageId, lastUpdated: new Date().toISOString() } : c));
        e.currentTarget.classList.remove('bg-accent');
    };
    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.currentTarget.classList.add('bg-accent');
    };
    const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
        e.currentTarget.classList.remove('bg-accent');
    };
    return (
        <div className="flex-1 p-8 overflow-x-auto">
            <div className="flex space-x-6 min-w-max h-full">
                {pipelineStages.map(stage => {
                    const customersInStage = customers.filter(c => c.pipelineStage === stage.id);
                    const stageValue = customersInStage.reduce((sum, c) => sum + c.opportunityValue, 0);
                    return (
                        <div key={stage.id} className="w-80 bg-secondary rounded-xl flex flex-col h-full" onDrop={(e) => handleDrop(e, stage.id)} onDragOver={handleDragOver} onDragLeave={handleDragLeave}>
                            <div className={`p-4 border-b`}>
                                <h4 className="font-bold text-foreground flex justify-between items-center">
                                    <span>{stage.title}</span>
                                    <span className="text-sm font-normal text-muted-foreground">{customersInStage.length}</span>
                                </h4>
                                <p className="text-sm text-muted-foreground">€{stageValue.toLocaleString()}</p>
                            </div>
                            <div className="p-2 space-y-2 overflow-y-auto flex-1">
                                {customersInStage.map(customer => (
                                    <div key={customer.id} draggable onDragStart={(e) => handleDragStart(e, customer.id)}>
                                        <CustomerCard customer={customer} onSelect={() => onSelectCustomer(customer)} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
const CustomerCard: React.FC<{ customer: Customer; onSelect: () => void }> = ({ customer, onSelect }) => {
    const seller = sellers.find(s => s.id === customer.assignedTo);
    const daysSinceUpdate = Math.floor((new Date().getTime() - new Date(customer.lastUpdated).getTime()) / (1000 * 60 * 60 * 24));
    const isInactive = daysSinceUpdate > 7;
    const priorityColors = { high: 'bg-red-500', medium: 'bg-yellow-500', low: 'bg-blue-500' };
    return (
        <div className="bg-card p-3 rounded-lg shadow-md cursor-pointer border border-transparent hover:border-primary hover:shadow-xl transition-all group" onClick={onSelect} > 
            <div className="flex justify-between items-start"> 
                <p className="font-bold text-foreground text-sm group-hover:text-primary transition-colors">{customer.name}</p> 
                <span className={`w-3 h-3 rounded-full ${priorityColors[customer.priority]}`} title={`Prioridad: ${customer.priority}`}></span>
            </div> 
            <p className="text-xs text-muted-foreground truncate">{customer.company}</p> 
            <div className="flex justify-between items-end mt-3"> 
                <div className="flex flex-col">
                    <span className="text-sm font-semibold text-foreground">€{customer.opportunityValue.toLocaleString()}</span> 
                    <div className="flex items-center space-x-1 mt-1">
                        {isInactive && <AlertTriangleIcon className="w-4 h-4 text-yellow-400" title={`Inactivo por ${daysSinceUpdate} días`} />} 
                        {customer.tags.slice(0, 2).map(tag => (
                            <span key={tag} className="text-[10px] bg-secondary px-1.5 py-0.5 rounded-full text-secondary-foreground">{tag}</span>
                        ))}
                    </div>
                </div>
                {seller && <img src={seller.avatarUrl} alt={seller.name} className="w-7 h-7 rounded-full border-2 border-card" />} 
            </div> 
        </div>
    );
};
const ContactListView: React.FC<{ customers: Customer[], onSelectCustomer: (c: Customer) => void }> = ({ customers, onSelectCustomer }) => {
    const [subView, setSubView] = useState<'all' | 'segments'>('all');
    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <div className="flex space-x-1 bg-card p-1 rounded-lg">
                    <button onClick={() => setSubView('all')} className={`px-3 py-1 text-sm rounded-md ${subView === 'all' ? 'bg-primary text-primary-foreground' : 'text-foreground'}`}>Todos</button>
                    <button onClick={() => setSubView('segments')} className={`px-3 py-1 text-sm rounded-md ${subView === 'segments' ? 'bg-primary text-primary-foreground' : 'text-foreground'}`}>Segmentos</button>
                </div>
            </div>
            {subView === 'all' ? (
                <div className="bg-card rounded-xl shadow-lg">
                    <table className="w-full text-left">
                        <thead className="border-b text-xs text-muted-foreground uppercase">
                            <tr>
                                <th className="p-4">Nombre</th>
                                <th className="p-4">Empresa</th>
                                <th className="p-4">Valor</th>
                                <th className="p-4">Etapa</th>
                                <th className="p-4">Asignado a</th>
                            </tr>
                        </thead>
                        <tbody>
                            {customers.map(c => {
                                const seller = sellers.find(s => s.id === c.assignedTo);
                                return (
                                    <tr key={c.id} className="border-b hover:bg-muted cursor-pointer" onClick={() => onSelectCustomer(c)}>
                                        <td className="p-4 flex items-center space-x-3"><img src={c.avatarUrl} alt={c.name} className="w-8 h-8 rounded-full" /><span className="font-semibold">{c.name}</span></td>
                                        <td className="p-4 text-muted-foreground">{c.company}</td><td className="p-4 text-muted-foreground">€{c.opportunityValue.toLocaleString()}</td>
                                        <td className="p-4"><span className={`px-2 py-1 text-xs font-bold rounded-full ${STAGE_COLORS[c.pipelineStage]}`}>{c.pipelineStage}</span></td>
                                        <td className="p-4 text-muted-foreground">{seller?.name || 'N/A'}</td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            ) : (
                <div className="bg-card rounded-xl shadow-lg p-6">
                    <h4 className="text-xl font-bold mb-4">Gestor de Segmentos</h4>
                    <div className="space-y-4">
                        {mockSegments.map(seg => (
                            <div key={seg.id} className="bg-muted p-4 rounded-lg flex justify-between items-center">
                                <div>
                                    <p className="font-bold">{seg.name}</p>
                                    <p className="text-sm text-muted-foreground">Criterio: {seg.criteria}</p>
                                </div>
                                <span className="font-bold text-primary">{seg.contactCount} Contactos</span>
                            </div>
                        ))}
                    </div>
                    <button className="mt-6 flex items-center space-x-2 bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90">
                        <PlusIcon className="w-5 h-5" />
                        <span>Crear Segmento</span>
                    </button>
                </div>
            )}
        </div>
    );
};

const LeadCaptureView: React.FC = () => {
    const [integrations, setIntegrations] = useState<Integration[]>(initialIntegrations);

    const iconMap: { [key: string]: React.FC<{className?: string}> } = {
        'meta-ads': FacebookIcon, 'google-ads': GoogleIcon, 'linkedin-ads': LinkedInIcon,
        'tiktok-ads': TikTokIcon, 'x-ads': XIcon, 'pinterest-ads': PinterestIcon,
        'snapchat-ads': SnapchatIcon, 'youtube-ads': YouTubeIcon, 'whatsapp': WhatsAppIcon,
        'sms': SmsIcon, 'telegram': TelegramIcon, 'gmail': MailIcon,
        'outlook': MailIcon, 'zoom': ZoomIcon, 'google-meet': GoogleIcon,
        'teams': TeamsIcon, 'voip': PhoneIcon, 'facebook': FacebookIcon,
        'instagram': InstagramIcon, 'linkedin': LinkedInIcon, 'tiktok': TikTokIcon,
        'youtube': YouTubeIcon, 'twitch': TwitchIcon, 'sap': SapIcon, 'quickbooks': QuickbooksIcon,
        'shopify': ShopifyIcon
    };

    const handleToggleIntegration = (id: string) => {
        setIntegrations(prev => prev.map(int => 
            int.id === id 
            ? { ...int, status: int.status === 'connected' ? 'disconnected' : 'connected' }
            : int
        ));
    };

    const IntegrationCard: React.FC<{ integration: Integration }> = ({ integration }) => {
        const Icon = iconMap[integration.id] || BriefcaseIcon;
        const isConnected = integration.status === 'connected';
        return (
            <div className="bg-card p-4 rounded-xl flex flex-col items-center justify-between text-center shadow-lg border">
                <Icon className="w-10 h-10 mb-2 text-foreground" />
                <p className="font-semibold text-foreground mb-3 h-10 flex items-center">{integration.name}</p>
                <button 
                    onClick={() => handleToggleIntegration(integration.id)}
                    className={`w-full py-2 text-sm rounded-md font-bold transition-colors ${
                        isConnected 
                        ? 'bg-green-500/20 text-green-400 hover:bg-green-500/40' 
                        : 'bg-primary text-primary-foreground hover:bg-primary/90'
                    }`}
                >
                    {isConnected ? 'Gestionar' : 'Conectar'}
                </button>
            </div>
        );
    };
    
    const IntegrationCategorySection: React.FC<{title: string, category: IntegrationCategory, color: string}> = ({title, category, color}) => (
        <div className="bg-card p-6 rounded-2xl border shadow-sm">
            <h4 className={`font-bold text-xl mb-4 ${color}`}>{title}</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
                {integrations.filter(int => int.category === category).map(int => <IntegrationCard key={int.id} integration={int} />)}
            </div>
        </div>
    );

    return (
        <div className="p-8 space-y-8">
            <IntegrationCategorySection title="Publicidad y Marketing Digital" category="ads" color="text-blue-400" />
            <IntegrationCategorySection title="Comunicación y Mensajería" category="communication" color="text-teal-400" />
            <IntegrationCategorySection title="Redes Sociales" category="social" color="text-pink-400" />
            <IntegrationCategorySection title="ERP y Finanzas" category="erp" color="text-yellow-400" />
        </div>
    );
};


// --- SUPPORT CENTER VIEWS ---
const SupportDashboard: React.FC<{ tickets: Ticket[] }> = ({ tickets }) => {
    const validRatings = tickets.map(t => t.satisfactionRating).filter((r): r is number => r !== undefined);
    const avgSatisfaction = validRatings.length > 0 ? (validRatings.reduce((a,b) => a+b, 0) / validRatings.length * 20).toFixed(1) : 'N/A';
    
    return (
        <div className="space-y-8 p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KpiCard icon={TicketIcon} title="Tickets Abiertos" value={tickets.filter(t => t.status !== 'resolved').length.toString()} />
                <KpiCard icon={TrendingUpIcon} title="Tiempo Resolución (Promedio)" value="8.2h" />
                <KpiCard icon={CheckCircleIcon} title="Satisfacción Cliente (CSAT)" value={`${avgSatisfaction}%`} />
                <KpiCard icon={AlertTriangleIcon} title="Incumplimientos de SLA" value={tickets.filter(t => new Date(t.slaExpiresAt) < new Date() && t.status !== 'resolved').length.toString()} />
            </div>
        </div>
    );
};

const TicketCard: React.FC<{ ticket: Ticket; customer?: Customer; onSelect: () => void; }> = ({ ticket, customer, onSelect }) => {
    const isSlaBreached = new Date(ticket.slaExpiresAt) < new Date() && ticket.status !== 'resolved';
    return (
        <div onClick={onSelect} className="bg-card p-4 rounded-lg shadow-md cursor-pointer border hover:border-primary">
            <div className="flex justify-between items-start">
                <p className="font-bold text-foreground truncate pr-2">{ticket.subject}</p>
                <span className={`px-2 py-1 text-xs font-bold rounded-full text-white ${TICKET_PRIORITY_COLORS[ticket.priority]}`}>{ticket.priority}</span>
            </div>
            <p className="text-sm text-muted-foreground">#{ticket.id} de {customer?.name || 'Cliente Desconocido'}</p>
            {isSlaBreached && <div className="flex items-center text-destructive text-sm mt-2"><HourglassIcon className="w-4 h-4 mr-1"/>SLA Incumplido</div>}
        </div>
    );
};

const TicketKanbanView: React.FC<{ tickets: Ticket[], customers: Customer[], setTickets: React.Dispatch<React.SetStateAction<Ticket[]>>, onSelectTicket: (t: Ticket) => void }> = ({ tickets, customers, setTickets, onSelectTicket }) => {
    const handleDrop = (e: React.DragEvent<HTMLDivElement>, stageId: TicketStatus) => {
        const ticketId = e.dataTransfer.getData('ticketId');
        setTickets(prev => prev.map(t => t.id === ticketId ? { ...t, status: stageId } : t));
    };
    return (
        <div className="flex-1 px-8 pb-8 overflow-x-auto"><div className="flex space-x-6 min-w-max h-full">
            {ticketStages.map(stage => (<div key={stage.id} className="w-80 bg-secondary rounded-xl flex flex-col h-full" onDrop={(e) => handleDrop(e, stage.id)} onDragOver={e => e.preventDefault()}>
                <div className={`p-4 border-b`}><h4 className="font-bold text-foreground">{stage.title}</h4></div>
                <div className="p-4 space-y-4 overflow-y-auto flex-1">
                    {tickets.filter(t => t.status === stage.id).map(ticket => (
                        <div key={ticket.id} draggable onDragStart={(e) => e.dataTransfer.setData('ticketId', ticket.id)}>
                            <TicketCard ticket={ticket} customer={customers.find(c => c.id === ticket.customerId)} onSelect={() => onSelectTicket(ticket)} />
                        </div>
                    ))}
                </div>
            </div>))}
        </div></div>
    );
};

const KnowledgeBase: React.FC = () => (
    <div className="p-8 space-y-6">
        <div className="flex justify-between items-center"><button className="flex items-center space-x-2 bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90"><PlusIcon className="w-5 h-5"/><span>Nuevo Artículo</span></button></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockKbArticles.map(article => (<div key={article.id} className="bg-card p-4 rounded-lg hover:bg-muted cursor-pointer border shadow-sm"><span className="text-xs bg-accent text-accent-foreground px-2 py-1 rounded-full">{article.category}</span><h4 className="font-bold mt-2">{article.title}</h4><p className="text-sm text-muted-foreground mt-1">{article.excerpt}</p></div>))}
        </div>
    </div>
);

const LiveChannels: React.FC = () => (
    <div className="p-8 space-y-6">
        <div className="bg-card p-4 rounded-lg border shadow-sm">
            <h4 className="font-semibold mb-2">Chats Entrantes</h4>
            <div className="space-y-3">
                <div className="bg-muted p-3 rounded-lg flex justify-between items-center">
                    <div>
                        <p className="font-bold">Cliente Anónimo (Chat Web)</p>
                        <p className="text-sm text-muted-foreground">"Hola, tengo una pregunta sobre mi pedido..."</p>
                    </div>
                    <button className="bg-primary text-primary-foreground px-3 py-1 rounded-md text-sm">Crear Ticket</button>
                </div>
                 <div className="bg-muted p-3 rounded-lg flex justify-between items-center">
                    <div>
                        <p className="font-bold">Laura (WhatsApp)</p>
                        <p className="text-sm text-muted-foreground">"¿Pueden enviarme el manual de usuario?"</p>
                    </div>
                    <button className="bg-primary text-primary-foreground px-3 py-1 rounded-md text-sm">Crear Ticket</button>
                </div>
            </div>
        </div>
    </div>
);

const SupportCenter: React.FC<{ tickets: Ticket[], customers: Customer[], setTickets: React.Dispatch<React.SetStateAction<Ticket[]>>, onSelectTicket: (t: Ticket) => void }> = ({ tickets, customers, setTickets, onSelectTicket }) => {
    const [view, setView] = useState<'dashboard'|'tickets'|'kb'|'live'>('dashboard');
    const [ticketView, setTicketView] = useState<'kanban'|'list'>('kanban');

    const renderTicketView = () => {
        if (ticketView === 'kanban') return <TicketKanbanView tickets={tickets} customers={customers} setTickets={setTickets} onSelectTicket={onSelectTicket} />;
        return <p className="p-8 text-muted-foreground">Vista de lista de tickets próximamente.</p>;
    };

    return (
        <div className="h-full flex flex-col">
            <header className="px-6 pt-6">
                <nav className="flex space-x-2">
                    <button onClick={() => setView('dashboard')} className={`px-4 py-2 rounded-md ${view === 'dashboard' ? 'bg-accent text-accent-foreground' : 'text-muted-foreground'}`}>Dashboard</button>
                    <button onClick={() => setView('tickets')} className={`px-4 py-2 rounded-md ${view === 'tickets' ? 'bg-accent text-accent-foreground' : 'text-muted-foreground'}`}>Tickets</button>
                     <button onClick={() => setView('live')} className={`px-4 py-2 rounded-md ${view === 'live' ? 'bg-accent text-accent-foreground' : 'text-muted-foreground'}`}>Canales en Vivo</button>
                    <button onClick={() => setView('kb')} className={`px-4 py-2 rounded-md ${view === 'kb' ? 'bg-accent text-accent-foreground' : 'text-muted-foreground'}`}>Base de Conocimientos</button>
                </nav>
            </header>
            <main className="flex-1 overflow-auto">
                {view === 'dashboard' && <SupportDashboard tickets={tickets} />}
                {view === 'tickets' && (
                    <div>
                        <div className="px-8 py-6 flex justify-end items-center">
                            <div className="flex items-center space-x-2 bg-card p-1 rounded-lg">
                               <button onClick={() => setTicketView('kanban')} className={`p-1 rounded-md ${ticketView === 'kanban' ? 'bg-primary text-primary-foreground' : ''}`}><KanbanIcon className="w-5 h-5"/></button>
                               <button onClick={() => setTicketView('list')} className={`p-1 rounded-md ${ticketView === 'list' ? 'bg-primary text-primary-foreground' : ''}`}><ListIcon className="w-5 h-5"/></button>
                            </div>
                        </div>
                        {renderTicketView()}
                    </div>
                )}
                {view === 'live' && <LiveChannels />}
                {view === 'kb' && <KnowledgeBase />}
            </main>
        </div>
    );
};

// --- SLIDE-OUT PANELS ---
const CustomerDetailPanel: React.FC<{ customer: Customer | null; onClose: () => void, onSelectTicket: (t: Ticket) => void, onUpdateQuote: (customerId: number, quoteId: string, newQuote: Partial<Quote>) => void }> = ({ customer, onClose, onSelectTicket, onUpdateQuote }) => {
    if (!customer) return null;
    const [tab, setTab] = useState('activity');
    return (
        <div className="fixed inset-0 bg-black/60 z-40" onClick={onClose}><div className="fixed top-0 right-0 h-full w-full max-w-2xl bg-background shadow-2xl z-50 flex flex-col border-l" onClick={e => e.stopPropagation()}>
            {/* Header */}
            <div className="p-6 border-b flex justify-between items-start">
                <div><div className="flex items-center space-x-4"><img src={customer.avatarUrl} alt={customer.name} className="w-16 h-16 rounded-full" /><div><h3 className="text-2xl font-bold text-foreground">{customer.name}</h3><p className="text-muted-foreground">{customer.company}</p></div></div><div className="flex flex-wrap gap-2 mt-4">{customer.tags.map(tag => <span key={tag} className="px-2 py-1 text-xs bg-accent text-accent-foreground rounded-full">{tag}</span>)}</div></div>
                <button onClick={onClose} className="p-2 rounded-full hover:bg-muted"><XMarkIcon className="w-6 h-6" /></button>
            </div>
            {/* Tabs */}
            <div className="border-b px-6"><nav className="flex space-x-4">
                <button onClick={() => setTab('activity')} className={`py-3 px-1 border-b-2 ${tab==='activity'?'border-primary text-foreground':'border-transparent text-muted-foreground'}`}>Actividad</button>
                <button onClick={() => setTab('quotes')} className={`py-3 px-1 border-b-2 ${tab==='quotes'?'border-primary text-foreground':'border-transparent text-muted-foreground'}`}>Cotizaciones</button>
                <button onClick={() => setTab('support')} className={`py-3 px-1 border-b-2 ${tab==='support'?'border-primary text-foreground':'border-transparent text-muted-foreground'}`}>Soporte ({customer.tickets.length})</button>
            </nav></div>
            {/* Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {tab === 'activity' && <div><h4 className="font-semibold mb-4">Línea de Tiempo de Actividad</h4></div>}
                {tab === 'quotes' && <div><h4 className="font-semibold mb-4">Cotizaciones</h4><div className="space-y-3">{customer.quotes.map(q => <div key={q.id} className="bg-muted p-3 rounded-lg flex justify-between items-center"><div><p className="font-bold">{q.number}</p><p className="text-sm text-muted-foreground">€{q.amount.toLocaleString()} - <span className="capitalize">{q.status}</span></p></div> {q.paid ? (<span className="flex items-center text-sm text-green-500"><InvoiceIcon className="w-4 h-4 mr-1"/>Pagado</span>) : q.status === 'accepted' ? (<button onClick={() => onUpdateQuote(customer.id, q.id, { paid: true })} className="bg-green-600 text-xs px-2 py-1 rounded-md text-white">Marcar como Pagado</button>) : null} </div>)}</div></div>}
                {tab === 'support' && <div><h4 className="font-semibold mb-4">Historial de Soporte</h4><div className="space-y-2">{customer.tickets.map(t => (<div key={t.id} onClick={() => onSelectTicket(t)} className="bg-muted p-3 rounded-lg cursor-pointer hover:bg-accent"><p className="font-bold">{t.subject}</p><p className="text-sm text-muted-foreground">#{t.id} - <span className="capitalize">{t.status}</span></p></div>))}</div></div>}
            </div>
        </div></div>
    );
};

const TicketDetailPanel: React.FC<{ ticket: Ticket | null, customers: Customer[], onClose: () => void, onUpdateTicket: (id: string, newTicket: Partial<Ticket>) => void }> = ({ ticket, customers, onClose, onUpdateTicket }) => {
    if (!ticket) return null;
    const customer = customers.find(c => c.id === ticket.customerId);
    const handleSetRating = (rating: number) => { onUpdateTicket(ticket.id, { satisfactionRating: rating }); };
    return (
        <div className="fixed inset-0 bg-black/60 z-40" onClick={onClose}><div className="fixed top-0 right-0 h-full w-full max-w-2xl bg-background shadow-2xl z-50 flex flex-col border-l" onClick={e => e.stopPropagation()}>
            <div className="p-6 border-b flex justify-between items-start">
                <div><h3 className="text-2xl font-bold text-foreground">Ticket #{ticket.id}</h3><p className="text-muted-foreground">{ticket.subject}</p></div>
                <button onClick={onClose} className="p-2 rounded-full hover:bg-muted"><XMarkIcon className="w-6 h-6" /></button>
            </div>
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                <div className="grid grid-cols-2 gap-4">
                    <div><p className="text-sm text-muted-foreground">Cliente</p><p>{customer?.name}</p></div>
                    <div><p className="text-sm text-muted-foreground">Asignado a</p><p>{sellers.find(s=>s.id === ticket.assigneeId)?.name || 'Sin asignar'}</p></div>
                    <div><p className="text-sm text-muted-foreground">Prioridad</p><p className="capitalize">{ticket.priority}</p></div>
                    <div><p className="text-sm text-muted-foreground">Estado</p><p className="capitalize">{ticket.status}</p></div>
                </div>
                 {ticket.status === 'resolved' && (
                    <div className="bg-muted p-4 rounded-lg">
                        <h4 className="font-semibold mb-2">Satisfacción del Cliente</h4>
                        <div className="flex items-center space-x-1">{[1,2,3,4,5].map(star => <button key={star} onClick={() => handleSetRating(star)}><StarIcon className={`w-6 h-6 ${ticket.satisfactionRating && star <= ticket.satisfactionRating ? 'text-yellow-400' : 'text-gray-600'}`} /></button>)}</div>
                    </div>
                )}
                <div><h4 className="font-semibold mb-2">Conversación</h4><div className="space-y-4">{ticket.conversation.map(msg => (<div key={msg.id} className="flex space-x-3"><img src={msg.authorAvatarUrl || customer?.avatarUrl} className="w-8 h-8 rounded-full"/><div className="bg-muted p-3 rounded-lg flex-1"><p className="text-sm">{msg.text}</p><p className="text-xs text-muted-foreground text-right">{new Date(msg.timestamp).toLocaleString()}</p></div></div>))}</div></div>
            </div>
            <div className="p-4 border-t flex items-center space-x-2">
                <textarea className="flex-1 bg-input rounded-lg p-2 border" placeholder="Escribe una respuesta..."></textarea>
                <button className="bg-primary text-primary-foreground p-2 rounded-lg"><PaperAirplaneIcon className="w-5 h-5"/></button>
                <button className="bg-secondary p-2 rounded-lg"><ArchiveBoxIcon className="w-5 h-5"/></button>
            </div>
        </div></div>
    );
};

// --- MAIN COMPONENT ---
const Level2_Responses: React.FC = () => {
    type MainView = 'dashboard' | 'pipeline' | 'contacts' | 'support' | 'integrations';
    const [view, setView] = useState<MainView>('dashboard');
    const [customers, setCustomers] = useState<Customer[]>(initialCustomers);
    const [tickets, setTickets] = useState<Ticket[]>(initialTickets);
    const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
    const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);

    const navItems = [
        { id: 'dashboard', label: 'Dashboard', icon: DashboardIcon },
        { id: 'pipeline', label: 'Pipeline', icon: PipelineIcon },
        { id: 'contacts', label: 'Contactos', icon: ContactsIcon },
        { id: 'support', label: 'Soporte', icon: SupportIcon },
        { id: 'integrations', label: 'Integraciones', icon: TargetIcon },
    ];
    
    const handleSelectTicket = (ticket: Ticket) => {
        setSelectedCustomer(null);
        setSelectedTicket(ticket);
    };

    const handleUpdateTicket = (id: string, newTicket: Partial<Ticket>) => {
        setTickets(prev => prev.map(t => t.id === id ? { ...t, ...newTicket } : t));
    };

    const handleUpdateQuote = (customerId: number, quoteId: string, newQuote: Partial<Quote>) => {
        setCustomers(prev => prev.map(c => 
            c.id === customerId 
            ? { ...c, quotes: c.quotes.map(q => q.id === quoteId ? {...q, ...newQuote} : q) } 
            : c
        ));
    };

    const renderContent = () => {
        switch(view) {
            case 'pipeline': return <PipelineView customers={customers} setCustomers={setCustomers} onSelectCustomer={setSelectedCustomer} />;
            case 'contacts': return <ContactListView customers={customers} onSelectCustomer={setSelectedCustomer} />;
            case 'support': return <SupportCenter tickets={tickets} customers={customers} setTickets={setTickets} onSelectTicket={handleSelectTicket} />;
            case 'integrations': return <LeadCaptureView />;
            case 'dashboard': default: return <Dashboard customers={customers} tickets={tickets} />;
        }
    };

    return (
         <div className="h-full flex text-foreground">
            {/* Dedicated Side Navigation */}
            <nav className="w-60 bg-card p-4 border-r flex flex-col">
                <ul className="space-y-1">
                    {navItems.map(item => (
                        <li key={item.id}>
                            <button
                                onClick={() => setView(item.id as MainView)}
                                className={`w-full flex justify-between items-center p-3 rounded-lg transition-colors duration-200 ${
                                    view === item.id
                                        ? 'bg-accent text-accent-foreground font-semibold'
                                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                                }`}
                            >
                                <div className="flex items-center space-x-3">
                                    <item.icon className="w-5 h-5" />
                                    <span>{item.label}</span>
                                </div>
                                {view === item.id && <div className="w-2 h-2 bg-primary rounded-full"></div>}
                            </button>
                        </li>
                    ))}
                </ul>
            </nav>

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col overflow-hidden">
                <div className="p-4 border-b flex justify-between items-center h-[65px] flex-shrink-0">
                     <div></div>
                    <div className="flex items-center space-x-4">
                        <div className="relative flex items-center">
                            <SearchIcon className="w-5 h-5 absolute left-3 text-muted-foreground" />
                            <input type="text" placeholder="Buscar..." className="bg-input rounded-md py-2 pl-10 pr-4 w-64 text-foreground placeholder-muted-foreground" />
                        </div>
                        <button className="flex items-center space-x-2 bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors">
                            <PlusIcon className="w-5 h-5"/> 
                            <span className="font-semibold">Añadir Lead</span>
                        </button>
                    </div>
                </div>
                <main className="flex-1 overflow-auto">
                    {renderContent()}
                </main>
            </div>

            {/* Slide-out Panels */}
            <CustomerDetailPanel customer={selectedCustomer} onClose={() => setSelectedCustomer(null)} onSelectTicket={handleSelectTicket} onUpdateQuote={handleUpdateQuote} />
            <TicketDetailPanel ticket={selectedTicket} customers={customers} onClose={() => setSelectedTicket(null)} onUpdateTicket={handleUpdateTicket} />
        </div>
    );
};

export default Level2_Responses;
