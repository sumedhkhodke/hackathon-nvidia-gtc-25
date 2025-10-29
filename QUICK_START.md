# Quick Start Guide - Agentic Lifelog MVP

## ⚡ Setup (5 minutes)

### 1. Install Dependencies with uv
This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable dependency management.

```bash
# If you don't have uv installed yet:
# curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and create virtual environment
uv sync
```

That's it! `uv sync` will:
- Create a `.venv` directory with a Python 3.12 environment
- Install all dependencies from `pyproject.toml`
- Set up the project in editable mode

### 2. Activate Virtual Environment
```bash
source .venv/bin/activate  # On Mac/Linux
# or on Windows: .venv\Scripts\activate
```

### 3. Get NVIDIA API Key
1. Go to https://build.nvidia.com/
2. Sign up/Login
3. Navigate to any Nemotron model
4. Click "Get API Key"
5. Copy your key

### 4. Set Environment Variable
```bash
cp env.example .env
# Edit .env and add your NVIDIA_API_KEY
```

Or export directly:
```bash
export NVIDIA_API_KEY="nvapi-your-key-here"
```

### 5. Test Data Store
```bash
# With uv (recommended - automatically uses the right Python and packages):
uv run python src/data_store.py

# Or if you activated the venv:
python src/data_store.py
```

You should see:
```
✅ Loaded 32 entries into vector database
🔍 Query: 'sleep quality patterns'
Found 3 relevant entries...
```

---

## 🎯 Next Steps

Follow the **master-task-list.md** for the complete build sequence.

**Current Priority**: 
1. ✅ Data store working
2. ⏳ Build `src/agents.py` (Nemotron API integration)
3. ⏳ Build `src/agentic_workflow.py` (LangGraph)
4. ⏳ Build `app.py` (Streamlit UI)

---

## 🧪 Testing Individual Components

### Test Vector Database
```bash
uv run python src/data_store.py
```

### Test Nemotron API (after creating agents.py)
```bash
uv run python src/agents.py
```

### Test Agentic Workflow (after creating workflow)
```bash
uv run python src/agentic_workflow.py
```

### Launch Full App
```bash
uv run streamlit run app.py
```

---

## 📝 Demo Questions (Pre-tested)

1. "What patterns do you see in my sleep quality over the past week?"
2. "When do I feel most productive based on my logs?"
3. "What might be contributing to my low mood scores recently?"

---

## 🐛 Troubleshooting

### ChromaDB Import Error
```bash
uv sync --force-reinstall
```

### NVIDIA API Error
- Verify API key is set: `echo $NVIDIA_API_KEY`
- Check key starts with `nvapi-`
- Ensure you have internet connection

### Missing Dependencies
```bash
# Re-sync all dependencies
uv sync

# Add a new dependency
uv add package-name

# Remove a dependency
uv remove package-name
```

### Starting Fresh
```bash
# Remove the virtual environment and reinstall
rm -rf .venv uv.lock
uv sync
```

---

## 📊 Success Checklist

- [ ] uv installed (`which uv` shows path)
- [ ] Dependencies synced (`uv sync` completed successfully)
- [ ] Virtual environment created (`.venv/` directory exists)
- [ ] NVIDIA API key configured
- [ ] Sample data loaded into ChromaDB
- [ ] Data store test passes
- [ ] Ready to build agents!

**Time Check**: You should be done with setup in under 3 minutes with uv (it's much faster than pip!). If stuck, skip to emergency shortcuts in master-task-list.md.

---

## 💡 Why uv?

- **10-100x faster** than pip for dependency resolution and installation
- **Reliable** - deterministic builds with lock files
- **Simple** - one command (`uv sync`) does everything
- **Modern** - uses `pyproject.toml` standard instead of `requirements.txt`

