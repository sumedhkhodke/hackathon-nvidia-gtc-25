import React, { useEffect } from 'react';

export const Architecture: React.FC = () => {
  useEffect(() => {
    // Initialize Mermaid when component mounts
    if (window.mermaid) {
      window.mermaid.initialize({ startOnLoad: false, theme: 'default' });
      window.mermaid.init(undefined, document.querySelectorAll('.mermaid'));
    }
  }, []);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">🏗️ Multi-Agent Architecture</h2>
      
      <p className="text-gray-700 mb-6">
        This system implements a sophisticated <strong>multi-agent architecture</strong> using NVIDIA Nemotron models, 
        orchestrated by LangGraph to demonstrate advanced agentic AI capabilities for the <strong>NVIDIA GTC Hackathon 2025</strong>.
        Background Analysis & Coaching agents process historical data asynchronously to provide KPI-driven insights to the ReAct workflow.
      </p>

      <div className="bg-white rounded-lg shadow p-4 mb-8">
        <pre className='mermaid' style={{ minHeight: '520px' }}>
{`flowchart LR
    classDef ioNode fill:#ffe0e0,stroke:#d32f2f,stroke-width:2px;

    Question([User question]):::ioNode --> SafetyIn

    subgraph System["Agentic Insight Pipeline"]
        subgraph Capture["1. Capture & Store"]
            UserData[User data streams] --> Normalize[Normalize & tag]
            Normalize --> VectorDB[Vector DB]
            Normalize --> Metadata[Metadata]
        end

        subgraph Background["2. Background Analysis"]
            VectorDB --> AnalysisAgent[Analysis agent]
            Metadata --> AnalysisAgent
            AnalysisAgent --> KPIStore[KPI store]
            KPIStore --> CoachAgent[Coach agent]
            CoachAgent --> InsightsCache[Insights cache]
        end

        subgraph Conversation["3. Conversational Coach"]
            SafetyIn --> Orchestrator[ReAct orchestrator]
            Orchestrator --> Retrieval[Search vector DB]
            Retrieval --> Orchestrator
            Orchestrator --> InsightsTool[Query insights cache]
            InsightsTool --> Orchestrator
            Orchestrator --> Synthesis[Synthesize answer]
            Synthesis --> SafetyOut[Safety check out]
        end
    end

    VectorDB -.-> Retrieval
    InsightsCache -.-> InsightsTool

    SafetyOut --> Response([Coach response]):::ioNode`}
        </pre>
      </div>

      <script src='https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'></script>
    </div>
  );
};
