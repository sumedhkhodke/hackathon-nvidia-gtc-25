import { create } from 'zustand';
import type { ChatMessage, SystemStats } from '../types/index';
import { chatApi, dataApi } from '../services/api';

interface ChatStore {
  // State
  messages: ChatMessage[];
  isLoading: boolean;
  demoQuestion: string | null;
  stats: SystemStats | null;
  sidebarOpen: boolean;
  
  // Actions
  addMessage: (message: ChatMessage) => void;
  setMessages: (messages: ChatMessage[]) => void;
  clearMessages: () => void;
  setLoading: (loading: boolean) => void;
  setDemoQuestion: (question: string | null) => void;
  setStats: (stats: SystemStats) => void;
  setSidebarOpen: (open: boolean) => void;
  
  // Async actions
  sendMessage: (message: string) => Promise<void>;
  loadChatHistory: () => Promise<void>;
  loadStats: () => Promise<void>;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  // Initial state
  messages: [
    {
      role: 'assistant',
      content: `👋 **Hello! I'm your Agentic AI Coach.**

I can analyze your lifelog data using advanced multi-agent reasoning to provide deep insights about your:
- 😴 Sleep patterns and quality
- 🏃 Exercise habits and energy levels  
- 💼 Work productivity patterns
- 😊 Mood trends and correlations

**I use a sophisticated ReAct (Reasoning + Action) pattern with safety guardrails to ensure accurate, helpful, and safe responses.**

Try asking me a question, or click a demo button in the sidebar!`,
      timestamp: new Date(),
    }
  ],
  isLoading: false,
  demoQuestion: null,
  stats: null,
  sidebarOpen: true,

  // Actions
  addMessage: (message) => {
    set((state) => ({
      messages: [...state.messages, message],
    }));
  },

  setMessages: (messages) => {
    set({ messages });
  },

  clearMessages: async () => {
    set({ messages: [] });
    try {
      await chatApi.clearHistory();
    } catch (error) {
      console.error('Error clearing chat history:', error);
    }
  },

  setLoading: (loading) => {
    set({ isLoading: loading });
  },

  setDemoQuestion: (question) => {
    set({ demoQuestion: question });
  },

  setStats: (stats) => {
    set({ stats });
  },
  
  setSidebarOpen: (open) => {
    set({ sidebarOpen: open });
  },

  // Async actions
  sendMessage: async (message) => {
    const { addMessage, setLoading } = get();
    
    if (!message.trim() || get().isLoading) return;

    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    addMessage(userMessage);
    setLoading(true);

    try {
      const response = await chatApi.sendMessage({ message });
      
      if (response.success) {
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: response.response,
          timestamp: new Date(),
          reasoning_steps: response.reasoning_steps,
          safety_checks: response.safety_checks,
          metrics: {
            react_cycles: response.react_cycles,
            retrieved_entries: response.retrieved_entries,
            elapsed_time: response.elapsed_time,
          },
        };
        addMessage(assistantMessage);
      } else {
        throw new Error(response.error || 'Unknown error');
      }
    } catch (error) {
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: `❌ Sorry, I couldn't connect to the server. Please make sure the backend is running.`,
        timestamp: new Date(),
      };
      addMessage(errorMessage);
    } finally {
      setLoading(false);
    }
  },

  loadChatHistory: async () => {
    try {
      const history = await chatApi.getHistory();
      set({ messages: history });
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  },

  loadStats: async () => {
    try {
      const stats = await dataApi.getStats();
      set({ stats });
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  },
}));
