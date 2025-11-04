"""Simple JSON-based cache for storing and retrieving pre-computed insights."""
import json
import os
from typing import Dict, List, Any
from datetime import datetime


class InsightsCache:
    """Simple JSON-based cache for MVP."""
    
    def __init__(self, cache_file: str = "data/insights_cache.json"):
        """Initialize the cache with the specified file path."""
        self.cache_file = cache_file
        self.insights = self.load_cache()
    
    def load_cache(self) -> Dict[str, Any]:
        """Load insights from cache file if it exists."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"⚠️ Warning: Could not load cache from {self.cache_file}")
                return {}
        return {}
    
    def get_relevant_insights(self, query: str) -> Dict[str, Any]:
        """Return insights relevant to the query using keyword matching."""
        if not self.insights:
            return {}
        
        query_lower = query.lower()
        relevant = {}
        
        # Check if cache is stale (older than 24 hours)
        if "generated_at" in self.insights:
            try:
                generated_time = datetime.fromisoformat(self.insights["generated_at"])
                age_hours = (datetime.now() - generated_time).total_seconds() / 3600
                if age_hours > 24:
                    relevant["cache_warning"] = "Insights are older than 24 hours"
            except:
                pass
        
        # Extract relevant KPIs based on keywords
        kpis = self.insights.get("kpis", {})
        
        # Sleep-related queries
        if any(word in query_lower for word in ["sleep", "rest", "tired", "fatigue", "energy"]):
            if "sleep" in kpis:
                relevant["sleep_kpi"] = kpis["sleep"]
        
        # Mood-related queries
        if any(word in query_lower for word in ["mood", "feeling", "emotion", "happy", "sad", "depressed"]):
            if "mood" in kpis:
                relevant["mood_kpi"] = kpis["mood"]
        
        # Productivity-related queries
        if any(word in query_lower for word in ["productive", "productivity", "work", "focus", "efficient"]):
            if "productivity" in kpis:
                relevant["productivity_kpi"] = kpis["productivity"]
        
        # Exercise-related queries
        if any(word in query_lower for word in ["exercise", "workout", "fitness", "physical", "activity"]):
            if "exercise" in kpis:
                relevant["exercise_kpi"] = kpis["exercise"]
        
        # Health-related queries (include overall score)
        if any(word in query_lower for word in ["health", "overall", "wellness", "wellbeing"]):
            if "overall_health" in kpis:
                relevant["overall_health"] = kpis["overall_health"]
        
        # Extract relevant patterns
        patterns = self.insights.get("patterns", [])
        relevant_patterns = []
        
        for pattern in patterns:
            pattern_text = pattern.get("pattern", "").lower()
            
            # Check if pattern is relevant to query
            if any(word in query_lower for word in pattern_text.split()):
                relevant_patterns.append(pattern)
            # Also check specific keywords
            elif "sleep" in query_lower and "sleep" in pattern_text:
                relevant_patterns.append(pattern)
            elif "mood" in query_lower and "mood" in pattern_text:
                relevant_patterns.append(pattern)
            elif "exercise" in query_lower and "exercise" in pattern_text:
                relevant_patterns.append(pattern)
            elif "productivity" in query_lower and "productivity" in pattern_text:
                relevant_patterns.append(pattern)
        
        if relevant_patterns:
            relevant["patterns"] = relevant_patterns[:3]  # Limit to top 3 most relevant
        
        # Extract relevant coaching insights
        coaching = self.insights.get("coaching", [])
        relevant_coaching = []
        
        for insight in coaching:
            category = insight.get("category", "").lower()
            insight_text = insight.get("insight", "").lower()
            recommendation = insight.get("recommendation", "").lower()
            
            # Check if coaching insight is relevant
            if category in query_lower:
                relevant_coaching.append(insight)
            elif any(word in query_lower for word in insight_text.split()):
                relevant_coaching.append(insight)
            elif any(word in query_lower for word in recommendation.split()[:5]):  # Check first 5 words
                relevant_coaching.append(insight)
        
        if relevant_coaching:
            relevant["coaching_insights"] = relevant_coaching[:2]  # Limit to top 2
        
        # For general queries, include high-priority insights
        if len(relevant) < 2 and any(word in query_lower for word in ["help", "advice", "recommendation", "suggest", "improve"]):
            # Add high priority coaching insights
            high_priority = [i for i in coaching if i.get("priority") == "high"]
            if high_priority:
                relevant["high_priority_insights"] = high_priority[:2]
            
            # Add overall health if available
            if "overall_health" in kpis and "overall_health" not in relevant:
                relevant["overall_health"] = kpis["overall_health"]
        
        return relevant
    
    def has_insights(self) -> bool:
        """Check if any insights are available in the cache."""
        return bool(self.insights)
    
    def get_cache_age_hours(self) -> float:
        """Get the age of the cache in hours."""
        if not self.insights or "generated_at" not in self.insights:
            return float('inf')
        
        try:
            generated_time = datetime.fromisoformat(self.insights["generated_at"])
            return (datetime.now() - generated_time).total_seconds() / 3600
        except:
            return float('inf')
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of available insights."""
        if not self.insights:
            return {"status": "no_cache", "message": "No insights available"}
        
        return {
            "status": "ready",
            "generated_at": self.insights.get("generated_at", "unknown"),
            "age_hours": round(self.get_cache_age_hours(), 1),
            "total_entries_analyzed": self.insights.get("total_entries_analyzed", 0),
            "available_insights": {
                "kpis": len(self.insights.get("kpis", {})),
                "patterns": len(self.insights.get("patterns", [])),
                "coaching": len(self.insights.get("coaching", []))
            }
        }
    
    def clear_cache(self):
        """Clear the insights cache."""
        self.insights = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)


# Convenience function for testing
def test_cache():
    """Test the insights cache functionality."""
    print("🧪 Testing Insights Cache...\n")
    
    # Create test data
    test_insights = {
        "kpis": {
            "sleep": {
                "average_hours": 7.2,
                "quality_score": 7.5,
                "trend": "improving"
            },
            "mood": {
                "average": 3.4,
                "volatility": "moderate"
            }
        },
        "patterns": [
            {
                "pattern": "Poor sleep correlates with low mood the following day",
                "confidence": 0.82,
                "occurrences": 5
            }
        ],
        "coaching": [
            {
                "category": "sleep",
                "insight": "Your sleep quality is improving",
                "recommendation": "Maintain consistent sleep schedule",
                "priority": "medium"
            }
        ],
        "generated_at": datetime.now().isoformat()
    }
    
    # Save test data
    os.makedirs("data", exist_ok=True)
    with open("data/test_insights_cache.json", "w") as f:
        json.dump(test_insights, f, indent=2)
    
    # Test cache loading
    cache = InsightsCache("data/test_insights_cache.json")
    
    print("📊 Cache Summary:")
    print(json.dumps(cache.get_summary(), indent=2))
    
    # Test relevance filtering
    test_queries = [
        "How is my sleep quality?",
        "What's affecting my mood?",
        "Any patterns in my data?",
        "Give me health advice"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        relevant = cache.get_relevant_insights(query)
        print(f"Found {len(relevant)} relevant insight categories")
        for key in relevant:
            print(f"  - {key}")
    
    # Clean up
    os.remove("data/test_insights_cache.json")
    print("\n✅ Cache test complete!")


if __name__ == "__main__":
    test_cache()
