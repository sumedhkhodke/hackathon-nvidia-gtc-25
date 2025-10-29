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
    
    def safety_check_input_node(self, state: AgentState) -> AgentState:
        """Node: Safety check for user input using Nemotron Safety Guard.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with safety check results
        """
        query = state["query"]
        reasoning_steps = state.get("reasoning_steps", [])
        safety_checks = state.get("safety_checks", [])
        
        reasoning_steps.append({
            "step": "🛡️ Input Safety Check",
            "description": "Validating user input with Nemotron Safety Guard"
        })
        
        # Perform safety check
        safety_result = self.safety_guard.check_input_safety(query)
        
        # Add to safety checks log
        safety_checks.append({
            "type": "input",
            "is_safe": safety_result["is_safe"],
            "category": safety_result["category"],
            "should_block": safety_result.get("should_block", False)
        })
        
        # If unsafe, block and set error response
        if safety_result.get("should_block", False):
            reasoning_steps.append({
                "step": "⚠️ Input Blocked",
                "description": f"Input flagged as unsafe: {safety_result['category']}"
            })
            
            return {
                **state,
                "safety_checks": safety_checks,
                "reasoning_steps": reasoning_steps,
                "response": f"I'm sorry, but I can't process this request. It was flagged for: {safety_result['category']}. Please rephrase your question.",
                "should_continue": False
            }
        
        reasoning_steps.append({
            "step": "✅ Input Validated",
            "description": "User input passed safety checks"
        })
        
        return {
            **state,
            "safety_checks": safety_checks,
            "reasoning_steps": reasoning_steps,
            "should_continue": True
        }
    
    def react_reason_node(self, state: AgentState) -> AgentState:
        """Node: ReAct REASON - Analyze query and plan next action.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with reasoning and action plan
        """
        query = state["query"]
        reasoning_steps = state.get("reasoning_steps", [])
        react_context = state.get("react_context", {})
        observations = state.get("observations", [])
        iteration = state.get("iteration_count", 0)
        
        reasoning_steps.append({
            "step": f"🧠 ReAct Cycle {iteration + 1}: REASON",
            "description": "Analyzing problem and planning next action"
        })
        
        # Use ReAct agent to reason about the query
        reasoning_result = self.react_agent.reason_and_plan(
            query,
            {"observations": observations}
        )
        
        # Update context
        react_context["current_reasoning"] = reasoning_result["reasoning"]
        react_context["next_action"] = reasoning_result["next_action"]
        
        reasoning_steps.append({
            "step": "💡 Reasoning Complete",
            "description": f"Planned action: {reasoning_result['next_action']}"
        })
        
        return {
            **state,
            "react_context": react_context,
            "reasoning_steps": reasoning_steps
        }
    
    def react_act_node(self, state: AgentState) -> AgentState:
        """Node: ReAct ACT - Execute the planned action.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with action results
        """
        query = state["query"]
        reasoning_steps = state.get("reasoning_steps", [])
        react_context = state.get("react_context", {})
        next_action = react_context.get("next_action", "data_retrieval")
        
        reasoning_steps.append({
            "step": "⚡ ReAct: ACT",
            "description": f"Executing action: {next_action}"
        })
        
        # Execute the action (for now, always retrieve data)
        # In future iterations, this could call different tools
        if "data" in next_action or "retrieval" in next_action or "analysis" in next_action:
            results = self.data_store.query(query, n_results=5)
            action_result = f"Retrieved {len(results)} relevant lifelog entries"
            
            reasoning_steps.append({
                "step": "📊 Data Retrieved",
                "description": f"Found {len(results)} relevant entries from personal lifelog"
            })
            
            return {
                **state,
                "retrieved_data": results,
                "react_context": {**react_context, "last_action_result": action_result},
                "reasoning_steps": reasoning_steps
            }
        else:
            # Default action
            results = self.data_store.query(query, n_results=5)
            action_result = f"Retrieved {len(results)} entries"
            
            return {
                **state,
                "retrieved_data": results,
                "react_context": {**react_context, "last_action_result": action_result},
                "reasoning_steps": reasoning_steps
            }
    
    def react_observe_node(self, state: AgentState) -> AgentState:
        """Node: ReAct OBSERVE - Reflect on action results and decide next steps.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with observations and continuation decision
        """
        query = state["query"]
        reasoning_steps = state.get("reasoning_steps", [])
        react_context = state.get("react_context", {})
        observations = state.get("observations", [])
        iteration_count = state.get("iteration_count", 0)
        
        reasoning_steps.append({
            "step": "👁️ ReAct: OBSERVE",
            "description": "Reflecting on results and determining sufficiency"
        })
        
        # Get last action result
        action_result = react_context.get("last_action_result", "No action result")
        
        # Use ReAct agent to observe and reflect
        observation_result = self.react_agent.observe_and_reflect(action_result, query)
        
        # Add observation to history
        observations.append(observation_result["observation"])
        
        # Increment iteration
        iteration_count += 1
        
        # Determine if we should continue
        should_continue = not observation_result["is_sufficient"]
        
        # Don't continue if we've hit max iterations
        if iteration_count >= self.max_iterations:
            should_continue = False
            reasoning_steps.append({
                "step": "🎯 Observation Complete",
                "description": f"Sufficient information gathered after {iteration_count} cycles"
            })
        elif should_continue:
            reasoning_steps.append({
                "step": "🔄 Need More Information",
                "description": "Continuing ReAct loop for additional data"
            })
        else:
            reasoning_steps.append({
                "step": "✅ Ready to Synthesize",
                "description": "Sufficient information gathered to answer query"
            })
        
        return {
            **state,
            "observations": observations,
            "iteration_count": iteration_count,
            "should_continue": should_continue,
            "reasoning_steps": reasoning_steps
        }
    
    def synthesize_response_node(self, state: AgentState) -> AgentState:
        """Node: Synthesize final response using Nemotron reasoning agent.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with final response
        """
        query = state["query"]
        retrieved_data = state.get("retrieved_data", [])
        reasoning_steps = state.get("reasoning_steps", [])
        observations = state.get("observations", [])
        
        reasoning_steps.append({
            "step": "🎨 Response Synthesis",
            "description": "Synthesizing insights from all gathered information"
        })
        
        # Generate response using reasoning agent
        response = self.reasoning_agent.analyze_with_context(query, retrieved_data)
        
        reasoning_steps.append({
            "step": "✨ Synthesis Complete",
            "description": "Generated personalized insights and recommendations"
        })
        
        return {
            **state,
            "response": response,
            "reasoning_steps": reasoning_steps
        }
    
    def safety_check_output_node(self, state: AgentState) -> AgentState:
        """Node: Safety check for AI-generated output using Nemotron Safety Guard.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with output safety validation
        """
        query = state["query"]
        response = state.get("response", "")
        reasoning_steps = state.get("reasoning_steps", [])
        safety_checks = state.get("safety_checks", [])
        
        reasoning_steps.append({
            "step": "🛡️ Output Safety Check",
            "description": "Validating AI response with Nemotron Safety Guard"
        })
        
        # Perform output safety check
        safety_result = self.safety_guard.check_output_safety(response, query)
        
        # Add to safety checks log
        safety_checks.append({
            "type": "output",
            "is_safe": safety_result["is_safe"],
            "should_block": safety_result.get("should_block", False),
            "needs_modification": safety_result.get("needs_modification", False)
        })
        
        # If output should be blocked
        if safety_result.get("should_block", False):
            reasoning_steps.append({
                "step": "⚠️ Output Blocked",
                "description": "AI response flagged as potentially unsafe"
            })
            
            return {
                **state,
                "safety_checks": safety_checks,
                "reasoning_steps": reasoning_steps,
                "response": "I apologize, but I need to refine my response. Let me provide a safer answer based on your data."
            }
        
        # If output needs modification (log but allow)
        if safety_result.get("needs_modification", False):
            reasoning_steps.append({
                "step": "⚡ Output Refined",
                "description": "Response passed with minor considerations noted"
            })
        else:
            reasoning_steps.append({
                "step": "✅ Output Validated",
                "description": "AI response passed all safety checks"
            })
        
        return {
            **state,
            "safety_checks": safety_checks,
            "reasoning_steps": reasoning_steps
        }
    
    def run(self, query: str) -> dict:
        """Execute the workflow for a given query with ReAct pattern and safety checks.
        
        Args:
            query: User's natural language question
            
        Returns:
            Dictionary with response, reasoning steps, safety checks, and ReAct observations
        """
        initial_state = {
            "query": query,
            "query_analysis": {},
            "retrieved_data": [],
            "response": "",
            "reasoning_steps": [],
            "safety_checks": [],
            "react_context": {},
            "observations": [],
            "iteration_count": 0,
            "should_continue": True
        }
        
        try:
            # Run the graph
            final_state = self.graph.invoke(initial_state)
            
            return {
                "success": True,
                "query": query,
                "response": final_state.get("response", ""),
                "reasoning_steps": final_state.get("reasoning_steps", []),
                "safety_checks": final_state.get("safety_checks", []),
                "observations": final_state.get("observations", []),
                "react_cycles": final_state.get("iteration_count", 0),
                "retrieved_entries": len(final_state.get("retrieved_data", []))
            }
        
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "response": f"Sorry, I encountered an error: {str(e)}",
                "reasoning_steps": []
            }
    
    def stream(self, query: str):
        """Stream the workflow execution with intermediate steps for real-time UI updates.
        
        Args:
            query: User's natural language question
            
        Yields:
            Dictionaries with intermediate state updates for streaming to UI
        """
        initial_state = {
            "query": query,
            "query_analysis": {},
            "retrieved_data": [],
            "response": "",
            "reasoning_steps": [],
            "safety_checks": [],
            "react_context": {},
            "observations": [],
            "iteration_count": 0,
            "should_continue": True
        }
        
        try:
            # Stream the graph execution
            for event in self.graph.stream(initial_state):
                # Extract node name and state from event
                node_name = list(event.keys())[0]
                node_state = event[node_name]
                
                # Yield intermediate state update
                yield {
                    "type": "intermediate",
                    "node": node_name,
                    "reasoning_steps": node_state.get("reasoning_steps", []),
                    "safety_checks": node_state.get("safety_checks", []),
                    "iteration_count": node_state.get("iteration_count", 0),
                    "should_continue": node_state.get("should_continue", True)
                }
            
            # Yield final result
            # Get the last event's state
            final_state = node_state
            
            yield {
                "type": "final",
                "success": True,
                "query": query,
                "response": final_state.get("response", ""),
                "reasoning_steps": final_state.get("reasoning_steps", []),
                "safety_checks": final_state.get("safety_checks", []),
                "observations": final_state.get("observations", []),
                "react_cycles": final_state.get("iteration_count", 0),
                "retrieved_entries": len(final_state.get("retrieved_data", []))
            }
        
        except Exception as e:
            yield {
                "type": "error",
                "success": False,
                "query": query,
                "error": str(e),
                "response": f"Sorry, I encountered an error: {str(e)}",
                "reasoning_steps": []
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

