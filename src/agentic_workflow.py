"""LangGraph agentic workflow for personal lifelog analysis with ReAct pattern."""
from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from src.agents import QueryAnalyzer, ReasoningAgent, SafetyGuardAgent, ReActAgent
from src.data_store import LifelogDataStore


class AgentState(TypedDict):
    """State passed between nodes in the graph."""
    query: str
    query_analysis: dict
    retrieved_data: list
    response: str
    reasoning_steps: list
    safety_checks: list
    react_context: dict
    observations: list
    iteration_count: int
    should_continue: bool


class LifelogAgentWorkflow:
    """Orchestrates the agentic workflow using LangGraph with ReAct pattern and safety guardrails."""
    
    def __init__(self, data_store: LifelogDataStore, max_iterations: int = 3):
        """Initialize the workflow with required components.
        
        Args:
            data_store: Vector database for lifelog data
            max_iterations: Maximum ReAct loop iterations
        """
        self.data_store = data_store
        self.query_analyzer = QueryAnalyzer()
        self.reasoning_agent = ReasoningAgent()
        self.safety_guard = SafetyGuardAgent()
        self.react_agent = ReActAgent()
        self.max_iterations = max_iterations
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow with ReAct pattern and safety guardrails.
        
        The workflow follows this pattern:
        1. Safety Check (Input) - Validate user input
        2. ReAct Loop:
           - Reason: Analyze query and plan actions
           - Act: Retrieve data or perform actions
           - Observe: Reflect on results and decide next steps
        3. Synthesize Response
        4. Safety Check (Output) - Validate AI response
        
        Returns:
            Compiled state graph
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes for safety guardrails
        workflow.add_node("safety_check_input", self.safety_check_input_node)
        workflow.add_node("safety_check_output", self.safety_check_output_node)
        
        # Add nodes for ReAct pattern
        workflow.add_node("react_reason", self.react_reason_node)
        workflow.add_node("react_act", self.react_act_node)
        workflow.add_node("react_observe", self.react_observe_node)
        
        # Add node for final synthesis
        workflow.add_node("synthesize_response", self.synthesize_response_node)
        
        # Define workflow flow
        workflow.set_entry_point("safety_check_input")
        
        # After input safety check, start ReAct reasoning
        workflow.add_edge("safety_check_input", "react_reason")
        
        # After reasoning, perform action
        workflow.add_edge("react_reason", "react_act")
        
        # After action, observe and decide
        workflow.add_edge("react_act", "react_observe")
        
        # After observation, either continue ReAct loop or synthesize
        workflow.add_conditional_edges(
            "react_observe",
            self._should_continue_react,
            {
                "continue": "react_reason",  # Loop back for more reasoning
                "synthesize": "synthesize_response"  # Move to final answer
            }
        )
        
        # After synthesis, check output safety
        workflow.add_edge("synthesize_response", "safety_check_output")
        
        # After output safety check, end
        workflow.add_edge("safety_check_output", END)
        
        return workflow.compile()
    
    def _should_continue_react(self, state: AgentState) -> str:
        """Determine if ReAct loop should continue or move to synthesis.
        
        Args:
            state: Current agent state
            
        Returns:
            "continue" to keep looping, "synthesize" to generate final answer
        """
        # Check if we've hit max iterations
        if state.get("iteration_count", 0) >= self.max_iterations:
            return "synthesize"
        
        # Check if agent decided it has sufficient information
        if state.get("should_continue", False) is False:
            return "synthesize"
        
        # Check if we have enough data
        if len(state.get("observations", [])) >= 2 and state.get("retrieved_data"):
            return "synthesize"
        
        # Continue by default
        return "continue"
    
    def analyze_query_node(self, state: AgentState) -> AgentState:
        """Node 1: Analyze user query to understand intent.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with query analysis
        """
        query = state["query"]
        
        # Add reasoning step
        reasoning_steps = state.get("reasoning_steps", [])
        reasoning_steps.append({
            "step": "Query Analysis",
            "description": f"Analyzing query: '{query}'"
        })
        
        # Analyze the query
        analysis = self.query_analyzer.analyze_query(query)
        
        reasoning_steps.append({
            "step": "Query Analysis Complete",
            "description": f"Extracted intent and search parameters"
        })
        
        return {
            **state,
            "query_analysis": analysis,
            "reasoning_steps": reasoning_steps
        }
    
    def retrieve_data_node(self, state: AgentState) -> AgentState:
        """Node 2: Retrieve relevant data from vector store.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with retrieved data
        """
        query = state["query"]
        reasoning_steps = state.get("reasoning_steps", [])
        
        reasoning_steps.append({
            "step": "Data Retrieval",
            "description": "Searching vector database for relevant lifelog entries"
        })
        
        # Query the vector store
        results = self.data_store.query(query, n_results=5)
        
        reasoning_steps.append({
            "step": "Data Retrieved",
            "description": f"Found {len(results)} relevant entries"
        })
        
        return {
            **state,
            "retrieved_data": results,
            "reasoning_steps": reasoning_steps
        }
    
    def synthesize_response_node(self, state: AgentState) -> AgentState:
        """Node 3: Synthesize final response using Nemotron.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with final response
        """
        query = state["query"]
        retrieved_data = state.get("retrieved_data", [])
        reasoning_steps = state.get("reasoning_steps", [])
        
        reasoning_steps.append({
            "step": "Response Synthesis",
            "description": "Using Nemotron to analyze patterns and generate insights"
        })
        
        # Generate response using reasoning agent
        response = self.reasoning_agent.analyze_with_context(query, retrieved_data)
        
        reasoning_steps.append({
            "step": "Complete",
            "description": "Generated personalized insights and recommendations"
        })
        
        return {
            **state,
            "response": response,
            "reasoning_steps": reasoning_steps
        }
    
    def run(self, query: str) -> dict:
        """Execute the workflow for a given query.
        
        Args:
            query: User's natural language question
            
        Returns:
            Dictionary with response and reasoning steps
        """
        initial_state = {
            "query": query,
            "query_analysis": {},
            "retrieved_data": [],
            "response": "",
            "reasoning_steps": []
        }
        
        try:
            # Run the graph
            final_state = self.graph.invoke(initial_state)
            
            return {
                "success": True,
                "query": query,
                "response": final_state["response"],
                "reasoning_steps": final_state["reasoning_steps"],
                "retrieved_entries": len(final_state.get("retrieved_data", []))
            }
        
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "response": f"Sorry, I encountered an error: {str(e)}"
            }


# Convenience function for testing
def test_workflow():
    """Test the agentic workflow."""
    print("🧪 Testing Agentic Workflow with LangGraph...\n")
    
    # Initialize components
    data_store = LifelogDataStore()
    
    # Load sample data
    print("📥 Loading sample data...")
    count = data_store.load_and_store_csv("data/sample_lifelog.csv")
    print(f"✅ Loaded {count} entries\n")
    
    # Create workflow
    workflow = LifelogAgentWorkflow(data_store)
    
    # Test queries
    test_queries = [
        "What patterns do you see in my sleep quality over the past week?",
        "When do I feel most productive based on my logs?",
        "What might be contributing to my low mood scores recently?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"🔍 Test Query {i}: {query}")
        print('='*60)
        
        result = workflow.run(query)
        
        if result["success"]:
            print("\n📊 Reasoning Steps:")
            for step in result["reasoning_steps"]:
                print(f"  → {step['step']}: {step['description']}")
            
            print(f"\n💡 Response:")
            print(result["response"])
            print(f"\n📈 Retrieved {result['retrieved_entries']} relevant entries")
        else:
            print(f"\n❌ Error: {result['error']}")
    
    print("\n\n✅ Workflow test complete!")


if __name__ == "__main__":
    test_workflow()

