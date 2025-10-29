"""Streamlit chat interface for Agentic Lifelog MVP."""
import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
from src.data_store import LifelogDataStore
from src.agentic_workflow import LifelogAgentWorkflow

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Agentic Lifelog - Personal AI Coach",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        color: #76B900;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
    }
    .reasoning-step {
        background-color: #f0f2f6;
        padding: 0.7rem 1.2rem;
        border-radius: 8px;
        margin: 0.4rem 0;
        border-left: 4px solid #76B900;
        transition: all 0.3s ease;
    }
    .reasoning-step:hover {
        background-color: #e8eaed;
        border-left: 4px solid #5a9400;
    }
    .step-title {
        font-weight: bold;
        color: #76B900;
        font-size: 1.05rem;
    }
    .stat-box {
        background: linear-gradient(135deg, #76B900 0%, #5a9400 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-box h3 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stat-box p {
        color: rgba(255,255,255,0.9);
        margin: 0.3rem 0 0 0;
    }
    .agent-badge {
        display: inline-block;
        background-color: #76B900;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        margin: 0.2rem;
    }
    .safety-check {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
    }
    .react-cycle {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .synthesis {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    .demo-banner {
        background: linear-gradient(90deg, #76B900 0%, #5a9400 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initialize the data store and workflow (cached for performance)."""
    # Check for API key
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        st.error("⚠️ NVIDIA_API_KEY not found! Please set it in your .env file.")
        st.stop()
    
    # Initialize data store
    data_store = LifelogDataStore()
    
    # Load sample data
    try:
        count = data_store.load_and_store_csv("data/sample_lifelog.csv")
        stats = data_store.get_stats()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()
    
    # Initialize workflow
    workflow = LifelogAgentWorkflow(data_store)
    
    return workflow, data_store, stats


@st.cache_data
def load_lifelog_data():
    """Load and cache the lifelog data for visualization."""
    try:
        df = pd.read_csv("data/sample_lifelog.csv")
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"Error loading data for visualization: {e}")
        return None


def create_mood_timeline(df):
    """Create a timeline chart of mood scores."""
    fig = px.line(df, x='date', y='mood_score', color='category',
                  title='Mood & Activity Timeline',
                  labels={'mood_score': 'Score (1-5)', 'date': 'Date'},
                  markers=True,
                  color_discrete_map={
                      'mood': '#76B900',
                      'sleep': '#2196f3',
                      'exercise': '#ff9800',
                      'work': '#9c27b0'
                  })
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_category_summary(df):
    """Create a summary chart by category."""
    avg_by_category = df.groupby('category')['mood_score'].mean().reset_index()
    fig = px.bar(avg_by_category, x='category', y='mood_score',
                 title='Average Score by Category',
                 labels={'mood_score': 'Average Score', 'category': 'Category'},
                 color='category',
                 color_discrete_map={
                     'mood': '#76B900',
                     'sleep': '#2196f3',
                     'exercise': '#ff9800',
                     'work': '#9c27b0'
                 })
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
    return fig


def render_reasoning_step(step):
    """Render a reasoning step with appropriate styling."""
    step_text = step['step']
    description = step['description']
    
    # Determine CSS class based on step type
    css_class = "reasoning-step"
    if "Safety" in step_text:
        css_class += " safety-check"
    elif "ReAct" in step_text:
        css_class += " react-cycle"
    elif "Synthesis" in step_text:
        css_class += " synthesis"
    
    return f"""
    <div class="{css_class}">
        <span class="step-title">{step_text}</span><br/>
        {description}
    </div>
    """


def get_demo_questions():
    """Return a list of demo questions for quick testing."""
    return [
        "What patterns do you see in my sleep quality?",
        "How does exercise impact my mood and energy levels?",
        "What's the relationship between my work productivity and sleep?",
        "When do I feel most productive during the week?",
        "What recommendations do you have for improving my overall well-being?",
        "Are there any correlations between my daily activities and mood scores?"
    ]


def main():
    """Main application entry point."""
    
    # Header
    st.markdown('<div class="main-header">🧠 Agentic Lifelog</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your Personal AI Coach powered by NVIDIA Nemotron</div>', unsafe_allow_html=True)
    
    # Initialize system
    workflow, data_store, stats = initialize_system()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Status")
        
        st.markdown(f"""
        <div class="stat-box">
            <h3>{stats['total_entries']}</h3>
            <p>Lifelog Entries Loaded</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.header("💡 Sample Questions")
        st.markdown("""
        Try asking:
        - *What patterns do you see in my sleep quality?*
        - *When do I feel most productive?*
        - *What's affecting my mood scores?*
        - *How does exercise impact my energy levels?*
        - *What recommendations do you have for better sleep?*
        """)
        
        st.markdown("---")
        
        st.header("🚀 How It Works")
        st.markdown("""
        1. **🛡️ Safety Check**: Validates input with Nemotron Guard
        2. **🧠 ReAct Loop**: 
           - **Reason**: Plans next action
           - **Act**: Retrieves data
           - **Observe**: Reflects on results
        3. **🎨 Synthesis**: Generates insights
        4. **🛡️ Output Validation**: Ensures safe response
        """)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            Powered by<br/>
            <b>NVIDIA Nemotron Super 49B</b><br/>
            <b>Nemotron Safety Guard 8B v3</b><br/>
            LangGraph • ChromaDB • ReAct Pattern
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    st.header("💬 Ask About Your Personal Data")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "👋 Hello! I'm your personal AI coach. I can analyze your lifelog data and provide insights about your sleep, mood, productivity, and exercise patterns. What would you like to know?"
        })
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display reasoning steps if present
            if "reasoning_steps" in message:
                with st.expander("🔍 View Agent Reasoning Process (ReAct Pattern)"):
                    for step in message["reasoning_steps"]:
                        st.markdown(f"""
                        <div class="reasoning-step">
                            <span class="step-title">{step['step']}</span><br/>
                            {step['description']}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Display safety checks if present
            if "safety_checks" in message and message["safety_checks"]:
                with st.expander("🛡️ Safety Guardrails"):
                    for check in message["safety_checks"]:
                        check_type = check.get("type", "unknown")
                        is_safe = check.get("is_safe", True)
                        icon = "✅" if is_safe else "⚠️"
                        
                        st.markdown(f"""
                        <div class="reasoning-step">
                            <span class="step-title">{icon} {check_type.title()} Check</span><br/>
                            Status: {'Safe' if is_safe else 'Flagged'}<br/>
                            Category: {check.get('category', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Display ReAct cycles if present
            if "react_cycles" in message and message["react_cycles"] > 0:
                st.info(f"🔄 ReAct Cycles: {message['react_cycles']} iteration(s)")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your lifelog data..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Analyzing your data..."):
                result = workflow.run(prompt)
            
            if result["success"]:
                st.markdown(result["response"])
                
                # Store assistant message with all metadata
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["response"],
                    "reasoning_steps": result.get("reasoning_steps", []),
                    "safety_checks": result.get("safety_checks", []),
                    "react_cycles": result.get("react_cycles", 0)
                })
                
                # Show reasoning steps
                with st.expander("🔍 View Agent Reasoning Process (ReAct Pattern)"):
                    for step in result["reasoning_steps"]:
                        st.markdown(f"""
                        <div class="reasoning-step">
                            <span class="step-title">{step['step']}</span><br/>
                            {step['description']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Show safety checks
                if result.get("safety_checks"):
                    with st.expander("🛡️ Safety Guardrails"):
                        for check in result["safety_checks"]:
                            check_type = check.get("type", "unknown")
                            is_safe = check.get("is_safe", True)
                            icon = "✅" if is_safe else "⚠️"
                            
                            st.markdown(f"""
                            <div class="reasoning-step">
                                <span class="step-title">{icon} {check_type.title()} Check</span><br/>
                                Status: {'Safe' if is_safe else 'Flagged'}<br/>
                                Category: {check.get('category', 'N/A')}
                            </div>
                            """, unsafe_allow_html=True)
                
                # Show stats
                react_cycles = result.get("react_cycles", 0)
                st.info(f"📈 Analyzed {result['retrieved_entries']} relevant entries | 🔄 ReAct Cycles: {react_cycles}")
            else:
                error_msg = f"❌ Sorry, I encountered an error: {result.get('error', 'Unknown error')}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.85rem;">
        <b>🏆 Built for NVIDIA GTC Hackathon 2025 - Nemotron Prize Track</b><br/>
        Demonstrating agentic AI with ReAct pattern, safety guardrails, multi-agent orchestration, and RAG
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

