# 🏆 Agentic Lifelog - Demo Guide for Judges

## Quick Start

```bash
# Make sure you're in the project directory
cd /Users/edjenkins/Documents/GitHub/Fun/hackathon-nvidia-gtc-25

# Ensure environment is activated and dependencies installed
uv pip install -e .

# Run the Streamlit app
streamlit run app.py
```

## Demo Flow (5-7 minutes)

### 1. Introduction (30 seconds)
**Say:** "Welcome to Agentic Lifelog - a multi-agent AI system that transforms personal data overload into actionable insights using NVIDIA Nemotron models."

**Show:** Point to the banner showing the key technologies:
- ReAct Pattern
- Multi-Agent Orchestration  
- Safety Guardrails
- Agentic RAG

### 2. System Overview (1 minute)
**Navigate to:** "🔬 System Info" tab

**Show:**
- The ASCII architecture diagram showing the full multi-agent workflow
- Point out the **5 key stages**:
  1. 🛡️ Input Safety Check (Nemotron Safety Guard 8B v3)
  2. 🔄 ReAct Loop (1-3 cycles of Reason → Act → Observe)
  3. 📊 Data Retrieval (Vector DB with RAG)
  4. 🎨 Synthesis (Nemotron Super 49B)
  5. 🛡️ Output Safety Check

**Say:** "This demonstrates sophisticated agentic AI - the system autonomously reasons, plans, retrieves data, and makes decisions through multiple cycles."

### 3. Data Insights (1 minute)
**Navigate to:** "📊 Data Insights" tab

**Show:**
- The 4 metric cards showing average scores by category
- Timeline chart showing all lifelog activities
- Category summary bar chart
- Correlation heatmap

**Say:** "Our system ingests multi-modal personal data into a vector database. Here you can see sleep, exercise, work, and mood patterns from real lifelog entries."

### 4. Live Demo - Simple Query (2 minutes)
**Navigate to:** "💬 Chat Interface" tab

**Click:** One of the demo buttons in sidebar, e.g., "What patterns do you see in my sleep quality?"

**As it processes, point out:**
- The spinner: "Multi-agent system analyzing your data..."
- When complete, show the 4 metrics:
  - 🔄 ReAct Cycles (typically 1-3)
  - 📊 Entries Retrieved
  - 🛡️ Safety Checks (2: input + output)
  - ⏱️ Response Time

**Expand:** "🔍 View Multi-Agent Reasoning Process"

**Walk through the steps:**
- "🛡️ Input Safety Check" (green) - Safety Guard validates input
- "🧠 ReAct Cycle 1: REASON" (orange) - Plans the action
- "⚡ ReAct: ACT" - Retrieves relevant data
- "👁️ ReAct: OBSERVE" - Reflects on results
- "🎨 Response Synthesis" (blue) - Nemotron generates insights
- "🛡️ Output Safety Check" (green) - Final validation

**Say:** "This transparent reasoning process shows true agentic behavior - the system isn't just responding to a prompt, it's autonomously planning, acting, and reflecting."

### 5. Live Demo - Complex Query (2 minutes)
**Type or click:** "What recommendations do you have for improving my overall well-being?"

**As it processes, highlight:**
- Higher ReAct cycles (possibly 2-3 iterations)
- More entries retrieved
- More complex reasoning steps

**Expand:** "🛡️ Safety Guardrails Report"

**Show:** Both safety checks passed
- ✅ INPUT Check: Passed
- ✅ OUTPUT Check: Passed

**Say:** "Safety is built into the architecture. Every interaction goes through Nemotron Safety Guard twice - validating inputs and filtering outputs to prevent harmful content and protect privacy."

### 6. Alignment with Judging Criteria (30 seconds)
**Navigate back to:** "🔬 System Info" tab, scroll to bottom

**Show:** The criteria alignment table

**Key points to emphasize:**
- ✅ **Creativity:** Novel ReAct pattern application to personal data
- ✅ **Functionality:** Live multi-agent reasoning with real data
- ✅ **Use of NVIDIA Tools:** 2 Nemotron models working together
- ✅ **Agentic AI:** Autonomous reasoning, multi-step planning, tool integration

### 7. Closing (30 seconds)
**Say:** "This POC demonstrates the future of personal AI - not just answering questions, but actively reasoning about your life patterns with privacy-by-design and built-in safety guardrails. All powered by NVIDIA Nemotron models orchestrated through LangGraph."

---

## Quick Demo Questions to Try

### Simple Queries (1-2 ReAct cycles):
- "What patterns do you see in my sleep quality?"
- "When do I feel most productive?"

### Complex Queries (2-3 ReAct cycles):
- "How does exercise impact my mood and energy levels?"
- "What recommendations do you have for improving my overall well-being?"
- "Are there any correlations between my daily activities and mood scores?"

### To Demonstrate Safety Guards:
Try asking something off-topic or requesting medical advice to show the safety system in action (though it may allow general wellness advice).

---

## Key Talking Points

### 🎯 What Makes This Agentic AI?
1. **Autonomous Decision-Making** - System decides when it has enough information
2. **Multi-Step Reasoning** - ReAct loops allow iterative problem solving
3. **Tool Integration** - Actively queries vector database based on reasoning
4. **State Management** - LangGraph maintains context across reasoning cycles
5. **Adaptive Behavior** - Different queries trigger different reasoning patterns

### 🏗️ Technical Architecture Highlights
- **Multi-Agent System** - Specialized agents for reasoning, safety, and retrieval
- **LangGraph Orchestration** - Stateful workflows with conditional routing
- **ReAct Pattern** - Reason → Act → Observe loop (not just Retrieval-Augmented Generation)
- **Dual Safety Layers** - Input and output validation with Nemotron Safety Guard
- **Vector RAG** - ChromaDB with semantic search for personal data

### 🛡️ Privacy & Safety
- **Privacy-by-Design** - Local-first architecture (data stays on user's device)
- **Safety Guardrails** - Nemotron Safety Guard 8B v3 at entry and exit points
- **Transparent Reasoning** - Users see exactly how decisions are made
- **Configurable Policies** - Safety system can enforce user-defined boundaries

---

## Troubleshooting

**If the app doesn't start:**
```bash
# Check API key is set
cat .env | grep NVIDIA_API_KEY

# Reinstall dependencies
uv pip install -e .
```

**If queries fail:**
- Check internet connection (needs to reach NVIDIA NIM APIs)
- Verify NVIDIA_API_KEY is valid
- Check the error message in the UI

**If visualizations don't load:**
- Make sure `data/sample_lifelog.csv` exists
- Check ChromaDB initialized correctly (should see stats in sidebar)

---

## Post-Demo Q&A Prep

**Q: Why use multiple Nemotron models?**
A: We use specialized models for specific tasks - Super 49B for complex reasoning and synthesis, Safety Guard 8B v3 for content moderation. This demonstrates understanding of the NVIDIA ecosystem and optimal resource allocation.

**Q: How is this different from RAG?**
A: Traditional RAG retrieves then generates. Our ReAct pattern allows the agent to reason about what it needs, retrieve iteratively, observe results, and decide if more information is needed - true agentic behavior.

**Q: What's the privacy approach?**
A: Local-first architecture - data stays in local ChromaDB. Models are accessed via API but user data is embedded locally. Production version would support fully local NIM deployment.

**Q: How does it scale?**
A: ChromaDB handles millions of vectors. Multi-agent design allows horizontal scaling. Each agent can be deployed as independent NIM container for production.

**Q: What's next for this project?**
A: 1) Multimodal ingestion (images, voice), 2) Web search integration, 3) Local NIM deployment, 4) Real device integrations (Apple HealthKit, Oura, etc.), 5) Smart glass interface.

---

## Judging Criteria Checklist

- [ ] **Creativity (1-5):** Demonstrated novel ReAct pattern application ✅
- [ ] **Functionality (1-5):** Live demo with stable multi-agent reasoning ✅
- [ ] **Scope (1-5):** Complete workflow with safety, reasoning, retrieval, synthesis ✅
- [ ] **Presentation (1-5):** Clear explanation of architecture and agentic behavior ✅
- [ ] **NVIDIA Tools (1-5):** 2+ Nemotron models via NIM APIs ✅
- [ ] **Nemotron Models (1-5):** Sophisticated multi-agent orchestration showcasing agentic capabilities ✅

---

**Good luck with your demo! 🚀**

