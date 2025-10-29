#!/usr/bin/env python3
"""
Comprehensive component testing script for Agentic Lifelog MVP.
Tests each component systematically and reports results.
"""
import os
import sys
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def test_environment():
    """Test 1: Environment Setup"""
    print_header("TEST 1: Environment Setup")
    
    issues = []
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 10:
        print_success(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        error_msg = f"Python 3.10+ required, found {python_version.major}.{python_version.minor}"
        print_error(error_msg)
        issues.append(error_msg)
    
    # Check required files
    required_files = [
        "requirements.txt",
        "src/data_store.py",
        "src/agents.py",
        "data/sample_lifelog.csv",
        "env.example"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print_success(f"Found: {file}")
        else:
            error_msg = f"Missing: {file}"
            print_error(error_msg)
            issues.append(error_msg)
    
    # Check for .env or NVIDIA_API_KEY
    api_key = os.getenv("NVIDIA_API_KEY")
    if api_key:
        print_success(f"NVIDIA_API_KEY is set (starts with: {api_key[:10]}...)")
    else:
        if Path(".env").exists():
            print_warning(".env file exists but NVIDIA_API_KEY not loaded")
            print_info("Run: source .env or export NVIDIA_API_KEY=your_key")
        else:
            print_warning("No .env file found and NVIDIA_API_KEY not set")
            print_info("Run: cp env.example .env and add your API key")
        issues.append("NVIDIA_API_KEY not configured")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print_success("Running in virtual environment")
    else:
        print_warning("Not in a virtual environment")
        print_info("Recommended: python -m venv venv && source venv/bin/activate")
    
    return len(issues) == 0, issues


def test_dependencies():
    """Test 2: Check Dependencies"""
    print_header("TEST 2: Python Dependencies")
    
    issues = []
    required_packages = [
        "pandas",
        "chromadb",
        "openai",
        "langchain",
        "langgraph",
        "streamlit"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"Imported: {package}")
        except ImportError as e:
            error_msg = f"Failed to import {package}: {str(e)}"
            print_error(error_msg)
            issues.append(error_msg)
    
    if issues:
        print_info("Install missing packages: pip install -r requirements.txt")
    
    return len(issues) == 0, issues


def test_data_store():
    """Test 3: Data Store Component"""
    print_header("TEST 3: Data Store (Vector Database)")
    
    try:
        from src.data_store import LifelogDataStore
        print_success("Imported LifelogDataStore")
        
        # Initialize store
        store = LifelogDataStore(persist_directory="./test_chroma_db")
        print_success("Initialized data store")
        
        # Load sample data
        count = store.load_and_store_csv("data/sample_lifelog.csv")
        print_success(f"Loaded {count} entries into vector database")
        
        # Test query
        results = store.query("sleep quality patterns", n_results=3)
        print_success(f"Query returned {len(results)} relevant entries")
        
        if len(results) > 0:
            print_info(f"Sample result: {results[0]['content'][:80]}...")
        
        # Get stats
        stats = store.get_stats()
        print_success(f"Database stats: {stats}")
        
        # Cleanup test database
        import shutil
        if Path("./test_chroma_db").exists():
            shutil.rmtree("./test_chroma_db")
            print_info("Cleaned up test database")
        
        return True, []
        
    except Exception as e:
        error_msg = f"Data store test failed: {str(e)}"
        print_error(error_msg)
        import traceback
        print(traceback.format_exc())
        return False, [error_msg]


def test_agents():
    """Test 4: NVIDIA Nemotron Agents"""
    print_header("TEST 4: NVIDIA Nemotron Agents")
    
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        error_msg = "NVIDIA_API_KEY not set. Skipping agent tests."
        print_error(error_msg)
        print_info("Set API key: export NVIDIA_API_KEY=your_key")
        return False, [error_msg]
    
    try:
        from src.agents import NemotronAgent, QueryAnalyzer, ReasoningAgent
        print_success("Imported agent classes")
        
        # Test 1: Basic agent
        print_info("\nTesting basic NemotronAgent...")
        agent = NemotronAgent()
        response = agent.generate("What is 2+2? Answer in one short sentence.")
        if response and len(response) > 0 and "error" not in response.lower():
            print_success(f"Basic agent works! Response: {response[:100]}")
        else:
            print_error(f"Basic agent failed: {response}")
            return False, ["Basic agent test failed"]
        
        # Test 2: Query Analyzer
        print_info("\nTesting QueryAnalyzer...")
        analyzer = QueryAnalyzer()
        query = "What patterns do you see in my sleep quality over the past week?"
        analysis = analyzer.analyze_query(query)
        if analysis and 'analysis' in analysis:
            print_success("Query analyzer works!")
            print_info(f"Analysis preview: {str(analysis['analysis'])[:150]}...")
        else:
            print_warning("Query analyzer returned unexpected format")
        
        # Test 3: Reasoning Agent
        print_info("\nTesting ReasoningAgent with mock data...")
        reasoner = ReasoningAgent()
        
        mock_data = [
            {"content": "Date: 2025-10-22\nCategory: sleep\nEntry: Slept 7.5 hours, feel refreshed\nMood: 4"},
            {"content": "Date: 2025-10-23\nCategory: sleep\nEntry: Only 5.5 hours, multiple wake-ups\nMood: 2"},
        ]
        
        insight = reasoner.analyze_with_context(
            "What patterns do you see in my sleep?",
            mock_data
        )
        
        if insight and len(insight) > 50 and "error" not in insight.lower():
            print_success("Reasoning agent works!")
            print_info(f"Insight preview: {insight[:200]}...")
        else:
            print_error(f"Reasoning agent failed: {insight}")
            return False, ["Reasoning agent test failed"]
        
        print_success("\n🎉 All agent tests passed!")
        return True, []
        
    except Exception as e:
        error_msg = f"Agent test failed: {str(e)}"
        print_error(error_msg)
        import traceback
        print(traceback.format_exc())
        return False, [error_msg]


def test_integration():
    """Test 5: Integration Test (Data Store + Agents)"""
    print_header("TEST 5: Integration Test")
    
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print_error("NVIDIA_API_KEY not set. Skipping integration test.")
        return False, ["API key not configured"]
    
    try:
        from src.data_store import LifelogDataStore
        from src.agents import ReasoningAgent
        
        print_info("Running end-to-end flow: Query → Retrieve → Reason")
        
        # Step 1: Load data
        store = LifelogDataStore(persist_directory="./test_chroma_db")
        count = store.load_and_store_csv("data/sample_lifelog.csv")
        print_success(f"Step 1: Loaded {count} entries")
        
        # Step 2: Query for relevant data
        user_query = "How is my sleep quality?"
        results = store.query(user_query, n_results=5)
        print_success(f"Step 2: Retrieved {len(results)} relevant entries")
        
        # Step 3: Generate insight
        reasoner = ReasoningAgent()
        insight = reasoner.analyze_with_context(user_query, results)
        print_success(f"Step 3: Generated insight")
        print_info(f"\nFinal Result:\n{Colors.BOLD}{insight}{Colors.END}")
        
        # Cleanup
        import shutil
        if Path("./test_chroma_db").exists():
            shutil.rmtree("./test_chroma_db")
        
        print_success("\n🎉 Integration test passed!")
        return True, []
        
    except Exception as e:
        error_msg = f"Integration test failed: {str(e)}"
        print_error(error_msg)
        import traceback
        print(traceback.format_exc())
        return False, [error_msg]


def main():
    """Run all tests."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     AGENTIC LIFELOG - COMPONENT TEST SUITE               ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    results = {}
    all_issues = []
    
    # Run all tests
    tests = [
        ("Environment Setup", test_environment),
        ("Dependencies", test_dependencies),
        ("Data Store", test_data_store),
        ("NVIDIA Agents", test_agents),
        ("Integration", test_integration),
    ]
    
    for test_name, test_func in tests:
        try:
            success, issues = test_func()
            results[test_name] = success
            all_issues.extend(issues)
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
            all_issues.append(f"{test_name} crashed")
    
    # Summary
    print_header("TEST SUMMARY")
    
    for test_name, success in results.items():
        if success:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    passed = sum(1 for s in results.values() if s)
    total = len(results)
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}")
    
    if all_issues:
        print_warning(f"\nFound {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"  • {issue}")
    else:
        print_success("\n🎉 All tests passed! System is ready for workflow integration.")
    
    # Next steps
    if passed == total:
        print_header("NEXT STEPS")
        print_info("✅ All components tested and working!")
        print_info("📝 Next: Build src/agentic_workflow.py")
        print_info("📝 Then: Build app.py")
        print_info("🚀 Finally: Run 'streamlit run app.py'")
    else:
        print_header("RECOMMENDED ACTIONS")
        if "NVIDIA_API_KEY not configured" in all_issues:
            print_info("1. Copy env.example to .env: cp env.example .env")
            print_info("2. Edit .env and add your NVIDIA API key")
            print_info("3. Export it: export NVIDIA_API_KEY=your_key")
        if any("import" in issue.lower() for issue in all_issues):
            print_info("4. Install dependencies: pip install -r requirements.txt")
        print_info("5. Re-run this script: python test_components.py")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

