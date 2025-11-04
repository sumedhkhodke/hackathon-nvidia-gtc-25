// Chat related types
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  reasoning_steps?: ReasoningStep[];
  safety_checks?: SafetyCheck[];
  metrics?: {
    react_cycles?: number;
    retrieved_entries?: number;
    elapsed_time?: number;
  };
}

export interface ReasoningStep {
  step: string;
  description: string;
}

export interface SafetyCheck {
  type: string;
  is_safe: boolean;
  category?: string;
  should_block?: boolean;
  needs_modification?: boolean;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface ChatResponse {
  success: boolean;
  response: string;
  reasoning_steps: ReasoningStep[];
  safety_checks: SafetyCheck[];
  react_cycles: number;
  retrieved_entries: number;
  elapsed_time: number;
  error?: string;
}

// WebSocket message types
export interface WSMessage {
  type: 'intermediate' | 'final' | 'error';
  content?: string;
  reasoning_step?: ReasoningStep;
  metrics?: {
    react_cycles?: number;
    retrieved_entries?: number;
    elapsed_time?: number;
  };
}

// Data related types
export interface SystemStats {
  total_entries: number;
  collection_name: string;
  status: string;
}

export interface LifelogEntry {
  date: string;
  category: string;
  entry: string;
  mood_score: number;
}

export interface CategorySummary {
  category: string;
  average_score: number;
  entry_count: number;
  min_score: number;
  max_score: number;
}

export interface DataInsights {
  total_entries: number;
  date_range: {
    start: string;
    end: string;
  };
  overall_average_score: number;
  category_summaries: CategorySummary[];
}

export interface CorrelationData {
  categories: string[];
  correlation_matrix: (number | null)[][];
}

// System related types
export interface AgentInfo {
  name: string;
  model: string;
  description: string;
  icon: string;
  status: 'active' | 'inactive';
}

export interface SystemArchitecture {
  title: string;
  description: string;
  components: Record<string, {
    title: string;
    items: string[];
  }>;
  workflow: Record<string, string>;
  tech_stack: Record<string, string[]>;
}

// Chart data types
export interface TimelineDataPoint {
  date: string;
  category: string;
  mood_score: number;
  entry: string;
}

// Re-export all types explicitly
export type {
  ChatMessage as ChatMessageType,
  ReasoningStep as ReasoningStepType,
  SafetyCheck as SafetyCheckType,
};