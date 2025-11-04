"""Background agents for pre-computing insights at startup."""
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict, Counter
import numpy as np

from src.data_store import LifelogDataStore
from src.agents import ReasoningAgent


class KPIAgent:
    """Agent for calculating key performance indicators from lifelog data."""
    
    def __init__(self):
        self.reasoning_agent = ReasoningAgent()
    
    def calculate_kpis(self, data_store: LifelogDataStore) -> Dict[str, Any]:
        """Calculate KPIs from all available data."""
        # Get all data
        all_entries = data_store.get_all_entries()
        
        kpis = {
            "sleep": self._calculate_sleep_kpis(all_entries),
            "mood": self._calculate_mood_kpis(all_entries),
            "productivity": self._calculate_productivity_kpis(all_entries),
            "exercise": self._calculate_exercise_kpis(all_entries),
            "overall_health": self._calculate_overall_health_score(all_entries)
        }
        
        return kpis
    
    def _calculate_sleep_kpis(self, entries: List[Dict]) -> Dict:
        """Calculate sleep-related KPIs."""
        sleep_entries = [e for e in entries if e.get("category") == "sleep"]
        
        if not sleep_entries:
            return {"status": "no_data"}
        
        # Extract sleep hours and quality scores
        sleep_hours = []
        quality_scores = []
        
        for entry in sleep_entries:
            content = entry.get("entry", "")
            # Simple extraction - look for patterns like "7.5 hours" or "slept 8h"
            import re
            hours_match = re.search(r'(\d+\.?\d*)\s*h(?:ours?)?', content.lower())
            if hours_match:
                sleep_hours.append(float(hours_match.group(1)))
            
            # Extract quality if mentioned (scale 1-10)
            quality_match = re.search(r'quality[:\s]+(\d+)', content.lower())
            if quality_match:
                quality_scores.append(int(quality_match.group(1)))
        
        return {
            "average_hours": round(np.mean(sleep_hours), 1) if sleep_hours else "unknown",
            "min_hours": round(min(sleep_hours), 1) if sleep_hours else "unknown",
            "max_hours": round(max(sleep_hours), 1) if sleep_hours else "unknown",
            "consistency_score": round(10 - np.std(sleep_hours), 1) if len(sleep_hours) > 1 else "unknown",
            "quality_score": round(np.mean(quality_scores), 1) if quality_scores else "unknown",
            "total_entries": len(sleep_entries),
            "trend": self._calculate_trend(sleep_hours) if len(sleep_hours) > 2 else "insufficient_data"
        }
    
    def _calculate_mood_kpis(self, entries: List[Dict]) -> Dict:
        """Calculate mood-related KPIs."""
        mood_values = []
        
        for entry in entries:
            mood = entry.get("mood")
            if mood and isinstance(mood, (int, float)):
                mood_values.append(mood)
        
        if not mood_values:
            return {"status": "no_data"}
        
        return {
            "average": round(np.mean(mood_values), 1),
            "min": min(mood_values),
            "max": max(mood_values),
            "volatility": "high" if np.std(mood_values) > 1.5 else "moderate" if np.std(mood_values) > 0.8 else "low",
            "trend": self._calculate_trend(mood_values) if len(mood_values) > 2 else "insufficient_data",
            "good_days_percentage": round(len([m for m in mood_values if m >= 4]) / len(mood_values) * 100, 1)
        }
    
    def _calculate_productivity_kpis(self, entries: List[Dict]) -> Dict:
        """Calculate productivity-related KPIs."""
        work_entries = [e for e in entries if e.get("category") == "work"]
        productivity_scores = []
        
        for entry in work_entries:
            prod = entry.get("productivity")
            if prod and isinstance(prod, (int, float)):
                productivity_scores.append(prod)
        
        if not productivity_scores:
            return {"status": "no_data"}
        
        return {
            "average_score": round(np.mean(productivity_scores), 1),
            "peak_performance_days": len([p for p in productivity_scores if p >= 8]),
            "consistency": round(10 - np.std(productivity_scores) * 2, 1) if len(productivity_scores) > 1 else "unknown",
            "trend": self._calculate_trend(productivity_scores) if len(productivity_scores) > 2 else "insufficient_data"
        }
    
    def _calculate_exercise_kpis(self, entries: List[Dict]) -> Dict:
        """Calculate exercise-related KPIs."""
        exercise_entries = [e for e in entries if e.get("category") == "exercise"]
        
        if not exercise_entries:
            return {"status": "no_data"}
        
        # Count exercise types
        exercise_types = []
        for entry in exercise_entries:
            content = entry.get("entry", "").lower()
            if "run" in content or "jog" in content:
                exercise_types.append("cardio")
            elif "weight" in content or "strength" in content:
                exercise_types.append("strength")
            elif "yoga" in content or "stretch" in content:
                exercise_types.append("flexibility")
            elif "walk" in content:
                exercise_types.append("walking")
            else:
                exercise_types.append("other")
        
        type_counts = Counter(exercise_types)
        
        return {
            "total_sessions": len(exercise_entries),
            "types": dict(type_counts),
            "most_common": type_counts.most_common(1)[0][0] if type_counts else "none",
            "weekly_average": round(len(exercise_entries) / max(1, len(set(e.get("date", "")[:10] for e in entries)) / 7), 1)
        }
    
    def _calculate_overall_health_score(self, entries: List[Dict]) -> Dict:
        """Calculate an overall health score based on all metrics."""
        # Simple weighted average of different factors
        scores = []
        weights = []
        
        # Get sub-scores
        sleep_kpis = self._calculate_sleep_kpis(entries)
        mood_kpis = self._calculate_mood_kpis(entries)
        productivity_kpis = self._calculate_productivity_kpis(entries)
        exercise_kpis = self._calculate_exercise_kpis(entries)
        
        # Sleep score (weight: 30%)
        if sleep_kpis.get("average_hours") != "unknown":
            sleep_score = min(10, max(0, (sleep_kpis["average_hours"] - 4) * 1.5))
            scores.append(sleep_score)
            weights.append(0.3)
        
        # Mood score (weight: 25%)
        if mood_kpis.get("average"):
            mood_score = mood_kpis["average"] * 2  # Convert 1-5 to 0-10
            scores.append(mood_score)
            weights.append(0.25)
        
        # Productivity score (weight: 25%)
        if productivity_kpis.get("average_score"):
            scores.append(productivity_kpis["average_score"])
            weights.append(0.25)
        
        # Exercise score (weight: 20%)
        if exercise_kpis.get("weekly_average"):
            exercise_score = min(10, exercise_kpis["weekly_average"] * 2)
            scores.append(exercise_score)
            weights.append(0.2)
        
        if scores:
            # Normalize weights
            weights = [w / sum(weights) for w in weights]
            overall_score = sum(s * w for s, w in zip(scores, weights))
            
            return {
                "score": round(overall_score, 1),
                "rating": "excellent" if overall_score >= 8 else "good" if overall_score >= 6 else "fair" if overall_score >= 4 else "needs_improvement",
                "components": {
                    "sleep_weight": weights[0] if len(weights) > 0 else 0,
                    "mood_weight": weights[1] if len(weights) > 1 else 0,
                    "productivity_weight": weights[2] if len(weights) > 2 else 0,
                    "exercise_weight": weights[3] if len(weights) > 3 else 0
                }
            }
        
        return {"status": "insufficient_data"}
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a series of values."""
        if len(values) < 3:
            return "insufficient_data"
        
        # Simple linear regression
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "improving"
        elif slope < -0.1:
            return "declining"
        else:
            return "stable"


class PatternAgent:
    """Agent for detecting patterns and correlations in lifelog data."""
    
    def __init__(self):
        self.reasoning_agent = ReasoningAgent()
    
    def detect_patterns(self, data_store: LifelogDataStore) -> List[Dict]:
        """Detect patterns in the data."""
        all_entries = data_store.get_all_entries()
        
        patterns = []
        
        # Pattern 1: Sleep-Mood correlation
        sleep_mood_pattern = self._analyze_sleep_mood_correlation(all_entries)
        if sleep_mood_pattern:
            patterns.append(sleep_mood_pattern)
        
        # Pattern 2: Exercise-Productivity correlation
        exercise_prod_pattern = self._analyze_exercise_productivity(all_entries)
        if exercise_prod_pattern:
            patterns.append(exercise_prod_pattern)
        
        # Pattern 3: Day of week patterns
        dow_patterns = self._analyze_day_of_week_patterns(all_entries)
        patterns.extend(dow_patterns)
        
        # Pattern 4: Time of day patterns
        tod_patterns = self._analyze_time_of_day_patterns(all_entries)
        patterns.extend(tod_patterns)
        
        return patterns
    
    def _analyze_sleep_mood_correlation(self, entries: List[Dict]) -> Dict:
        """Analyze correlation between sleep and next-day mood."""
        # Group entries by date
        entries_by_date = defaultdict(dict)
        
        for entry in entries:
            date = entry.get("date", "")[:10]  # Extract date part
            category = entry.get("category")
            
            if category == "sleep":
                entries_by_date[date]["sleep"] = entry
            
            if "mood" in entry and entry["mood"]:
                entries_by_date[date]["mood"] = entry["mood"]
        
        # Look for next-day correlations
        correlations = []
        dates = sorted(entries_by_date.keys())
        
        for i in range(len(dates) - 1):
            current_date = dates[i]
            next_date = dates[i + 1]
            
            if "sleep" in entries_by_date[current_date] and "mood" in entries_by_date[next_date]:
                sleep_entry = entries_by_date[current_date]["sleep"]["entry"].lower()
                mood_score = entries_by_date[next_date]["mood"]
                
                # Extract sleep quality indicators
                poor_sleep_indicators = ["poor", "bad", "terrible", "couldn't sleep", "insomnia", "restless"]
                good_sleep_indicators = ["great", "excellent", "deep", "refreshing", "well"]
                
                is_poor_sleep = any(ind in sleep_entry for ind in poor_sleep_indicators)
                is_good_sleep = any(ind in sleep_entry for ind in good_sleep_indicators)
                
                if is_poor_sleep and mood_score <= 2:
                    correlations.append("poor_sleep_low_mood")
                elif is_good_sleep and mood_score >= 4:
                    correlations.append("good_sleep_high_mood")
        
        if correlations:
            poor_sleep_count = correlations.count("poor_sleep_low_mood")
            good_sleep_count = correlations.count("good_sleep_high_mood")
            
            if poor_sleep_count > 2:
                return {
                    "pattern": "Poor sleep quality correlates with low mood the following day",
                    "confidence": min(0.9, poor_sleep_count / 10),
                    "occurrences": poor_sleep_count,
                    "recommendation": "Prioritize sleep quality to improve mood stability"
                }
            elif good_sleep_count > 2:
                return {
                    "pattern": "Good sleep quality correlates with improved mood the following day",
                    "confidence": min(0.9, good_sleep_count / 10),
                    "occurrences": good_sleep_count,
                    "recommendation": "Maintain your good sleep habits for continued mood benefits"
                }
        
        return None
    
    def _analyze_exercise_productivity(self, entries: List[Dict]) -> Dict:
        """Analyze correlation between exercise and productivity."""
        # Group by date
        entries_by_date = defaultdict(dict)
        
        for entry in entries:
            date = entry.get("date", "")[:10]
            category = entry.get("category")
            
            if category == "exercise":
                entries_by_date[date]["exercise"] = True
            if category == "work" and entry.get("productivity"):
                entries_by_date[date]["productivity"] = entry["productivity"]
        
        # Analyze same-day correlations
        exercise_prod_days = []
        no_exercise_prod_days = []
        
        for date, data in entries_by_date.items():
            if "productivity" in data:
                if "exercise" in data:
                    exercise_prod_days.append(data["productivity"])
                else:
                    no_exercise_prod_days.append(data["productivity"])
        
        if len(exercise_prod_days) > 2 and len(no_exercise_prod_days) > 2:
            avg_with_exercise = np.mean(exercise_prod_days)
            avg_without_exercise = np.mean(no_exercise_prod_days)
            
            if avg_with_exercise - avg_without_exercise > 1:
                return {
                    "pattern": "Days with exercise show higher productivity scores",
                    "confidence": min(0.85, abs(avg_with_exercise - avg_without_exercise) / 3),
                    "occurrences": len(exercise_prod_days),
                    "detail": f"Average productivity: {avg_with_exercise:.1f} with exercise vs {avg_without_exercise:.1f} without",
                    "recommendation": "Consider morning exercise to boost daily productivity"
                }
        
        return None
    
    def _analyze_day_of_week_patterns(self, entries: List[Dict]) -> List[Dict]:
        """Analyze patterns by day of week."""
        patterns = []
        
        # Group moods by day of week
        moods_by_dow = defaultdict(list)
        
        for entry in entries:
            if "mood" in entry and entry["mood"]:
                date_str = entry.get("date", "")[:10]
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    dow = date_obj.strftime("%A")
                    moods_by_dow[dow].append(entry["mood"])
                except:
                    continue
        
        # Find best and worst days
        if len(moods_by_dow) >= 3:
            avg_by_dow = {dow: np.mean(moods) for dow, moods in moods_by_dow.items() if len(moods) > 1}
            
            if avg_by_dow:
                best_day = max(avg_by_dow, key=avg_by_dow.get)
                worst_day = min(avg_by_dow, key=avg_by_dow.get)
                
                if avg_by_dow[best_day] - avg_by_dow[worst_day] > 0.5:
                    patterns.append({
                        "pattern": f"{best_day}s tend to be your best mood days, while {worst_day}s are challenging",
                        "confidence": 0.7,
                        "detail": f"Average mood: {best_day} ({avg_by_dow[best_day]:.1f}) vs {worst_day} ({avg_by_dow[worst_day]:.1f})",
                        "recommendation": f"Schedule important activities on {best_day}s when possible"
                    })
        
        return patterns
    
    def _analyze_time_of_day_patterns(self, entries: List[Dict]) -> List[Dict]:
        """Analyze patterns by time of day."""
        patterns = []
        
        # Analyze when exercise happens and its effectiveness
        exercise_times = []
        
        for entry in entries:
            if entry.get("category") == "exercise":
                time_str = entry.get("date", "")[11:16]  # Extract HH:MM
                if time_str:
                    try:
                        hour = int(time_str.split(":")[0])
                        exercise_times.append(hour)
                    except:
                        continue
        
        if len(exercise_times) > 5:
            morning_count = len([h for h in exercise_times if 5 <= h < 12])
            evening_count = len([h for h in exercise_times if 16 <= h < 22])
            
            if morning_count > evening_count * 2:
                patterns.append({
                    "pattern": "You primarily exercise in the morning",
                    "confidence": 0.8,
                    "detail": f"{morning_count} morning sessions vs {evening_count} evening sessions",
                    "recommendation": "Your morning exercise routine is consistent - keep it up!"
                })
            elif evening_count > morning_count * 2:
                patterns.append({
                    "pattern": "You primarily exercise in the evening",
                    "confidence": 0.8,
                    "detail": f"{evening_count} evening sessions vs {morning_count} morning sessions",
                    "recommendation": "Consider if evening exercise affects your sleep quality"
                })
        
        return patterns


class CoachAgent:
    """Agent for generating personalized coaching insights."""
    
    def __init__(self):
        self.reasoning_agent = ReasoningAgent()
    
    def generate_coaching_insights(self, data_store: LifelogDataStore, kpis: Dict, patterns: List[Dict]) -> List[Dict]:
        """Generate coaching insights based on KPIs and patterns."""
        insights = []
        
        # Analyze sleep insights
        sleep_insights = self._generate_sleep_insights(kpis.get("sleep", {}))
        insights.extend(sleep_insights)
        
        # Analyze mood insights
        mood_insights = self._generate_mood_insights(kpis.get("mood", {}))
        insights.extend(mood_insights)
        
        # Analyze productivity insights
        productivity_insights = self._generate_productivity_insights(kpis.get("productivity", {}))
        insights.extend(productivity_insights)
        
        # Analyze exercise insights
        exercise_insights = self._generate_exercise_insights(kpis.get("exercise", {}))
        insights.extend(exercise_insights)
        
        # Generate holistic insights based on patterns
        holistic_insights = self._generate_holistic_insights(kpis, patterns)
        insights.extend(holistic_insights)
        
        # Use AI to generate one premium insight
        ai_insight = self._generate_ai_insight(kpis, patterns)
        if ai_insight:
            insights.append(ai_insight)
        
        # Return top 5 most relevant insights
        return insights[:5]
    
    def _generate_sleep_insights(self, sleep_kpis: Dict) -> List[Dict]:
        """Generate insights about sleep."""
        insights = []
        
        if sleep_kpis.get("average_hours") and sleep_kpis["average_hours"] != "unknown":
            avg_hours = sleep_kpis["average_hours"]
            
            if avg_hours < 6:
                insights.append({
                    "category": "sleep",
                    "insight": f"Your average sleep of {avg_hours} hours is below recommended levels",
                    "recommendation": "Aim for 7-9 hours of sleep. Try setting a consistent bedtime 8 hours before your wake time.",
                    "priority": "high"
                })
            elif avg_hours > 9:
                insights.append({
                    "category": "sleep",
                    "insight": f"You're averaging {avg_hours} hours of sleep, which may indicate oversleeping",
                    "recommendation": "Consider if you're compensating for poor sleep quality. Focus on sleep consistency rather than duration.",
                    "priority": "medium"
                })
            
            if sleep_kpis.get("consistency_score") and sleep_kpis["consistency_score"] != "unknown":
                if sleep_kpis["consistency_score"] < 7:
                    insights.append({
                        "category": "sleep",
                        "insight": "Your sleep schedule varies significantly night to night",
                        "recommendation": "Set a regular sleep schedule, going to bed and waking at the same time daily, even on weekends.",
                        "priority": "high"
                    })
        
        return insights
    
    def _generate_mood_insights(self, mood_kpis: Dict) -> List[Dict]:
        """Generate insights about mood."""
        insights = []
        
        if mood_kpis.get("average"):
            avg_mood = mood_kpis["average"]
            
            if avg_mood < 3:
                insights.append({
                    "category": "mood",
                    "insight": f"Your average mood score of {avg_mood} suggests you're experiencing persistent low mood",
                    "recommendation": "Consider journaling positive experiences daily and reaching out to supportive friends or professionals.",
                    "priority": "high"
                })
            
            if mood_kpis.get("volatility") == "high":
                insights.append({
                    "category": "mood",
                    "insight": "Your mood shows high volatility with significant ups and downs",
                    "recommendation": "Track triggers for mood changes. Consider mindfulness practices to improve emotional regulation.",
                    "priority": "medium"
                })
            
            if mood_kpis.get("good_days_percentage") and mood_kpis["good_days_percentage"] < 50:
                insights.append({
                    "category": "mood",
                    "insight": f"Only {mood_kpis['good_days_percentage']}% of your days have good mood scores",
                    "recommendation": "Identify activities from your good days and intentionally schedule them more frequently.",
                    "priority": "medium"
                })
        
        return insights
    
    def _generate_productivity_insights(self, productivity_kpis: Dict) -> List[Dict]:
        """Generate insights about productivity."""
        insights = []
        
        if productivity_kpis.get("average_score"):
            avg_prod = productivity_kpis["average_score"]
            
            if avg_prod < 5:
                insights.append({
                    "category": "productivity",
                    "insight": f"Your average productivity score of {avg_prod} indicates room for improvement",
                    "recommendation": "Try time-blocking your most important tasks during your peak energy hours.",
                    "priority": "medium"
                })
            
            if productivity_kpis.get("consistency") and productivity_kpis["consistency"] != "unknown":
                if productivity_kpis["consistency"] < 6:
                    insights.append({
                        "category": "productivity",
                        "insight": "Your productivity levels are inconsistent day to day",
                        "recommendation": "Establish a morning routine to create consistent work momentum.",
                        "priority": "medium"
                    })
        
        return insights
    
    def _generate_exercise_insights(self, exercise_kpis: Dict) -> List[Dict]:
        """Generate insights about exercise."""
        insights = []
        
        if exercise_kpis.get("weekly_average"):
            weekly_avg = exercise_kpis["weekly_average"]
            
            if weekly_avg < 3:
                insights.append({
                    "category": "exercise",
                    "insight": f"You're averaging {weekly_avg} exercise sessions per week",
                    "recommendation": "Aim for at least 3-4 sessions weekly. Start with 20-minute walks if needed.",
                    "priority": "medium"
                })
            
            if exercise_kpis.get("types"):
                types = exercise_kpis["types"]
                if len(types) == 1:
                    insights.append({
                        "category": "exercise",
                        "insight": f"Your exercise routine focuses only on {list(types.keys())[0]}",
                        "recommendation": "Add variety with different exercise types for balanced fitness.",
                        "priority": "low"
                    })
        
        return insights
    
    def _generate_holistic_insights(self, kpis: Dict, patterns: List[Dict]) -> List[Dict]:
        """Generate insights that connect multiple aspects."""
        insights = []
        
        # Look for sleep-mood-productivity connections
        sleep_avg = kpis.get("sleep", {}).get("average_hours", 0)
        mood_avg = kpis.get("mood", {}).get("average", 0)
        prod_avg = kpis.get("productivity", {}).get("average_score", 0)
        
        if sleep_avg and mood_avg and prod_avg:
            if sleep_avg < 7 and mood_avg < 3 and prod_avg < 6:
                insights.append({
                    "category": "holistic",
                    "insight": "Poor sleep appears to be impacting both your mood and productivity",
                    "recommendation": "Prioritize sleep as your #1 health intervention - it will improve everything else.",
                    "priority": "high"
                })
        
        # Look for patterns mentioning correlations
        for pattern in patterns:
            if "exercise" in pattern.get("pattern", "").lower() and "productivity" in pattern.get("pattern", "").lower():
                insights.append({
                    "category": "holistic",
                    "insight": pattern["pattern"],
                    "recommendation": pattern.get("recommendation", "Maintain this positive habit"),
                    "priority": "medium"
                })
                break
        
        return insights
    
    def _generate_ai_insight(self, kpis: Dict, patterns: List[Dict]) -> Dict:
        """Use AI to generate one premium insight."""
        # Prepare context for AI
        context = f"""
        Based on this person's health data:
        
        KPIs Summary:
        - Sleep: {kpis.get('sleep', {}).get('average_hours', 'unknown')} hours average
        - Mood: {kpis.get('mood', {}).get('average', 'unknown')} average score
        - Productivity: {kpis.get('productivity', {}).get('average_score', 'unknown')} average
        - Exercise: {kpis.get('exercise', {}).get('weekly_average', 'unknown')} sessions/week
        
        Key Patterns:
        {chr(10).join([f"- {p['pattern']}" for p in patterns[:3]])}
        
        Generate ONE specific, actionable insight that connects multiple aspects of their health.
        Focus on what would have the biggest positive impact.
        """
        
        try:
            ai_response = self.reasoning_agent.generate(
                context,
                system_prompt="You are a health coach. Provide ONE specific, actionable recommendation based on the data patterns. Be concise and practical. Do NOT include any thinking process, XML tags, or meta-commentary. Just provide the direct recommendation in 1-2 sentences.",
                max_tokens=300
            )
            
            # Clean up AI response - remove any thinking tags if present
            clean_response = ai_response.strip()
            
            if "<think>" in clean_response:
                # Extract only content after thinking
                parts = clean_response.split("</think>")
                if len(parts) > 1:
                    clean_response = parts[-1].strip()
                else:
                    # Fallback if no closing tag
                    clean_response = "Focus on improving your sleep quality by maintaining a consistent 7-8 hour sleep schedule."
            
            # Ensure it doesn't start with tags
            if clean_response.startswith("<"):
                clean_response = "Focus on improving your sleep quality by maintaining a consistent 7-8 hour sleep schedule."
            
            # Ensure we have a complete sentence
            if len(clean_response) > 250:
                # Find the last complete sentence within 250 chars
                cutoff = clean_response[:250].rfind('.')
                if cutoff > 0:
                    clean_response = clean_response[:cutoff + 1]
                else:
                    clean_response = clean_response[:247] + "..."
            
            return {
                "category": "ai_generated",
                "insight": "Personalized Health Insight",
                "recommendation": clean_response,
                "priority": "high"
            }
        except Exception as e:
            # Fallback if AI fails - provide a generic but useful insight
            print(f"AI insight generation failed: {e}")
            
            # Generate fallback based on available data
            if kpis.get('sleep', {}).get('average_hours') and kpis['sleep']['average_hours'] != 'unknown':
                if kpis['sleep']['average_hours'] < 7:
                    return {
                        "category": "ai_generated",
                        "insight": "Sleep Optimization Needed",
                        "recommendation": "Your average sleep of {:.1f} hours is below optimal. Aim for 7-8 hours nightly by setting a consistent bedtime routine.".format(kpis['sleep']['average_hours']),
                        "priority": "high"
                    }
            
            if kpis.get('exercise', {}).get('weekly_average'):
                if kpis['exercise']['weekly_average'] < 3:
                    return {
                        "category": "ai_generated", 
                        "insight": "Increase Activity Level",
                        "recommendation": "With only {:.1f} exercise sessions per week, try adding 10-minute walks to reach the recommended 3-4 sessions.".format(kpis['exercise']['weekly_average']),
                        "priority": "high"
                    }
            
            # Generic fallback
            return {
                "category": "ai_generated",
                "insight": "Holistic Health Focus",
                "recommendation": "Focus on the fundamentals: 7-8 hours of sleep, 3-4 exercise sessions weekly, and tracking your mood patterns for better self-awareness.",
                "priority": "medium"
            }


class BackgroundAnalyzer:
    """Main class for running all background analysis at startup."""
    
    def __init__(self, data_store: LifelogDataStore):
        """Initialize with data store and all agents."""
        self.data_store = data_store
        self.kpi_agent = KPIAgent()
        self.pattern_agent = PatternAgent()
        self.coach_agent = CoachAgent()
        self.cache_file = "data/insights_cache.json"
    
    def run_analysis(self):
        """Run all background agents and save insights to cache."""
        print("🔄 Starting background analysis...")
        
        # Calculate KPIs
        print("📊 Calculating KPIs...")
        kpis = self.kpi_agent.calculate_kpis(self.data_store)
        
        # Detect patterns
        print("🔍 Detecting patterns...")
        patterns = self.pattern_agent.detect_patterns(self.data_store)
        
        # Generate coaching insights
        print("💡 Generating coaching insights...")
        coaching = self.coach_agent.generate_coaching_insights(self.data_store, kpis, patterns)
        
        # Compile all insights
        insights = {
            "kpis": kpis,
            "patterns": patterns,
            "coaching": coaching,
            "generated_at": datetime.now().isoformat(),
            "total_entries_analyzed": len(self.data_store.get_all_entries())
        }
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save to cache file
        with open(self.cache_file, "w") as f:
            json.dump(insights, f, indent=2)
        
        print(f"✅ Background analysis complete! Saved to {self.cache_file}")
        print(f"   - KPIs calculated: {len(kpis)}")
        print(f"   - Patterns detected: {len(patterns)}")
        print(f"   - Coaching insights: {len(coaching)}")
        
        return insights
