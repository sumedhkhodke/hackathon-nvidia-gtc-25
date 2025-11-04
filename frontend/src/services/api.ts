import axios from 'axios';
import type {
  ChatRequest,
  ChatResponse,
  ChatMessage,
  SystemStats,
  LifelogEntry,
  DataInsights,
  CorrelationData,
  AgentInfo,
  SystemArchitecture,
  TimelineDataPoint
} from '../types/index';

const API_BASE_URL = 'http://localhost:8000';
const WS_BASE_URL = 'ws://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatApi = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/api/chat/message', request);
    return response.data;
  },

  getHistory: async (limit?: number): Promise<ChatMessage[]> => {
    const response = await api.get<ChatMessage[]>('/api/chat/history', {
      params: { limit },
    });
    return response.data;
  },

  clearHistory: async (): Promise<void> => {
    await api.delete('/api/chat/history');
  },

  getWebSocketUrl: (): string => {
    return `${WS_BASE_URL}/ws/chat`;
  },
};

// Data API
export const dataApi = {
  getStats: async (): Promise<SystemStats> => {
    const response = await api.get<SystemStats>('/api/data/stats');
    return response.data;
  },

  getEntries: async (
    limit?: number,
    offset?: number,
    category?: string
  ): Promise<LifelogEntry[]> => {
    const response = await api.get<LifelogEntry[]>('/api/data/entries', {
      params: { limit, offset, category },
    });
    return response.data;
  },

  getInsights: async (): Promise<DataInsights> => {
    const response = await api.get<DataInsights>('/api/data/insights');
    return response.data;
  },

  getCorrelations: async (): Promise<CorrelationData> => {
    const response = await api.get<CorrelationData>('/api/data/correlations');
    return response.data;
  },

  getTimeline: async (category?: string): Promise<{ data: TimelineDataPoint[] }> => {
    const response = await api.get<{ data: TimelineDataPoint[] }>('/api/data/timeline', {
      params: { category },
    });
    return response.data;
  },
};

// System API
export const systemApi = {
  getAgents: async (): Promise<AgentInfo[]> => {
    const response = await api.get<AgentInfo[]>('/api/system/agents');
    return response.data;
  },

  getArchitecture: async (): Promise<SystemArchitecture> => {
    const response = await api.get<SystemArchitecture>('/api/system/architecture');
    return response.data;
  },

  getFeatures: async (): Promise<{ features: Record<string, string> }> => {
    const response = await api.get<{ features: Record<string, string> }>('/api/system/features');
    return response.data;
  },

  getDemoQuestions: async (): Promise<{ questions: string[] }> => {
    const response = await api.get<{ questions: string[] }>('/api/system/demo-questions');
    return response.data;
  },
};

// Health check
export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await api.get('/health');
    return response.data.status === 'healthy';
  } catch {
    return false;
  }
};
