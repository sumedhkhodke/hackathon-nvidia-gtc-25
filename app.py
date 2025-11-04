"""Enhanced Streamlit chat interface for Agentic Lifelog POC Demo."""
import os
# Suppress tokenizer parallelism warning from ChromaDB/embedding models
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
from src.data_store import LifelogDataStore
from src.agentic_workflow import LifelogAgentWorkflow
from src.background_agents import BackgroundAnalyzer

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Agentic Lifelog - POC Demo",
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
        background: linear-gradient(90deg, #76B900 0%, #5a9400 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
        border-left: 4px solid #4caf50 !important;
    }
    .react-cycle {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800 !important;
    }
    .synthesis {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3 !important;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
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
        font-weight: bold;
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
    
    # Run background analysis (only once per session)
    if not st.session_state.get("insights_generated", False):
        with st.spinner("🔄 Running background analysis..."):
            analyzer = BackgroundAnalyzer(data_store)
            analyzer.run_analysis()
            st.session_state.insights_generated = True
            st.success("✅ Background insights ready!")
    
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
                  title='Lifelog Timeline - All Categories',
                  labels={'mood_score': 'Score (1-5)', 'date': 'Date'},
                  markers=True,
                  color_discrete_map={
                      'mood': '#76B900',
                      'sleep': '#2196f3',
                      'exercise': '#ff9800',
                      'work': '#9c27b0'
                  })
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
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
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
    return fig


def create_correlation_heatmap(df):
    """Create a correlation heatmap showing relationships between categories."""
    # Pivot to get categories as columns
    pivot_df = df.pivot_table(index='date', columns='category', values='mood_score')
    
    # Calculate correlation
    corr = pivot_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdYlGn',
        zmid=0
    ))
    fig.update_layout(
        title='Category Correlation Matrix',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
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
    st.markdown('<div class="sub-header">Your Personal AI Coach powered by NVIDIA Nemotron Multi-Agent System</div>', unsafe_allow_html=True)
    
    # Demo banner
    st.markdown("""
    <div class="demo-banner">
        🏆 NVIDIA GTC Hackathon 2025 - Nemotron Prize Track POC Demo<br/>
        Showcasing: ReAct Pattern • Multi-Agent Orchestration • Safety Guardrails • Agentic RAG
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    workflow, data_store, stats = initialize_system()
    df = load_lifelog_data()
    
    # Sidebar
    with st.sidebar:
        st.image("https://www.nvidia.com/content/dam/en-zz/Solutions/about-nvidia/logo-and-brand/01-nvidia-logo-vert-500x200-2c50-d@2x.png", width=150)
        
        st.markdown("---")
        
        st.header("🎯 Quick Demo")
        
        # Demo questions buttons
        demo_questions = get_demo_questions()
        st.write("**Click to try:**")
        for i, question in enumerate(demo_questions[:4]):
            if st.button(f"💡 {question[:35]}...", key=f"demo_{i}", width='stretch'):
                st.session_state.demo_question = question
        
        st.markdown("---")
        
        st.header("📊 System Status")
        
        st.markdown(f"""
        <div class="stat-box">
            <h3>{stats['total_entries']}</h3>
            <p>Lifelog Entries</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.header("🤖 Active Agents")
        st.markdown("""
        <span class="agent-badge">🧠 Super 49B v1.5</span>
        <span class="agent-badge">🛡️ Safety 8B v3</span>
        <span class="agent-badge">⚡ Nano 9B v2</span>
        <span class="agent-badge">🔄 ReAct</span>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.header("🎨 Architecture")
        st.markdown("""
        **Multi-Agent Workflow:**
        1. 🛡️ Input Safety Check
        2. 🔄 ReAct Loop (1-3 cycles)
           - Reason & Plan
           - Act & Retrieve
           - Observe & Decide
        3. 🎨 Synthesize Insights
        4. 🛡️ Output Validation
        
        **Tech Stack:**
        - NVIDIA Nemotron Models
        - LangGraph Orchestration
        - ChromaDB Vector Store
        - Agentic RAG Pattern
        """)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["💬 Chat Interface", "📊 Data Insights", "🔬 System Info"])
    
    with tab1:
        # Main chat interface
        st.header("Ask Your Personal AI Coach")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # Add welcome message
            st.session_state.messages.append({
                "role": "assistant",
                "content": """👋 **Hello! I'm your Agentic AI Coach.**

I can analyze your lifelog data using advanced multi-agent reasoning to provide deep insights about your:
- 😴 Sleep patterns and quality
- 🏃 Exercise habits and energy levels  
- 💼 Work productivity patterns
- 😊 Mood trends and correlations

**I use a sophisticated ReAct (Reasoning + Action) pattern with safety guardrails to ensure accurate, helpful, and safe responses.**

Try asking me a question, or click a demo button in the sidebar!"""
            })
        
        # Check for demo question
        if hasattr(st.session_state, 'demo_question'):
            prompt = st.session_state.demo_question
            del st.session_state.demo_question
        else:
            prompt = None
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display detailed metrics if present
                if "react_cycles" in message or "retrieved_entries" in message:
                    cols = st.columns(4)
                    if "react_cycles" in message:
                        cols[0].metric("🔄 ReAct Cycles", message.get("react_cycles", 0))
                    if "retrieved_entries" in message:
                        cols[1].metric("📊 Entries Retrieved", message.get("retrieved_entries", 0))
                    if "safety_checks" in message:
                        cols[2].metric("🛡️ Safety Checks", len(message.get("safety_checks", [])))
                    if "elapsed_time" in message:
                        cols[3].metric("⏱️ Response Time", f"{message.get('elapsed_time', 0):.2f}s")
                
                # Display reasoning steps if present
                if "reasoning_steps" in message and message["reasoning_steps"]:
                    with st.expander("🔍 View Multi-Agent Reasoning Process", expanded=False):
                        for step in message["reasoning_steps"]:
                            st.markdown(render_reasoning_step(step), unsafe_allow_html=True)
                
                # Display safety checks if present
                if "safety_checks" in message and message["safety_checks"]:
                    with st.expander("🛡️ Safety Guardrails Report", expanded=False):
                        for check in message["safety_checks"]:
                            check_type = check.get("type", "unknown")
                            is_safe = check.get("is_safe", True)
                            icon = "✅" if is_safe else "⚠️"
                            st.markdown(f"{icon} **{check_type.upper()} Check**: {'Passed' if is_safe else 'Flagged'} - Category: {check.get('category', 'N/A')}")
        
        # Chat input
        user_input = prompt if prompt else st.chat_input("Ask me anything about your lifelog data...")
        
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Multi-agent system analyzing your data..."):
                    start_time = datetime.now()
                    result = workflow.run(user_input)
                    elapsed_time = (datetime.now() - start_time).total_seconds()
                
                if result["success"]:
                    st.markdown(result["response"])
                    
                    # Show metrics
                    cols = st.columns(4)
                    cols[0].metric("🔄 ReAct Cycles", result.get("react_cycles", 0))
                    cols[1].metric("📊 Entries Retrieved", result.get("retrieved_entries", 0))
                    cols[2].metric("🛡️ Safety Checks", len(result.get("safety_checks", [])))
                    cols[3].metric("⏱️ Response Time", f"{elapsed_time:.2f}s")
                    
                    # Store assistant message with reasoning
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["response"],
                        "reasoning_steps": result.get("reasoning_steps", []),
                        "safety_checks": result.get("safety_checks", []),
                        "react_cycles": result.get("react_cycles", 0),
                        "retrieved_entries": result.get("retrieved_entries", 0),
                        "elapsed_time": elapsed_time
                    })
                    
                    # Show reasoning steps
                    with st.expander("🔍 View Multi-Agent Reasoning Process", expanded=True):
                        for step in result["reasoning_steps"]:
                            st.markdown(render_reasoning_step(step), unsafe_allow_html=True)
                    
                    # Show safety checks details
                    if result.get("safety_checks"):
                        with st.expander("🛡️ Safety Guardrails Report", expanded=False):
                            for check in result["safety_checks"]:
                                check_type = check.get("type", "unknown")
                                is_safe = check.get("is_safe", True)
                                icon = "✅" if is_safe else "⚠️"
                                st.markdown(f"{icon} **{check_type.upper()} Check**: {'Passed' if is_safe else 'Flagged'} - Category: {check.get('category', 'N/A')}")
                else:
                    error_msg = f"❌ Sorry, I encountered an error: {result.get('error', 'Unknown error')}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    with tab2:
        # Data visualization tab
        st.header("📊 Your Lifelog Data Insights")
        
        if df is not None:
            # Summary stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <h3 style="color: #2196f3;">😴</h3>
                    <p><b style="font-size: 2rem;">{:.1f}</b><br/>Avg Sleep Score</p>
                </div>
                """.format(df[df['category']=='sleep']['mood_score'].mean()), unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <h3 style="color: #ff9800;">🏃</h3>
                    <p><b style="font-size: 2rem;">{:.1f}</b><br/>Avg Exercise Score</p>
                </div>
                """.format(df[df['category']=='exercise']['mood_score'].mean()), unsafe_allow_html=True)
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <h3 style="color: #9c27b0;">💼</h3>
                    <p><b style="font-size: 2rem;">{:.1f}</b><br/>Avg Work Score</p>
                </div>
                """.format(df[df['category']=='work']['mood_score'].mean()), unsafe_allow_html=True)
            with col4:
                st.markdown("""
                <div class="metric-card">
                    <h3 style="color: #76B900;">😊</h3>
                    <p><b style="font-size: 2rem;">{:.1f}</b><br/>Avg Mood Score</p>
                </div>
                """.format(df[df['category']=='mood']['mood_score'].mean()), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_mood_timeline(df), width='stretch')
            
            with col2:
                st.plotly_chart(create_category_summary(df), width='stretch')
            
            st.markdown("---")
            
            # Correlation heatmap
            st.plotly_chart(create_correlation_heatmap(df), width='stretch')
            
            st.markdown("---")
            
            # Recent entries
            st.subheader("📝 Recent Lifelog Entries")
            st.dataframe(
                df.sort_values('date', ascending=False).head(15),
                width='stretch',
                hide_index=True
            )
        else:
            st.error("Unable to load data for visualization")
    
    with tab3:
        # System information tab
        st.header("🔬 Agentic System Architecture")
        
        st.markdown("""
        ### 🏗️ Multi-Agent Architecture
        
        This system implements a sophisticated **multi-agent architecture** using NVIDIA Nemotron models, 
        orchestrated by LangGraph to demonstrate advanced agentic AI capabilities for the **NVIDIA GTC Hackathon 2025**.
        Background Analysis & Coaching agents process historical data asynchronously to provide KPI-driven insights to the ReAct workflow.
        """)
        
        mermaid_diagram = """
        <div style='width:100%; background:#ffffff; border-radius:12px; padding:16px; box-shadow:0 0 12px rgba(0,0,0,0.05);'>
            <pre class='mermaid' style='min-height:520px;'>
flowchart LR
    classDef ioNode fill:#ffe0e0,stroke:#d32f2f,stroke-width:2px;

    Question([User question]):::ioNode --> SafetyIn

    subgraph System["Agentic Insight Pipeline"]
        subgraph Capture["1. Capture & Store"]
            UserData[User data streams] --> Normalize[Normalize & tag]
            Normalize --> VectorDB[Vector DB]
            Normalize --> Metadata[Metadata]
        end

        subgraph Background["2. Background Analysis"]
            VectorDB --> AnalysisAgent[Analysis agent]
            Metadata --> AnalysisAgent
            AnalysisAgent --> KPIStore[KPI store]
            KPIStore --> CoachAgent[Coach agent]
            CoachAgent --> InsightsCache[Insights cache]
        end

        subgraph Conversation["3. Conversational Coach"]
            SafetyIn --> Orchestrator[ReAct orchestrator]
            Orchestrator --> Retrieval[Search vector DB]
            Retrieval --> Orchestrator
            Orchestrator --> InsightsTool[Query insights cache]
            InsightsTool --> Orchestrator
            Orchestrator --> Synthesis[Synthesize answer]
            Synthesis --> SafetyOut[Safety check out]
        end
    end

    VectorDB -.-> Retrieval
    InsightsCache -.-> InsightsTool

    SafetyOut --> Response([Coach response]):::ioNode
            </pre>
        </div>
        <script src='https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'></script>
        <script>
            if (window.mermaid) {
                mermaid.initialize({ startOnLoad: false, theme: 'default' });
                mermaid.init(undefined, document.querySelectorAll('.mermaid'));
            }
        </script>
        """

        st.components.v1.html(mermaid_diagram, height=640, scrolling=False)
        
        st.markdown("---")
        
        # Enhanced agent descriptions with new background agents
        st.subheader("🤖 Agent Descriptions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### Core Reasoning Agents
            
            **🧠 Reasoning Agent**
            - Model: Nemotron Super 49B v1.5 ✅
            - High-level reasoning & synthesis
            - Pattern identification
            - Hypothesis generation
            
            **🔄 ReAct Agent**
            - Model: Nemotron Super 49B v1.5 ✅
            - Iterative reasoning loops
            - Action planning & observation
            - Adaptive decision-making
            
            **⚡ Query Analyzer**
            - Model: Nemotron Nano 9B v2 ✅
            - Fast intent extraction
            - Tool selection
            - Optimized for speed
            """)
        
        with col2:
            st.markdown("""
            ### Background Analysis
            
            **📊 Analysis Agent**
            - Model: Nemotron Super 49B ✅
            - Runs on historical data
            - Calculates KPIs:
              - Sleep quality trends
              - Productivity metrics
              - Mood correlations
              - Activity patterns
            - Triggered separately/scheduled
            
            **🎯 Coach Agent**
            - Model: Nemotron Super 49B ✅
            - Uses KPIs from Analysis Agent
            - Generates coaching insights:
              - Personalized recommendations
              - Goal suggestions
              - Behavior optimizations
            - Pre-computes insights for fast retrieval
            """)
        
        with col3:
            st.markdown("""
            ### Safety & Support
            
            **🛡️ Safety Guard**
            - Model: Nemotron Safety 8B v3 ✅
            - Dual checkpoint system
            - 23 unsafe categories
            - Privacy protection
            
            **💡 Insights Tool**
            - Bridges background & real-time
            - Fetches pre-computed KPIs
            - Enriches ReAct context
            - Enables data-driven responses
            
            **📊 Data Stores**
            - ChromaDB: Vector embeddings
            - KPI Store: Computed metrics
            - Insights Cache: Coach outputs
            - SQLite: Metadata
            """)
        
        st.markdown("---")
        
        # Background agents workflow
        st.subheader("🔄 Background Agent Workflow")
        
        st.markdown("""
        ### How Background Agents Enhance the System
        
        The new **Analysis Agent** and **Coach Agent** operate asynchronously to pre-compute insights:
        
        1. **📊 Analysis Agent (Triggered Separately)**
           - Runs periodic analysis on historical lifelog data
           - Computes KPIs like: average sleep quality, productivity trends, mood patterns
           - Stores metrics in KPI Store for fast retrieval
           - Example KPIs: "Weekly sleep efficiency: 78%", "Peak productivity: Tuesday 2-4pm"
        
        2. **🎯 Coach Agent (Triggered After Analysis)**
           - Uses KPIs from Analysis Agent as input
           - Generates personalized coaching insights based on patterns
           - Pre-computes recommendations for common scenarios
           - Caches insights like: "Your mood improves 23% after morning exercise"
        
        3. **💡 Integration with ReAct Workflow**
           - During ReAct ACT phase, the Insights Tool can query both stores
           - Enriches context with pre-computed KPIs and coaching insights
           - Enables faster, more data-driven responses
           - Example: User asks about sleep → ReAct retrieves both raw data AND pre-computed sleep KPIs
        """)
        
        st.markdown("---")
        
        # Key features
        st.markdown("""
        ### ✨ Key Features Demonstrated
        
        ✅ **Agentic Behavior** - Autonomous reasoning and decision-making  
        ✅ **ReAct Pattern** - Reason → Act → Observe cycles for complex problem-solving  
        ✅ **Multi-Agent Orchestration** - Specialized agents working in coordination via LangGraph  
        ✅ **Background Processing** - Async Analysis & Coach agents for KPI-driven insights
        ✅ **Safety Guardrails** - Dual safety checks on input and output  
        ✅ **Agentic RAG** - Intelligent retrieval-augmented generation  
        ✅ **Tool Integration** - Vector DB querying and data analysis  
        ✅ **State Management** - LangGraph for stateful workflows  
        ✅ **Privacy-by-Design** - Local-first data architecture  
        """)
        
        st.markdown("---")
        
        # Technologies used
        st.subheader("🛠️ Technology Stack")
        
        tech_col1, tech_col2, tech_col3 = st.columns(3)
        
        with tech_col1:
            st.markdown("""
            **AI Models:**
            - Nemotron Super 49B v1.5 ✅
            - Nemotron Safety 8B v3 ✅ (NEW)
            - Nemotron Nano 9B v2 ✅
            - NVIDIA NIM APIs
            """)
        
        with tech_col2:
            st.markdown("""
            **Orchestration:**
            - LangGraph
            - Python OpenAI Client
            - Streamlit
            """)
        
        with tech_col3:
            st.markdown("""
            **Data & Storage:**
            - ChromaDB
            - Pandas
            - Vector Embeddings
            """)
        
        st.markdown("---")
        
        # Alignment with judging criteria
        st.subheader("🏆 Alignment with Judging Criteria")
        
        st.markdown("""
        | Criteria | How We Address It |
        |----------|------------------|
        | **Creativity** | Novel application of multi-agent AI to personal lifelog analysis with ReAct pattern |
        | **Functionality** | Live demo with real data processing, multi-step reasoning, and safety guardrails |
        | **Scope of Completion** | Complete end-to-end workflow: data ingestion → RAG retrieval → multi-agent reasoning → safe output |
        | **Presentation** | Interactive UI showing agent reasoning process, safety checks, and system architecture |
        | **Use of NVIDIA Tools** | NVIDIA Nemotron models (Super 49B, Safety 8B v3) via NIM APIs |
        | **Use of Nemotron Models** | Sophisticated multi-agent orchestration demonstrating agentic reasoning and safety capabilities |
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.85rem;">
        <b>🏆 Built for NVIDIA GTC Hackathon 2025 - Nemotron Prize Track</b><br/>
        Demonstrating agentic AI with ReAct pattern, multi-agent orchestration, safety guardrails, and tool integration<br/>
        <i>Powered by NVIDIA Nemotron Super 49B v1.5 & Nemotron Safety Guard 8B v3</i>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

