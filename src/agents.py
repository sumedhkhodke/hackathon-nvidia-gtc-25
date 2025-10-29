"""NVIDIA Nemotron API integration for agentic lifelog."""
import os
from typing import Dict, List
from openai import OpenAI


class NemotronAgent:
    """Client for NVIDIA Nemotron models via API."""
    
    def __init__(self, model_name: str = "nvidia/llama-3.3-nemotron-super-49b-v1.5-instruct"):
        """Initialize the Nemotron agent.
        
        Args:
            model_name: Name of the Nemotron model to use
        """
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY environment variable not set!")
        
        self.model_name = model_name
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
    
    def generate(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000) -> str:
        """Generate a response using the Nemotron model.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for agent behavior
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=max_tokens
            )
            
            return completion.choices[0].message.content
        
        except Exception as e:
            return f"Error calling Nemotron API: {str(e)}"


class ReasoningAgent(NemotronAgent):
    """Specialized agent for complex reasoning and synthesis.
    
    Uses Nemotron-super-49b-v1.5 for advanced multi-step reasoning and causal analysis.
    This is one of the recommended models for the NVIDIA GTC 2025 Nemotron Prize Track.
    """
    
    def __init__(self):
        super().__init__(model_name="nvidia/llama-3.3-nemotron-super-49b-v1.5-instruct")
        self.system_prompt = """You are an expert personal AI coach and data analyst. 
Your role is to analyze personal lifelog data and provide insightful, actionable advice.

Guidelines:
- Be empathetic and supportive in tone
- Base insights on the provided data
- Identify patterns and correlations
- Provide specific, actionable recommendations
- If data is insufficient, say so clearly
- Never make medical diagnoses or prescribe treatments"""
    
    def analyze_with_context(self, query: str, context_data: List[Dict]) -> str:
        """Analyze a query with retrieved context data.
        
        Args:
            query: User's question
            context_data: Retrieved relevant data from vector store
            
        Returns:
            Analysis and insights
        """
        # Format context data
        context_text = "\n\n".join([
            f"Entry {i+1}:\n{item['content']}"
            for i, item in enumerate(context_data)
        ])
        
        prompt = f"""Based on the following personal lifelog entries, please answer the user's question.

LIFELOG DATA:
{context_text}

USER QUESTION: {query}

Please provide:
1. Key patterns you observe in the data
2. Relevant insights that answer the question
3. 2-3 specific, actionable recommendations

Your response:"""
        
        return self.generate(prompt, system_prompt=self.system_prompt, max_tokens=1500)


class QueryAnalyzer(NemotronAgent):
    """Agent for analyzing user queries and extracting intent.
    
    Uses Nemotron-nano-9b-v2 for fast, efficient query processing and tool use.
    This is one of the recommended models for the NVIDIA GTC 2025 Nemotron Prize Track.
    """
    
    def __init__(self):
        super().__init__(model_name="nvidia/nvidia-nemotron-nano-9b-v2")
        self.system_prompt = """You are a query analysis agent. 
Your job is to understand user questions about their personal data and extract:
1. The main topic/category (sleep, mood, productivity, exercise, etc.)
2. The time range mentioned (if any)
3. The type of insight requested (pattern, cause, recommendation, etc.)

Be concise and extract key information."""
    
    def analyze_query(self, query: str) -> Dict:
        """Analyze a user query to extract intent and parameters.
        
        Args:
            query: User's natural language question
            
        Returns:
            Dictionary with extracted information
        """
        prompt = f"""Analyze this query and extract key information:

QUERY: "{query}"

Respond in this format:
CATEGORIES: [list main topics: sleep, mood, work, exercise, etc.]
TIME_RANGE: [any time period mentioned, or "not specified"]
INTENT: [what type of insight: pattern analysis, causation, recommendation, etc.]
SEARCH_TERMS: [3-5 key terms to search the data for]"""
        
        response = self.generate(prompt, system_prompt=self.system_prompt, max_tokens=300)
        
        # TODO: Parse response into structured dict
        # For MVP, return raw text
        return {"analysis": response, "query": query}


class SafetyGuardAgent(NemotronAgent):
    """Agent for content safety moderation using Nemotron Safety Guard 8B v3.
    
    This agent acts as a mandatory checkpoint for all user inputs and AI outputs,
    ensuring content safety and adherence to user-defined policies.
    This is one of the NEW recommended models for the NVIDIA GTC 2025 Nemotron Prize Track.
    """
    
    def __init__(self):
        """Initialize the Safety Guard agent with Nemotron Safety Guard 8B v3."""
        super().__init__(model_name="nvidia/llama-3.1-nemotron-safety-guard-8b-v3")
        self.unsafe_categories = [
            "illegal_activity", "violence", "self_harm", "harassment",
            "hate_speech", "sexual_content", "privacy_violation",
            "medical_advice", "financial_advice", "dangerous_content"
        ]
    
    def check_input_safety(self, user_input: str) -> Dict:
        """Check if user input is safe and appropriate.
        
        Args:
            user_input: The user's input text to check
            
        Returns:
            Dictionary with safety assessment:
                - is_safe: bool
                - category: str (if unsafe)
                - explanation: str
                - should_block: bool
        """
        system_prompt = """You are a content safety moderator. Your job is to analyze user input for safety concerns.

Evaluate the input for:
1. Self-harm or crisis indicators
2. Requests for medical or financial advice
3. Privacy violations or attempts to extract sensitive data
4. Inappropriate, harmful, or abusive content
5. Off-topic or malicious queries

Respond in this exact format:
SAFE: [YES or NO]
CATEGORY: [category if unsafe, or "safe" if safe]
SEVERITY: [LOW, MEDIUM, HIGH, or NONE]
EXPLANATION: [brief explanation]
ACTION: [ALLOW or BLOCK]"""

        prompt = f"""Analyze this user input for safety concerns:

USER INPUT: "{user_input}"

Provide your safety assessment:"""

        try:
            response = self.generate(prompt, system_prompt=system_prompt, max_tokens=200)
            
            # Parse the response
            is_safe = "SAFE: YES" in response or "SAFE:YES" in response
            should_block = "ACTION: BLOCK" in response or "ACTION:BLOCK" in response
            
            # Extract category (simple parsing)
            category = "unknown"
            if "CATEGORY:" in response:
                try:
                    category_line = [line for line in response.split('\n') if 'CATEGORY:' in line][0]
                    category = category_line.split('CATEGORY:')[1].strip().lower()
                except:
                    pass
            
            return {
                "is_safe": is_safe and not should_block,
                "category": category if not is_safe else "safe",
                "explanation": response,
                "should_block": should_block,
                "raw_response": response
            }
        
        except Exception as e:
            # Fail-safe: if safety check fails, be cautious
            return {
                "is_safe": False,
                "category": "error",
                "explanation": f"Safety check failed: {str(e)}",
                "should_block": True,
                "error": str(e)
            }
    
    def check_output_safety(self, ai_output: str, user_context: str = "") -> Dict:
        """Check if AI-generated output is safe and appropriate.
        
        Args:
            ai_output: The AI's generated response to check
            user_context: Optional user query context
            
        Returns:
            Dictionary with safety assessment
        """
        system_prompt = """You are a content safety moderator reviewing AI-generated responses.

Check the output for:
1. Medical diagnoses or prescriptive medical advice
2. Financial investment advice or predictions
3. Privacy violations or disclosure of sensitive data
4. Harmful recommendations or dangerous suggestions
5. Biased or inappropriate content

Respond in this exact format:
SAFE: [YES or NO]
ISSUES: [list any issues, or "none" if safe]
SEVERITY: [LOW, MEDIUM, HIGH, or NONE]
RECOMMENDATION: [ALLOW, MODIFY, or BLOCK]"""

        prompt = f"""Review this AI-generated response for safety:

USER QUERY: "{user_context}"

AI RESPONSE: "{ai_output}"

Provide your safety assessment:"""

        try:
            response = self.generate(prompt, system_prompt=system_prompt, max_tokens=200)
            
            is_safe = "SAFE: YES" in response or "SAFE:YES" in response
            should_block = "RECOMMENDATION: BLOCK" in response or "RECOMMENDATION:BLOCK" in response
            needs_modification = "RECOMMENDATION: MODIFY" in response or "RECOMMENDATION:MODIFY" in response
            
            return {
                "is_safe": is_safe and not should_block,
                "needs_modification": needs_modification,
                "should_block": should_block,
                "explanation": response,
                "raw_response": response
            }
        
        except Exception as e:
            # Fail-safe: if safety check fails, allow but log
            return {
                "is_safe": True,  # Don't block on errors for output
                "needs_modification": False,
                "should_block": False,
                "explanation": f"Safety check failed (allowing): {str(e)}",
                "error": str(e)
            }


class ReActAgent(NemotronAgent):
    """Agent implementing the ReAct (Reasoning + Action) pattern.
    
    This agent performs iterative reasoning and action cycles to solve complex problems.
    Uses Nemotron-super-49b-v1.5 for sophisticated multi-step planning and observation.
    This is one of the recommended models for the NVIDIA GTC 2025 Nemotron Prize Track.
    """
    
    def __init__(self):
        """Initialize the ReAct agent with Nemotron Super 49B v1.5."""
        super().__init__(model_name="nvidia/llama-3.3-nemotron-super-49b-v1.5")
        self.system_prompt = """You are an expert reasoning agent using the ReAct pattern.

For each step, you will:
1. REASON: Analyze the current situation and plan your next action
2. ACT: Decide what action to take (query data, search web, analyze, etc.)
3. OBSERVE: Review the results and determine if you need more information

Be explicit about your reasoning process. Think step-by-step."""
    
    def reason_and_plan(self, query: str, context: Dict) -> Dict:
        """First step: Reason about the query and create an action plan.
        
        Args:
            query: User's question
            context: Current context including previous observations
            
        Returns:
            Dictionary with reasoning and planned actions
        """
        # Build context summary
        context_summary = ""
        if context.get("observations"):
            context_summary = "Previous observations:\n" + "\n".join([
                f"- {obs}" for obs in context.get("observations", [])
            ])
        
        prompt = f"""You are solving this problem: "{query}"

{context_summary}

THINK STEP-BY-STEP:
1. What do I need to understand to answer this question?
2. What information do I already have?
3. What information am I missing?
4. What should be my next action?

Respond in this format:
REASONING: [your step-by-step reasoning]
NEXT_ACTION: [data_retrieval, web_search, analysis, or final_answer]
ACTION_DETAILS: [specific details about what to retrieve/search/analyze]
CONFIDENCE: [LOW, MEDIUM, or HIGH]"""

        response = self.generate(prompt, system_prompt=self.system_prompt, max_tokens=400)
        
        # Parse the response
        next_action = "analysis"  # default
        if "NEXT_ACTION:" in response:
            try:
                action_line = [line for line in response.split('\n') if 'NEXT_ACTION:' in line][0]
                next_action = action_line.split('NEXT_ACTION:')[1].strip().lower()
            except:
                pass
        
        return {
            "reasoning": response,
            "next_action": next_action,
            "full_response": response
        }
    
    def observe_and_reflect(self, action_result: str, original_query: str) -> Dict:
        """Third step: Observe results and reflect on next steps.
        
        Args:
            action_result: Results from the action taken
            original_query: The original user query
            
        Returns:
            Dictionary with observations and next step determination
        """
        prompt = f"""You took an action to help answer: "{original_query}"

ACTION RESULT:
{action_result}

REFLECT:
1. What did I learn from this result?
2. Do I have enough information to answer the question?
3. If not, what else do I need?

Respond in this format:
OBSERVATION: [what you learned]
SUFFICIENT: [YES or NO - do you have enough info?]
NEXT_STEP: [continue_searching, ready_to_synthesize, or need_different_approach]
REASONING: [explain your thinking]"""

        response = self.generate(prompt, system_prompt=self.system_prompt, max_tokens=300)
        
        # Parse if we're ready to synthesize
        is_sufficient = "SUFFICIENT: YES" in response or "SUFFICIENT:YES" in response
        
        return {
            "observation": response,
            "is_sufficient": is_sufficient,
            "full_response": response
        }


# Convenience function for testing
def test_agent():
    """Test the Nemotron agent with a simple query."""
    print("🧪 Testing Nemotron Agents...\n")
    
    # Test 1: Basic generation
    print("="*60)
    print("TEST 1: Basic Generation")
    print("="*60)
    agent = NemotronAgent()
    response = agent.generate("What is artificial intelligence in one sentence?")
    print(f"✅ Response: {response}\n")
    
    # Test 2: Query Analyzer
    print("="*60)
    print("TEST 2: Query Analyzer")
    print("="*60)
    analyzer = QueryAnalyzer()
    query = "What patterns do you see in my sleep quality over the past week?"
    analysis = analyzer.analyze_query(query)
    print(f"Query: {query}")
    print(f"✅ Analysis:\n{analysis['analysis']}\n")
    
    # Test 3: Safety Guard - Input Check
    print("="*60)
    print("TEST 3: Safety Guard - Input Safety Check")
    print("="*60)
    safety_guard = SafetyGuardAgent()
    
    # Safe input
    safe_input = "What patterns do you see in my sleep quality?"
    safe_result = safety_guard.check_input_safety(safe_input)
    print(f"Input: '{safe_input}'")
    print(f"✅ Is Safe: {safe_result['is_safe']}")
    print(f"   Category: {safe_result['category']}\n")
    
    # Potentially unsafe input
    unsafe_input = "Can you prescribe me medication for my headaches?"
    unsafe_result = safety_guard.check_input_safety(unsafe_input)
    print(f"Input: '{unsafe_input}'")
    print(f"⚠️  Is Safe: {unsafe_result['is_safe']}")
    print(f"   Should Block: {unsafe_result['should_block']}")
    print(f"   Category: {unsafe_result['category']}\n")
    
    # Test 4: Safety Guard - Output Check
    print("="*60)
    print("TEST 4: Safety Guard - Output Safety Check")
    print("="*60)
    test_output = "Based on your sleep patterns, I recommend trying to sleep 7-8 hours per night."
    output_result = safety_guard.check_output_safety(test_output, safe_input)
    print(f"AI Output: '{test_output}'")
    print(f"✅ Is Safe: {output_result['is_safe']}\n")
    
    # Test 5: ReAct Agent - Reasoning
    print("="*60)
    print("TEST 5: ReAct Agent - Reasoning")
    print("="*60)
    react_agent = ReActAgent()
    reasoning = react_agent.reason_and_plan(
        "What's causing my low energy levels?",
        {"observations": []}
    )
    print(f"Query: 'What's causing my low energy levels?'")
    print(f"✅ Reasoning:\n{reasoning['reasoning']}\n")
    print(f"   Next Action: {reasoning['next_action']}\n")
    
    # Test 6: ReAct Agent - Observation
    print("="*60)
    print("TEST 6: ReAct Agent - Observation")
    print("="*60)
    mock_action_result = "Found 5 entries showing sleep < 6 hours correlates with energy score < 3"
    observation = react_agent.observe_and_reflect(
        mock_action_result,
        "What's causing my low energy levels?"
    )
    print(f"Action Result: '{mock_action_result}'")
    print(f"✅ Observation:\n{observation['observation']}\n")
    print(f"   Sufficient Info: {observation['is_sufficient']}\n")
    
    # Test 7: Reasoning Agent (with mock data)
    print("="*60)
    print("TEST 7: Reasoning Agent with Context")
    print("="*60)
    reasoner = ReasoningAgent()
    
    mock_data = [
        {"content": "Date: 2025-10-22\nCategory: sleep\nEntry: Slept 7.5 hours, feel refreshed\nMood: 4"},
        {"content": "Date: 2025-10-23\nCategory: sleep\nEntry: Only 5.5 hours, multiple wake-ups\nMood: 2"},
        {"content": "Date: 2025-10-24\nCategory: sleep\nEntry: 6 hours, not fully rested\nMood: 3"}
    ]
    
    insight = reasoner.analyze_with_context(
        "What patterns do you see in my sleep?",
        mock_data
    )
    print(f"✅ Insight:\n{insight}\n")
    
    print("="*60)
    print("✅ All agent tests complete!")
    print("="*60)


if __name__ == "__main__":
    test_agent()

