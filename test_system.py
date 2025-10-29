"""System validation script - test without requiring API key."""
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    required_modules = [
        ("streamlit", "Streamlit"),
        ("langchain", "LangChain"),
        ("langgraph", "LangGraph"),
        ("chromadb", "ChromaDB"),
        ("pandas", "Pandas"),
        ("dotenv", "python-dotenv"),
        ("openai", "OpenAI"),
    ]
    
    failed = []
    for module, name in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {name} imported successfully")
        except ImportError as e:
            print(f"  ❌ {name} failed to import: {e}")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Failed to import: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed correctly\n")
    return True


def test_data_files():
    """Test that required data files exist."""
    print("🧪 Testing data files...")
    
    required_files = [
        "data/sample_lifelog.csv",
        "src/__init__.py",
        "src/agents.py",
        "src/data_store.py",
        "src/agentic_workflow.py",
        "app.py",
        "requirements.txt",
        "env.example",
    ]
    
    failed = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path} exists")
        else:
            print(f"  ❌ {file_path} missing")
            failed.append(file_path)
    
    if failed:
        print(f"\n❌ Missing files: {', '.join(failed)}")
        return False
    
    print("✅ All required files present\n")
    return True


def test_data_structure():
    """Test that sample data has correct structure."""
    print("🧪 Testing data structure...")
    
    try:
        import pandas as pd
        df = pd.read_csv("data/sample_lifelog.csv")
        
        required_columns = ['date', 'category', 'entry', 'mood_score']
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            print(f"  ❌ Missing columns: {missing_cols}")
            return False
        
        print(f"  ✅ CSV has correct columns: {list(df.columns)}")
        print(f"  ✅ CSV has {len(df)} entries")
        
        if len(df) < 20:
            print(f"  ⚠️  Warning: Only {len(df)} entries (recommended: 20+)")
        
        print("✅ Data structure valid\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading CSV: {e}")
        return False


def test_code_structure():
    """Test that Python modules have correct structure."""
    print("🧪 Testing code structure...")
    
    try:
        # Test agents module
        from src.agents import NemotronAgent, QueryAnalyzer, ReasoningAgent
        print("  ✅ src.agents - all classes importable")
        
        # Test data_store module
        from src.data_store import LifelogDataStore
        print("  ✅ src.data_store - LifelogDataStore importable")
        
        # Test workflow module
        from src.agentic_workflow import LifelogAgentWorkflow, AgentState
        print("  ✅ src.agentic_workflow - workflow classes importable")
        
        print("✅ Code structure valid\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_environment():
    """Test environment configuration."""
    print("🧪 Testing environment...")
    
    import os
    from dotenv import load_dotenv
    
    # Try to load .env
    if Path(".env").exists():
        load_dotenv()
        print("  ✅ .env file found")
        
        api_key = os.getenv("NVIDIA_API_KEY")
        if api_key and api_key != "your_key_here":
            print("  ✅ NVIDIA_API_KEY is set")
            return True
        else:
            print("  ⚠️  NVIDIA_API_KEY not configured in .env")
            print("     Copy env.example to .env and add your key")
            return False
    else:
        print("  ⚠️  .env file not found")
        print("     Copy env.example to .env and add your NVIDIA_API_KEY")
        return False


def print_summary(results):
    """Print test summary."""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems ready!")
        print("\n📝 Next steps:")
        print("   1. Ensure NVIDIA_API_KEY is set in .env")
        print("   2. Run: streamlit run app.py")
        print("   3. Ask: 'What patterns do you see in my sleep quality?'")
        return True
    else:
        print("\n⚠️  Some tests failed. Please fix issues above.")
        return False


def main():
    """Run all system tests."""
    print("\n" + "="*60)
    print("🚀 AGENTIC LIFELOG - SYSTEM VALIDATION")
    print("="*60 + "\n")
    
    results = {
        "Dependencies": test_imports(),
        "Required Files": test_data_files(),
        "Data Structure": test_data_structure(),
        "Code Structure": test_code_structure(),
        "Environment": test_environment(),
    }
    
    success = print_summary(results)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

