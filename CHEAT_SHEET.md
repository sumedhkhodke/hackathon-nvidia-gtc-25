# Cheat Sheet

## Essential Commands

```bash
# Setup
uv sync
export NVIDIA_API_KEY="nvapi-your-key"

# Test
uv run python src/data_store.py
uv run python src/agents.py

# Run
uv run streamlit run app.py

# Git
git add . && git commit -m "message" && git push
```

## Demo Questions

1. "What patterns do you see in my sleep quality over the past week?"
2. "When do I feel most productive based on my logs?"
3. "What might be contributing to my low mood scores recently?"

## Quick Fixes

| Issue | Fix |
|-------|-----|
| API Key Error | `echo $NVIDIA_API_KEY` |
| Import Error | `uv sync --force-reinstall` |
| DB Error | `rm -rf chroma_db/ && uv run python src/data_store.py` |
| Fresh Start | `rm -rf .venv chroma_db/ && uv sync` |

## Architecture

```
User Query
    ↓
Query Analysis (Nemotron)
    ↓
Vector Search (ChromaDB)
    ↓
Reasoning & Synthesis (Nemotron)
    ↓
Personalized Insight
```

## Judging Criteria

- **Creativity**: Quantified Self → Understood Self
- **Functionality**: Live agentic AI demo
- **Completion**: Full working MVP + architecture
- **Presentation**: Clear problem + solution
- **NVIDIA Tools**: NIM API + ChromaDB
- **Nemotron**: Multi-model specialized architecture ⭐

## File Structure

```
app.py              # Main UI (START HERE)
src/
  ├── agents.py             # Nemotron integration
  ├── data_store.py         # Vector DB
  └── agentic_workflow.py   # LangGraph workflow
data/
  └── sample_lifelog.csv    # 32 sample entries
```
