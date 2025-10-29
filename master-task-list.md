# Master Task List - Agentic Lifelog MVP (1 Hour Sprint)

## 🚨 CRITICAL: Time-Boxed 1-Hour MVP Strategy

**Goal**: Demonstrate the CORE agentic concept with Nemotron models, not build the full system.

**Philosophy**: Working demo > Perfect architecture. Focus on ONE end-to-end flow that judges can interact with.

---

## Pre-Flight Check (5 minutes)

### Environment Setup
- [ ] **Verify Python 3.10+ installed**: `python --version`
- [ ] **Create virtual environment**: 
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Mac/Linux (Windows: venv\Scripts\activate)
  ```
- [ ] **Get NVIDIA API Key**: 
  - Go to https://build.nvidia.com/
  - Sign up/login and navigate to any model
  - Click "Get API Key" and copy it
- [ ] **Configure environment**:
  ```bash
  cp env.example .env
  # Edit .env and replace 'your_key_here' with your actual key
  # OR export directly:
  export NVIDIA_API_KEY="nvapi-your-actual-key-here"
  ```
- [ ] **Verify setup**: `echo $NVIDIA_API_KEY` (should show your key)

---

## Phase 1: Minimal Infrastructure (15 minutes)

### Task 1.1: Install Dependencies
**Time: 3 minutes**
- [ ] Create `requirements.txt`:
  ```
  langchain==0.1.0
  langchain-nvidia-ai-endpoints==0.0.11
  langgraph==0.0.20
  streamlit==1.29.0
  chromadb==0.4.22
  pandas==2.1.4
  python-dotenv==1.0.0
  ```
- [ ] Install: `pip install -r requirements.txt`

### Task 1.2: Sample Data Creation
**Time: 5 minutes**
- [ ] Create `data/sample_lifelog.csv` with mock personal data:
  - Columns: date, category, entry, mood_score
  - 20-30 rows of sample entries (sleep, exercise, work, mood)
  - Example: "2025-10-15, sleep, Slept 6.5 hours, woke up twice, 3"

### Task 1.3: Simple Vector Store Setup
**Time: 7 minutes**
- [ ] Create `src/data_store.py`:
  - Function to load CSV
  - Function to create ChromaDB collection
  - Function to embed and store data using simple text embeddings
  - Function to query vector store

---

## Phase 2: Core Agentic Workflow (25 minutes)

### Task 2.1: NVIDIA Nemotron Integration
**Time: 10 minutes**
- [ ] Create `src/agents.py`
- [ ] Setup NVIDIA API client for Nemotron model
- [ ] Use **ONE** model initially: `nvidia/llama-3.3-nemotron-super-49b-v1.5-instruct`
- [ ] Test simple completion to verify API works

### Task 2.2: Minimal LangGraph Agent
**Time: 15 minutes**
- [ ] Create `src/agentic_workflow.py`
- [ ] Define LangGraph StateGraph with state schema:
  ```python
  from typing import TypedDict
  class AgentState(TypedDict):
      query: str
      query_analysis: dict
      retrieved_data: list
      response: str
  ```
- [ ] Define 3 nodes:
  1. **analyze_query_node**: Uses QueryAnalyzer to understand intent
  2. **retrieve_data_node**: Uses LifelogDataStore to get relevant entries
  3. **synthesize_node**: Uses ReasoningAgent to generate insights
- [ ] Connect nodes: START → analyze → retrieve → synthesize → END
- [ ] Add error handling for each node
- [ ] Create `run_workflow(query: str)` function that returns response
- [ ] Test with simple query: "How is my sleep?"

**SIMPLIFIED WORKFLOW** (no web search, no multimodal for now):
```
User Query → Analyze Intent → Retrieve Personal Data → Synthesize Answer
```

---

## Phase 3: User Interface (10 minutes)

### Task 3.1: Streamlit Chat Interface
**Time: 10 minutes**
- [ ] Create `app.py`
- [ ] Initialize on startup:
  ```python
  # Load data store
  # Initialize workflow
  # Display welcome message
  ```
- [ ] Main chat interface:
  - `st.chat_input()` for user questions
  - `st.chat_message()` for display
  - Show each workflow step (expander for reasoning)
  - Display final response
  - Handle loading states with spinner
- [ ] Add sidebar:
  - Database stats (entries loaded)
  - Model info (Nemotron Super 49B)
  - Sample questions as buttons
- [ ] Error handling:
  - Missing API key → show setup instructions
  - No data → show data loading instructions
  - API errors → friendly message
- [ ] Test locally: `streamlit run app.py`

---

## Phase 4: Demo Preparation (10 minutes)

### Task 4.1: Prepare Demo Script
**Time: 5 minutes**
- [ ] Create `DEMO.md` with:
  - 3 pre-tested questions that work well
  - Expected responses
  - Key talking points for each judging criterion

**Sample Questions**:
1. "What patterns do you see in my sleep quality over the past week?"
2. "When do I feel most productive based on my logs?"
3. "What might be contributing to my low mood scores recently?"

### Task 4.2: Documentation Sprint
**Time: 5 minutes**
- [ ] Update `README.md` with:
  - Quick start instructions
  - Architecture diagram (simple text/ASCII)
  - How it addresses judging criteria
  - Future roadmap (the full vision from project-outline.md)

---

## Phase 5: Final Polish & Testing (10 minutes)

### Task 5.1: End-to-End Test
**Time: 5 minutes**
- [ ] **Pre-flight checks**:
  - `python src/data_store.py` → Should load 32 entries
  - `python src/agents.py` → Should pass all 3 agent tests
  - Verify NVIDIA_API_KEY is set: `echo $NVIDIA_API_KEY`
- [ ] **Integration test**:
  - `streamlit run app.py`
  - Test all 3 demo questions:
    1. "What patterns do you see in my sleep quality over the past week?"
    2. "What might be contributing to my low mood scores recently?"
    3. "When do I feel most productive based on my logs?"
- [ ] **Validation**:
  - Responses are coherent and data-grounded
  - Reasoning steps are visible
  - Response time < 15 seconds
  - No errors in console
- [ ] **Record results** for demo backup

### Task 5.2: Error Handling & Fallbacks
**Time: 3 minutes**
- [ ] Add try-catch blocks for API failures
- [ ] Add friendly error messages
- [ ] Test with invalid input

### Task 5.3: Git & Submission Prep
**Time: 2 minutes**
- [ ] `git add .`
- [ ] `git commit -m "MVP: Agentic Lifelog with Nemotron"`
- [ ] `git push origin main`
- [ ] Test clone and run from fresh directory

---

## Priority Ranking (If Running Out of Time)

### MUST HAVE (Core Demo):
1. ✅ One Nemotron model working via API
2. ✅ Sample data in vector store
3. ✅ Basic question → retrieve → answer flow
4. ✅ Simple UI to show it working

### SHOULD HAVE (Scoring Points):
5. ✅ LangGraph orchestration (shows sophistication)
6. ✅ Visible agent reasoning steps (shows agentic behavior)
7. ✅ Clean README with architecture explanation

### NICE TO HAVE (If Time Permits):
8. ⚠️ Multiple agent types (reasoning + retrieval)
9. ⚠️ Safety guardrails
10. ⚠️ Pretty UI

### CUT IF NECESSARY:
- ❌ Multimodal processing (future work)
- ❌ Web search integration (future work)
- ❌ Local model deployment (use API for demo)
- ❌ Multiple data source connectors (just CSV)
- ❌ Advanced privacy features (document the architecture)

---

## File Structure (Minimal)

```
hackathon-nvidia-gtc-25/
├── app.py                      # Streamlit UI (ENTRY POINT)
├── requirements.txt            # Dependencies
├── .env                        # API keys (gitignored)
├── README.md                   # Main documentation
├── DEMO.md                     # Demo script for judges
├── data/
│   └── sample_lifelog.csv     # Sample data
├── src/
│   ├── __init__.py
│   ├── data_store.py          # Vector DB operations
│   ├── agents.py              # Nemotron API integration
│   └── agentic_workflow.py    # LangGraph workflow
└── erik/                       # Keep existing planning docs
```

---

## Judging Criteria Alignment (Talk Track)

### Creativity (Innovative Problem-Solving)
- "We're solving the 'data-rich, insight-poor' problem for personal data"
- "Moving from Quantified Self to Understood Self using agentic AI"

### Functionality (Working Prototype)
- Live demo: Ask questions, get personalized insights
- Shows data retrieval, reasoning, and synthesis in real-time

### Scope of Completion
- "This is Phase 1 of our roadmap (show project-outline.md)"
- "MVP demonstrates core workflow; architecture is designed for full system"

### Presentation
- Clear architecture diagram in README
- Demo script with 3 compelling use cases
- Link to full technical blueprint (project-outline.md)

### Use of NVIDIA Tools
- Using NVIDIA NIM API endpoints
- ChromaDB for local vector storage (ready for NVIDIA embedding models)

### Use of NVIDIA Nemotron Models ⭐
- **PRIMARY**: Llama 3.3 Nemotron Super 49B for reasoning and synthesis
- **FUTURE**: Document how we'd use nano models, multimodal, and safety models
- "We designed a multi-model architecture where each Nemotron variant serves a specialized role"

---

## 🚨 Troubleshooting Guide

### Common Issues

**API Key Error**: "NVIDIA_API_KEY environment variable not set"
- Solution: `export NVIDIA_API_KEY="nvapi-your-key"` or check `.env` file

**Import Error**: "No module named 'langchain'"
- Solution: Ensure venv is activated, run `pip install -r requirements.txt`

**ChromaDB Error**: "Collection already exists"
- Solution: Delete `chroma_db/` directory and reload data

**Slow API Response**: Response takes >20 seconds
- Expected: First call may be slower due to model cold start
- If persistent: Check internet connection or NVIDIA API status

**Empty Results**: Query returns no relevant data
- Solution: Verify data is loaded: `python src/data_store.py`
- Check that sample_lifelog.csv exists in data/ directory

---

## Emergency Shortcuts (If Under 30 Minutes Left)

1. **Skip LangGraph**: Use simple function calls, document the intended graph architecture
2. **Skip Vector Store**: Use simple keyword search on pandas DataFrame
3. **Skip Streamlit**: Use CLI with colored output (`rich` library)
4. **Focus on**: One working question → answer with Nemotron API → show reasoning

---

## Success Criteria (Minimum Viable Demo)

✅ User can ask a question about their personal data
✅ System retrieves relevant context from stored data  
✅ Nemotron model generates a personalized insight
✅ The flow is visible (shows agentic reasoning steps)
✅ Demo is stable and reproducible
✅ README explains the vision and architecture
✅ Can articulate how this scales to full system

---

## Post-Demo (If Time Remains)

- [ ] Record a 2-minute demo video
- [ ] Add screenshots to README
- [ ] Clean up code comments
- [ ] Add docstrings to main functions

---

## Contact & Resources

- NVIDIA Build API: https://build.nvidia.com/
- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- Nemotron Models: https://build.nvidia.com/explore/reasoning

**Remember**: A simple working demo with a compelling story beats a complex broken system. Focus on the story: "This is a personal AI co-pilot that turns your data into actionable insights using specialized Nemotron models."

