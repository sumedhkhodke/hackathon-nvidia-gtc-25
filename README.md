# Agentic Lifelog · Personal AI Coach

[![NVIDIA GTC 2025](https://img.shields.io/badge/NVIDIA%20GTC-2025-76B900?style=flat&logo=nvidia)](https://www.nvidia.com/
gtc/)
[![Nemotron Prize Track](https://img.shields.io/badge/Prize%20Track-Nemotron-76B900?style=flat)](https://www.nvidia.com/
en-us/ai/)

- **Mission** – Deliver a privacy-first personal intelligence layer that converts quantified-self data into actionable coaching, as framed in `docs/project-outline.md`.
- **Problem** – Individuals drown in siloed sleep, mood, and productivity logs that lack synthesis; the platform unifies them into a trusted narrative.
- **Solution** – LangGraph orchestrates Nemotron agents (reasoning, safety, retrieval) running on NVIDIA NIM, mirroring the data and control paths in `docs/project-diagram.md`.
- **Safety & Privacy** – Dual Nemotron Safety Guard checkpoints moderate every input/output and keep sensitive data local-first with encrypted storage.
- **Nemotron & NIM Alignment** – Showcases Super 49B for reasoning, Nano 9B for fast tool use, and Guard 8B for policy enforcement, highlighting NVIDIA GTC Nemotron track goals.
- **Current Status** – Streamlit UI, lifelog store, and iterative ReAct loop are MVP-complete; backlog includes multimodal ingestion and proactive insights.
- **Resources** – Architecture blueprint and latest diagrams live in `docs/project-outline.md` and `docs/project-diagram.md`.

## Architecture Diagram
```mermaid
flowchart LR
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

    SafetyOut --> Response([Coach response]):::ioNode
```

## Get Started
1. Clone: `git clone https://github.com/yourusername/hackathon-nvidia-gtc-25.git && cd hackathon-nvidia-gtc-25`
2. Install Python 3.10+ deps: `pip install .` (or `pip install -e .[dev]` for tooling).
3. Configure credentials: `cp env.example .env` and add `NVIDIA_API_KEY` plus any data source secrets.
4. Launch the demo: `streamlit run app.py`
5. Optional smoke tests: `python src/agents.py` and `python src/agentic_workflow.py`

## Notes
- Sample lifelog data sits in `data/sample_lifelog.csv` for quick experimentation.
- Update `.streamlit/secrets.toml` or `.env` before connecting to live NVIDIA NIM endpoints.
- See `uv.lock` if you prefer `uv sync` to mirror the locked dependency set.
