"""Streamlit chat interface for Agentic Lifelog MVP."""
import streamlit as st
import os
from dotenv import load_dotenv
from src.data_store import LifelogDataStore
from src.agentic_workflow import LifelogAgentWorkflow

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Agentic Lifelog - Personal AI Coach",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #76B900;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .reasoning-step {
        background-color: #f0f2f6;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.3rem 0;
        border-left: 3px solid #76B900;
    }
    .step-title {
        font-weight: bold;
        color: #76B900;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
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
        1. **Query Analysis**: Understands your question
        2. **Data Retrieval**: Searches your lifelog data
        3. **AI Synthesis**: Nemotron generates insights
        """)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            Powered by<br/>
            <b>NVIDIA Nemotron Super 49B</b><br/>
            LangGraph • ChromaDB
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
                with st.expander("🔍 View Agent Reasoning Process"):
                    for step in message["reasoning_steps"]:
                        st.markdown(f"""
                        <div class="reasoning-step">
                            <span class="step-title">{step['step']}</span><br/>
                            {step['description']}
                        </div>
                        """, unsafe_allow_html=True)
    
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
                
                # Store assistant message with reasoning
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["response"],
                    "reasoning_steps": result["reasoning_steps"]
                })
                
                # Show reasoning steps
                with st.expander("🔍 View Agent Reasoning Process"):
                    for step in result["reasoning_steps"]:
                        st.markdown(f"""
                        <div class="reasoning-step">
                            <span class="step-title">{step['step']}</span><br/>
                            {step['description']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Show stats
                st.info(f"📈 Analyzed {result['retrieved_entries']} relevant entries from your lifelog")
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
        Demonstrating agentic AI with multi-step reasoning, RAG, and tool orchestration
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

