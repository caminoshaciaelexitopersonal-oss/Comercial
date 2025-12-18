
import axios from 'axios';
import { Opportunity } from '../types'; // Assuming Opportunity will be defined in types.ts

const API_URL = '/api/sales';

export const getOpportunities = async (): Promise<Opportunity[]> => {
    const response = await axios.get(`${API_URL}/opportunities/`);
    return response.data;
};

export const moveOpportunity = async (opportunityId: number, stage: string): Promise<Opportunity> => {
    const response = await axios.post(`${API_URL}/opportunities/${opportunityId}/move/`, { stage });
    return response.data;
};
