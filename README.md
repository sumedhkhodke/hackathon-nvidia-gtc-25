# 🧠 Agentic Lifelog - Personal AI Coach

> **Transform your personal data from noise into actionable insights using NVIDIA Nemotron models**

[![NVIDIA GTC 2025](https://img.shields.io/badge/NVIDIA%20GTC-2025-76B900?style=flat&logo=nvidia)](https://www.nvidia.com/gtc/)
[![Nemotron Prize Track](https://img.shields.io/badge/Prize%20Track-Nemotron-76B900?style=flat)](https://www.nvidia.com/en-us/ai/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 The Problem We're Solving

We live in the age of the **Quantified Self** - tracking sleep, fitness, mood, productivity. But all this data sits in silos, generating insights that are shallow or non-existent. We're **data-rich but insight-poor**.

**Agentic Lifelog** transforms this into the **Understood Self** - a privacy-first AI system that proactively analyzes your personal data using agentic reasoning to deliver truly personalized insights.

---

## ✨ What Makes This Different

### 🤖 True Agentic AI with ReAct Pattern
Not just a chatbot - a **multi-agent system** implementing **ReAct (Reasoning + Action)**:
- **Reasons** about queries using explicit planning
- **Acts** by retrieving data and executing tools
- **Observes** results and adapts iteratively
- **Synthesizes** insights through multi-step workflows
- **Transparently** shows every reasoning step

### 🛡️ Safety-First Design with Nemotron Guardrails
**Mandatory safety checkpoints** powered by Nemotron Safety Guard 8B v3:
- ✅ **Input Validation**: Every query checked before processing
- ✅ **Output Validation**: All AI responses validated before delivery
- ✅ **Content Moderation**: 23 unsafe categories monitored
- ✅ **Privacy Protection**: Medical/financial advice blocked
- ✅ **Crisis Detection**: Self-harm indicators flagged

### 🔒 Privacy-First Architecture
- All data processing can run **100% locally**
- No data ever sent to external servers (using NVIDIA NIM)
- Privacy-by-design, not privacy-by-policy
- AI-powered privacy guardrails actively protect user data

### 🎯 Specialized Nemotron Models
Each agent uses the right Nemotron model for its role (aligned with NVIDIA GTC 2025 Nemotron Prize Track):
- **Nemotron Super 49B v1.5**: ✅ Complex reasoning & synthesis
- **Nemotron Safety Guard 8B v3**: ✅ **NEW** - Safety & moderation
- **Nemotron Nano 9B v2**: ✅ Fast query analysis & tool use
- **Nemotron Nano VL 12B v2**: 📋 Multimodal data processing (planned for future iteration)

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.10+
- NVIDIA API Key ([Get one here](https://build.nvidia.com/))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/hackathon-nvidia-gtc-25.git
cd hackathon-nvidia-gtc-25

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
cp env.example .env
# Edit .env and add your NVIDIA_API_KEY

# 4. Run the application
streamlit run app.py
```

### Try It Out

Once running, ask questions like:
- *"What patterns do you see in my sleep quality over the past week?"*
- *"When do I feel most productive based on my logs?"*
- *"What might be contributing to my low mood scores recently?"*

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                    (Streamlit Chat App)                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LANGGRAPH ORCHESTRATOR                        │
│                  (Agentic Workflow Engine)                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Query        │ │ Data         │ │ Reasoning    │
    │ Analyzer     │ │ Retrieval    │ │ Synthesizer  │
    │ Agent        │ │ Agent        │ │ Agent        │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           │    ┌───────────▼─────────┐      │
           │    │   ChromaDB          │      │
           │    │   Vector Store      │      │
           │    └─────────────────────┘      │
           │                                 │
           └────────────┬────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────┐
        │  NVIDIA Nemotron Super 49B v1.5    │
        │  (via NVIDIA NIM API)              │
        └────────────────────────────────────┘
```

### Agentic Workflow with ReAct Pattern

```mermaid
graph LR
    A[User Query] --> B[🛡️ Safety Check]
    B --> C[🧠 ReAct Loop]
    C --> D[Reason]
    D --> E[Act]
    E --> F[Observe]
    F --> |Continue| D
    F --> |Sufficient| G[🎨 Synthesis]
    G --> H[🛡️ Output Check]
    H --> I[Response]
    
    style B fill:#FF6B6B
    style C fill:#76B900
    style D fill:#4ECDC4
    style E fill:#45B7D1
    style F fill:#FFA07A
    style G fill:#98D8C8
    style H fill:#FF6B6B
```

**Step-by-Step Process:**

1. **🛡️ Input Safety Check** (Nemotron Safety Guard 8B v3)
   - Validates user query for safety concerns
   - Blocks medical advice requests, self-harm indicators
   - Checks for privacy violations and malicious intent
   - Agent: SafetyGuardAgent

2. **🧠 ReAct Cycle** (Iterative Reasoning Loop, max 3 cycles)
   
   **Reason** - Planning Phase
   - Analyzes the query and current context
   - Reviews previous observations
   - Determines information gaps
   - Plans next action (data retrieval, search, analysis)
   - Agent: ReActAgent (Nemotron Super 49B)
   
   **Act** - Execution Phase
   - Executes planned action
   - Retrieves data from vector database
   - Calls external tools (future: web search)
   - Collects results
   - Store: ChromaDB with semantic search
   
   **Observe** - Reflection Phase
   - Analyzes action results
   - Determines if information is sufficient
   - Decides: Continue searching OR Synthesize answer
   - Updates context for next cycle
   - Agent: ReActAgent (Nemotron Super 49B)

3. **🎨 Response Synthesis** 
   - Synthesizes all gathered information
   - Identifies patterns and correlations
   - Generates actionable recommendations
   - Creates empathetic, personalized insights
   - Agent: ReasoningAgent (Nemotron Super 49B)

4. **🛡️ Output Safety Check** (Nemotron Safety Guard 8B v3)
   - Validates AI-generated response
   - Blocks medical diagnoses or financial predictions
   - Ensures no privacy violations or harmful content
   - Agent: SafetyGuardAgent

---

## 📁 Project Structure

```
hackathon-nvidia-gtc-25/
├── app.py                      # 🎯 MAIN ENTRY POINT - Streamlit UI
├── requirements.txt            # Python dependencies
├── .env                        # API keys (create from env.example)
├── README.md                   # This file
├── DEMO.md                     # Demo script for presentation
├── QUICK_START.md              # Detailed setup guide
│
├── src/
│   ├── __init__.py
│   ├── agents.py               # Nemotron agent implementations
│   ├── data_store.py           # ChromaDB vector store
│   └── agentic_workflow.py     # LangGraph orchestration
│
├── data/
│   └── sample_lifelog.csv      # Sample personal data (30+ entries)
│
└── erik/                       # Project planning docs
    ├── project-outline.md      # Full system blueprint
    ├── judging-criteria.md     # Hackathon criteria
    └── nemotron-prize-track.md # Track requirements
```

---

## 🛠️ Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Models** | NVIDIA Nemotron Super 49B v1.5 | Advanced reasoning & synthesis |
| **Safety Model** | Nemotron Safety Guard 8B v3 | Content moderation & safety |
| **API Access** | NVIDIA NIM API | Cloud inference endpoints |
| **Orchestration** | LangGraph | Multi-agent workflow with ReAct pattern |
| **Vector DB** | ChromaDB | Semantic search & embeddings |
| **Framework** | LangChain | AI application framework |
| **UI** | Streamlit | Interactive chat interface |
| **Data** | Pandas | Data manipulation |

---

## 🎯 Alignment with Judging Criteria

### 1. **Creativity** ⭐⭐⭐⭐⭐
- **Novel Problem**: Quantified Self → Understood Self
- **Innovative Approach**: Privacy-first agentic personal intelligence
- **Unique Architecture**: Multi-model specialization with Nemotron suite

### 2. **Functionality** ⭐⭐⭐⭐⭐
- ✅ Working end-to-end prototype
- ✅ Live demo with real queries
- ✅ Visible agent reasoning process
- ✅ Stable and reproducible

### 3. **Scope of Completion** ⭐⭐⭐⭐⭐
- ✅ MVP demonstrates core agentic workflow
- ✅ Clean, documented codebase
- ✅ Full architecture blueprint for scaling
- ✅ Clear roadmap to production

### 4. **Presentation** ⭐⭐⭐⭐⭐
- ✅ Clear problem statement
- ✅ Compelling live demo
- ✅ Architecture diagrams
- ✅ Technical depth with accessibility

### 5. **Use of NVIDIA Tools** ⭐⭐⭐⭐⭐
- ✅ NVIDIA NIM API integration
- ✅ Designed for NIM microservices deployment
- ✅ Ready for NVIDIA embedding models

### 6. **Use of NVIDIA Nemotron Models** ⭐⭐⭐⭐⭐
- ✅ **Primary**: Llama 3.3 Nemotron Super 49B for reasoning
- ✅ **Architecture**: Multi-model specialization design
- ✅ **Demonstrates**: Deep understanding of Nemotron capabilities
- ✅ **Showcases**: Agentic reasoning, tool use, RAG

---

## 🎬 Demo Script

See [DEMO.md](DEMO.md) for the complete presentation script with:
- 3 pre-tested questions
- Expected agent behaviors
- Talking points for each criterion
- Troubleshooting guide

### Sample Demo Flow

```
👤 User: "What patterns do you see in my sleep quality over the past week?"

🤖 Agent Reasoning:
  → Query Analysis: Extracting intent and search parameters
  → Data Retrieval: Searching vector database for relevant entries
  → Response Synthesis: Analyzing patterns with Nemotron

💡 Response:
"Based on your lifelog data, I've identified a strong correlation between 
your sleep quality and meeting density. On days with 4+ back-to-back meetings 
(Oct 23, 27, 28), your sleep quality averaged 2.3/5 with multiple wake-ups. 

In contrast, days with focused work blocks (Oct 22, 25, 26) showed 4.3/5 
sleep quality with minimal disruptions.

Recommendations:
1. Block 'meeting-free' days 2x per week
2. No meetings after 3pm on high-meeting days
3. Add 10-min buffer between meetings for mental recovery"
```

---

## 🚧 Current Implementation (MVP)

**Working Features:**
- ✅ **Nemotron API integration** (Super 49B + Safety Guard 8B v3)
- ✅ **ReAct Pattern Implementation** with iterative reasoning loops
- ✅ **Safety Guardrails** with input/output validation
- ✅ **Multi-agent orchestration** with LangGraph
- ✅ **Vector database** for semantic search (ChromaDB)
- ✅ **Interactive chat UI** with reasoning visibility and safety status
- ✅ **Sample lifelog data** (30+ entries)
- ✅ **Comprehensive test suite** (20+ test cases)

**Future Enhancements**:
- ⚠️ Web search integration in ReAct loop
- ⚠️ Multimodal data processing (Nemotron Nano VL)
- ⚠️ Real-time data ingestion
- ⚠️ Proactive insights and notifications
- ⚠️ Local NIM deployment
- ⚠️ Custom safety policy configuration

---

## 🧪 Testing

### Run Component Tests

```bash
# Test data store
python src/data_store.py

# Test all agents (includes Safety Guard and ReAct)
python src/agents.py

# Test workflow
python src/agentic_workflow.py

# Run comprehensive safety and ReAct test suite
python test_safety_react.py
```

### Comprehensive Test Suite

The `test_safety_react.py` includes:
- ✅ **Safety Guard Input Validation** (6 test cases)
- ✅ **Safety Guard Output Validation** (4 test cases)
- ✅ **ReAct Agent Reasoning** (3 scenarios)
- ✅ **ReAct Agent Observation** (2 scenarios)
- ✅ **Full Workflow Integration** (3 end-to-end tests)
- ✅ **Edge Cases** (4 scenarios)

### Expected Output
Each test should show:
- ✅ Successful API connection
- ✅ Safety checks passing/blocking appropriately
- ✅ ReAct cycles completing with reasoning traces
- ✅ Data loading and retrieval
- ✅ Response generation with validation

---

## 📚 Learn More

- **🏗️ Advanced Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - Deep dive into ReAct and Safety Guardrails
- **📋 Full Technical Blueprint**: [erik/project-outline.md](erik/project-outline.md)
- **🚀 Quick Start Guide**: [QUICK_START.md](QUICK_START.md)
- **🎬 Demo Preparation**: [DEMO.md](DEMO.md)

### External Resources
- [NVIDIA Build Platform](https://build.nvidia.com/)
- [Nemotron Safety Guard Model](https://build.nvidia.com/nvidia/llama-3_1-nemotron-safety-guard-8b-v3)
- [Nemotron Models Documentation](https://docs.nvidia.com/nemo-framework/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)

---

## 🤝 Contributing

This is a hackathon project, but feedback and ideas are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NVIDIA** for Nemotron models and NIM infrastructure
- **LangChain/LangGraph** teams for orchestration frameworks
- **Hackathon organizers** for the opportunity
- **Quantified Self community** for inspiration

---

## 👥 Team

Built with ❤️ for NVIDIA GTC 2025 Hackathon - Nemotron Prize Track

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/hackathon-nvidia-gtc-25/issues)
- **Documentation**: See `erik/` directory
- **NVIDIA Developer**: [developer.nvidia.com](https://developer.nvidia.com)

---

<div align="center">

**🏆 Built to showcase the power of agentic AI with NVIDIA Nemotron models**

*From Quantified Self to Understood Self*

</div>
