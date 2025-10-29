# Quick Start

## ⚡ 3-Minute Setup

### 1. Install Dependencies
```bash
uv sync
```

### 2. Set API Key
```bash
# Get key from: https://build.nvidia.com/
export NVIDIA_API_KEY="nvapi-your-key-here"
```

### 3. Run
```bash
# Test components
uv run python src/data_store.py
uv run python src/agents.py

# Launch app
uv run streamlit run app.py
```

---

## 🎯 Demo Questions

1. "What patterns do you see in my sleep quality over the past week?"
2. "When do I feel most productive based on my logs?"
3. "What might be contributing to my low mood scores recently?"

---

## 🐛 Troubleshooting

**API Key Error:**  
`echo $NVIDIA_API_KEY` (should show nvapi-...)

**Import Error:**  
`uv sync --force-reinstall`

**Fresh Start:**  
`rm -rf .venv chroma_db/ && uv sync`

---

See `README.md` for full documentation.
