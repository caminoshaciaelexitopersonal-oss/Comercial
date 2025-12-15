
import React, { createContext, useContext, useState, useCallback, useMemo, useEffect, PropsWithChildren } from 'react';
import { initialAllData, createDefaultFunnel } from '../components/funnel-builder/data';
import type { Funnel, Block, LandingPage, Categoria, Subcategoria, CadenaTurismo, Asset } from '../types';

type AllData = typeof initialAllData;

// --- HISTORY HOOK for Undo/Redo ---
function useHistoryState<T>(initialState: T) {
    const [history, setHistory] = useState([initialState]);
    const [pointer, setPointer] = useState(0);

    const state = history[pointer];

    const setState = useCallback((newState: T | ((prevState: T) => T), fromHistory = false) => {
        const resolvedState = typeof newState === 'function' ? (newState as (prevState: T) => T)(state) : newState;
        if (!fromHistory && JSON.stringify(resolvedState) === JSON.stringify(state)) return; 
        
        const newHistory = history.slice(0, pointer + 1);
        newHistory.push(resolvedState);
        setHistory(newHistory);
        setPointer(newHistory.length - 1);
    }, [history, pointer, state]);

    const undo = useCallback(() => { if (pointer > 0) setPointer(p => p - 1); }, [pointer]);
    const redo = useCallback(() => { if (pointer < history.length - 1) setPointer(p => p + 1); }, [pointer, history.length]);

    return { state, setState, undo, redo, canUndo: pointer > 0, canRedo: pointer < history.length - 1 };
}


interface FunnelBuilderContextType {
    // State & History
    allData: AllData;
    updateData: (updater: (draft: AllData) => void | any) => void;
    undo: () => void;
    redo: () => void;
    canUndo: boolean;
    canRedo: boolean;
    saveStatus: 'saved' | 'saving' | 'error';

    // Active Selections
    activeCadenaId: string | null;
    setActiveCadenaId: (id: string | null) => void;
    activeCategoriaId: string | null;
    setActiveCategoriaId: (id: string | null) => void;
    activeSubcategoriaId: string | null;
    setActiveSubcategoriaId: (id: string | null) => void;
    activeLandingPageId: string | null;
    setActiveLandingPageId: (id: string | null) => void;
    activeFunnelId: string | null;
    setActiveFunnelId: (id: string | null) => void;
    activePageId: string | null;
    setActivePageId: (id: string | null) => void;
    activeBlockId: string | null;
    setActiveBlockId: (id: string | null) => void;
    
    // Derived Active Items
    activeCadena: CadenaTurismo | undefined;
    activeLandingPage: LandingPage | undefined;
    activeFunnel: Funnel | undefined;
    activePage: any | undefined; // FunnelPage is complex to derive here
    activeBlock: Block | undefined;

    // Filtered lists
    filteredCategorias: Categoria[];
    filteredSubcategorias: Subcategoria[];
    filteredLandingPages: LandingPage[];

    // UI State
    isCreateFunnelModalOpen: boolean;
    setIsCreateFunnelModalOpen: (isOpen: boolean) => void;
    isMediaLibraryOpen: boolean;
    setIsMediaLibraryOpen: (isOpen: boolean) => void;
    mediaLibraryCallback: ((url: string) => void) | null;
    setMediaLibraryCallback: (cb: ((url: string) => void) | null) => void;
    activeBreakpoint: 'desktop' | 'tablet' | 'mobile';
    setActiveBreakpoint: (bp: 'desktop' | 'tablet' | 'mobile') => void;
    
    // Actions
    handleCreateFunnel: (name: string) => void;
}

const FunnelBuilderContext = createContext<FunnelBuilderContextType | undefined>(undefined);

export const FunnelBuilderProvider: React.FC<PropsWithChildren<{}>> = ({ children }) => {
    const { state: allData, setState: setAllData, undo, redo, canUndo, canRedo } = useHistoryState(initialAllData);
    
    const [activeCadenaId, setActiveCadenaId] = useState<string | null>(null);
    const [activeCategoriaId, setActiveCategoriaId] = useState<string | null>(null);
    const [activeSubcategoriaId, setActiveSubcategoriaId] = useState<string | null>(null);
    const [activeLandingPageId, setActiveLandingPageId] = useState<string | null>(null);
    const [activeFunnelId, setActiveFunnelId] = useState<string | null>(null);
    const [activePageId, setActivePageId] = useState<string | null>(null);
    const [activeBlockId, setActiveBlockId] = useState<string | null>(null);

    const [isCreateFunnelModalOpen, setIsCreateFunnelModalOpen] = useState(false);
    const [isMediaLibraryOpen, setIsMediaLibraryOpen] = useState(false);
    const [mediaLibraryCallback, setMediaLibraryCallback] = useState<((url: string) => void) | null>(null);
    const [activeBreakpoint, setActiveBreakpoint] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');
    const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'error'>('saved');

    useEffect(() => {
        const handler = setTimeout(() => { setSaveStatus('saved'); }, 1000);
        return () => clearTimeout(handler);
    }, [allData]);

    const updateData = (updater: (draft: AllData) => void | any) => {
        const newState = JSON.parse(JSON.stringify(allData));
        const potentialReturnValue = updater(newState);
        if (potentialReturnValue) {
            setAllData(potentialReturnValue);
        } else {
            setAllData(newState);
        }
        setSaveStatus('saving');
    };

    // Auto-load default view
    useEffect(() => {
        if (allData.cadenas.length > 0 && !activeCadenaId) {
            const cadenaToLoad = allData.cadenas[0]!;
            const catToLoad = allData.categorias.find(c => c.cadenaId === cadenaToLoad.id);
            const subToLoad = catToLoad ? allData.subcategorias.find(s => s.categoriaId === catToLoad.id) : undefined;
            const lpToLoad = subToLoad ? allData.landingPages.find(l => l.subcategoriaId === subToLoad.id) : undefined;
            const funnelToLoad = lpToLoad?.funnels[0];

            setActiveCadenaId(cadenaToLoad.id);
            if (catToLoad) setActiveCategoriaId(catToLoad.id);
            if (subToLoad) setActiveSubcategoriaId(subToLoad.id);
            if (lpToLoad) setActiveLandingPageId(lpToLoad.id);
            if (funnelToLoad) {
                setActiveFunnelId(funnelToLoad.id);
                setActivePageId(funnelToLoad.pages[0]?.id || null);
            }
        }
    }, [allData, activeCadenaId]);

    // Derived values
    const activeCadena = useMemo(() => allData.cadenas.find(c => c.id === activeCadenaId), [allData.cadenas, activeCadenaId]);
    const filteredCategorias = useMemo(() => allData.categorias.filter(c => c.cadenaId === activeCadenaId), [allData.categorias, activeCadenaId]);
    const filteredSubcategorias = useMemo(() => activeCategoriaId ? allData.subcategorias.filter(s => s.categoriaId === activeCategoriaId) : [], [allData.subcategorias, activeCategoriaId]);
    const filteredLandingPages = useMemo(() => activeSubcategoriaId ? allData.landingPages.filter(lp => lp.subcategoriaId === activeSubcategoriaId) : [], [allData.landingPages, activeSubcategoriaId]);
    
    const activeLandingPage = useMemo(() => allData.landingPages.find(lp => lp.id === activeLandingPageId), [allData.landingPages, activeLandingPageId]);
    const activeFunnel = useMemo(() => activeLandingPage?.funnels.find(f => f.id === activeFunnelId), [activeLandingPage, activeFunnelId]);
    const activePage = useMemo(() => activeFunnel?.pages.find(p => p.id === activePageId), [activeFunnel, activePageId]);
    const activeBlock = useMemo(() => activePage?.blocks.find(b => b.id === activeBlockId), [activePage, activeBlockId]);

    const handleCreateFunnel = (newFunnelName: string) => {
        if (!newFunnelName.trim() || !activeLandingPageId) return;
        const newFunnel = createDefaultFunnel(activeLandingPageId, newFunnelName);
        updateData(draft => {
            const lp = draft.landingPages.find(l => l.id === activeLandingPageId);
            if (lp) lp.funnels.push(newFunnel);
        });
        setActiveFunnelId(newFunnel.id);
        setActivePageId(newFunnel.pages[0].id);
        setIsCreateFunnelModalOpen(false);
    };

    const value: FunnelBuilderContextType = {
        allData, updateData, undo, redo, canUndo, canRedo, saveStatus,
        activeCadenaId, setActiveCadenaId,
        activeCategoriaId, setActiveCategoriaId,
        activeSubcategoriaId, setActiveSubcategoriaId,
        activeLandingPageId, setActiveLandingPageId,
        activeFunnelId, setActiveFunnelId,
        activePageId, setActivePageId,
        activeBlockId, setActiveBlockId,
        activeCadena, activeLandingPage, activeFunnel, activePage, activeBlock,
        filteredCategorias, filteredSubcategorias, filteredLandingPages,
        isCreateFunnelModalOpen, setIsCreateFunnelModalOpen,
        isMediaLibraryOpen, setIsMediaLibraryOpen,
        mediaLibraryCallback, setMediaLibraryCallback,
        activeBreakpoint, setActiveBreakpoint,
        handleCreateFunnel
    };

    return <FunnelBuilderContext.Provider value={value}>{children}</FunnelBuilderContext.Provider>;
};

export const useFunnelBuilder = () => {
    const context = useContext(FunnelBuilderContext);
    if (context === undefined) {
        throw new Error('useFunnelBuilder must be used within a FunnelBuilderProvider');
    }
    return context;
};
