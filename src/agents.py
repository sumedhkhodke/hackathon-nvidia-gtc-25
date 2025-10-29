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
    """Specialized agent for complex reasoning and synthesis."""
    
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
    """Agent for analyzing user queries and extracting intent."""
    
    def __init__(self):
        super().__init__(model_name="nvidia/llama-3.3-nemotron-super-49b-v1.5-instruct")
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


# Convenience function for testing
def test_agent():
    """Test the Nemotron agent with a simple query."""
    print("🧪 Testing Nemotron Agent...\n")
    
    # Test 1: Basic generation
    agent = NemotronAgent()
    response = agent.generate("What is artificial intelligence in one sentence?")
    print(f"✅ Basic Generation Test:")
    print(f"Response: {response}\n")
    
    # Test 2: Query Analyzer
    print(f"✅ Query Analyzer Test:")
    analyzer = QueryAnalyzer()
    query = "What patterns do you see in my sleep quality over the past week?"
    analysis = analyzer.analyze_query(query)
    print(f"Query: {query}")
    print(f"Analysis:\n{analysis['analysis']}\n")
    
    # Test 3: Reasoning Agent (with mock data)
    print(f"✅ Reasoning Agent Test:")
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
    print(f"Insight:\n{insight}\n")
    
    print("✅ All agent tests complete!")


if __name__ == "__main__":
    test_agent()

