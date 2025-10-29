# Quick Reference Cheat Sheet

## 🚀 Essential Commands

```bash
# Setup (one time)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export NVIDIA_API_KEY="nvapi-your-key"

# Testing Components
python src/data_store.py      # Test vector DB
python src/agents.py           # Test Nemotron API
streamlit run app.py           # Launch full app

# Git
git add .
git commit -m "MVP complete"
git push
```

---

## 📂 File Status

| File | Status | Purpose |
|------|--------|---------|
| `data/sample_lifelog.csv` | ✅ | Sample personal data |
| `src/data_store.py` | ✅ | Vector DB operations |
| `src/agents.py` | ✅ | Nemotron API client |
| `src/agentic_workflow.py` | ⏳ | **BUILD NEXT** |
| `app.py` | ⏳ | **BUILD AFTER** |

---

## 🎯 Demo Questions

1. "What patterns do you see in my sleep quality over the past week?"
2. "When do I feel most productive based on my logs?"
3. "What might be contributing to my low mood scores recently?"

---

## 🐛 Quick Fixes

### API Key Error
```bash
echo $NVIDIA_API_KEY  # Should show nvapi-...
export NVIDIA_API_KEY="your-key"
```

### Import Error
```bash
which python  # Should show venv path
pip install --upgrade -r requirements.txt
```

### ChromaDB Error
```bash
rm -rf chroma_db/
python src/data_store.py  # Rebuild
```

---

## 📊 Architecture Flow

```
User Query
    ↓
[Query Analyzer]  ← Nemotron
    ↓
[Vector DB Query] ← ChromaDB
    ↓
[Reasoning Agent] ← Nemotron Super 49B
    ↓
Insight Response
```

---

## 🎭 Judging Criteria Quick Hits

- **Creativity**: Quantified Self → Understood Self
- **Functionality**: Working demo with live queries
- **Completion**: MVP shows full vision
- **Presentation**: Clear problem + compelling demo
- **NVIDIA Tools**: NIM API + ChromaDB
- **Nemotron Models**: Multi-model specialized architecture ⭐

---

## ⏱️ Time Check

- **Setup**: 5 min
- **Workflow**: 20 min
- **UI**: 15 min
- **Testing**: 10 min
- **Polish**: 10 min
- **Total**: 60 min

---

## 🆘 Emergency (if <30 min)

Skip Streamlit, use this:

```python
# quick_demo.py
from src.data_store import LifelogDataStore
from src.agents import ReasoningAgent

query = "What patterns in my sleep?"
store = LifelogDataStore()
context = store.query(query, n_results=3)
agent = ReasoningAgent()
insight = agent.analyze_with_context(query, context)
print(insight)
```

Run: `python quick_demo.py`

---

## ✅ Pre-Demo Checklist

- [ ] All 3 demo questions work
- [ ] Response time acceptable (<15s)
- [ ] No crashes or errors
- [ ] Can explain architecture
- [ ] README updated
- [ ] Code committed to git
- [ ] DEMO.md script reviewed

---

## 🎤 30-Second Pitch

"We built an AI co-pilot that transforms personal data into insights. Using specialized NVIDIA Nemotron models in a multi-agent architecture, we retrieve relevant context from a local vector database and generate personalized coaching - all while keeping data private. Watch as I ask about my sleep patterns..."

[Show demo]

"This demonstrates agentic AI: autonomous planning, tool use, and reasoning. The architecture scales to a full platform with multimodal data, background insights, and proactive recommendations."

---

## 📞 Key Resources

- NVIDIA Build: https://build.nvidia.com/
- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- START_HERE.md: Your build guide
- DEMO.md: Presentation script
- master-task-list.md: Detailed tasks

---

**Remember**: Working demo > Perfect code

**Focus**: ONE end-to-end flow that works reliably

**Story**: "Personal AI co-pilot with privacy-first agentic intelligence"

**You got this!** 🚀

