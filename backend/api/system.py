"""System information API endpoints."""
from typing import List, Dict
from fastapi import APIRouter, HTTPException

from backend.models.schemas import AgentInfo, SystemArchitecture

router = APIRouter()


@router.get("/agents", response_model=List[AgentInfo])
async def get_active_agents():
    """Get information about active agents."""
    agents = [
        AgentInfo(
            name="Reasoning Agent",
            model="Nemotron Super 49B v1.5",
            description="High-level reasoning & synthesis, pattern identification, hypothesis generation",
            icon="🧠",
            status="active"
        ),
        AgentInfo(
            name="ReAct Agent",
            model="Nemotron Super 49B v1.5",
            description="Iterative reasoning loops, action planning & observation, adaptive decision-making",
            icon="🔄",
            status="active"
        ),
        AgentInfo(
            name="Query Analyzer",
            model="Nemotron Nano 9B v2",
            description="Fast intent extraction, tool selection, optimized for speed",
            icon="⚡",
            status="active"
        ),
        AgentInfo(
            name="Safety Guard",
            model="Nemotron Safety 8B v3",
            description="Dual checkpoint system, 23 unsafe categories, privacy protection",
            icon="🛡️",
            status="active"
        ),
        AgentInfo(
            name="Analysis Agent",
            model="Nemotron Super 49B",
            description="Runs on historical data, calculates KPIs, triggered separately/scheduled",
            icon="📊",
            status="inactive"  # Not implemented in MVP
        ),
        AgentInfo(
            name="Coach Agent",
            model="Nemotron Super 49B",
            description="Uses KPIs from Analysis Agent, generates personalized coaching insights",
            icon="🎯",
            status="inactive"  # Not implemented in MVP
        )
    ]
    
    return agents


@router.get("/architecture", response_model=SystemArchitecture)
async def get_system_architecture():
    """Get system architecture information."""
    return SystemArchitecture(
        title="Multi-Agent Architecture",
        description="Sophisticated multi-agent architecture using NVIDIA Nemotron models, orchestrated by LangGraph",
        components={
            "capture_store": {
                "title": "Capture & Store",
                "items": [
                    "User data streams normalization",
                    "Vector DB with NVIDIA embeddings",
                    "Metadata storage"
                ]
            },
            "background_analysis": {
                "title": "Background Analysis",
                "items": [
                    "Analysis agent for KPI computation",
                    "Coach agent for insights generation",
                    "Insights cache for fast retrieval"
                ]
            },
            "conversational_coach": {
                "title": "Conversational Coach",
                "items": [
                    "ReAct orchestrator",
                    "Vector DB search",
                    "Insights tool integration",
                    "Response synthesis with safety checks"
                ]
            }
        },
        workflow={
            "input_safety": "Validate user input with Nemotron Safety Guard",
            "react_loop": "1-3 cycles of Reason → Act → Observe",
            "synthesis": "Generate insights from gathered information",
            "output_safety": "Validate AI response before returning"
        },
        tech_stack={
            "ai_models": [
                "Nemotron Super 49B v1.5",
                "Nemotron Safety 8B v3",
                "Nemotron Nano 9B v2",
                "NVIDIA NIM APIs"
            ],
            "orchestration": [
                "LangGraph",
                "Python OpenAI Client",
                "FastAPI"
            ],
            "data_storage": [
                "ChromaDB with NVIDIA embeddings",
                "Pandas",
                "Vector Embeddings"
            ]
        }
    )


@router.get("/features")
async def get_system_features():
    """Get key features demonstrated by the system."""
    features = {
        "agentic_behavior": "Autonomous reasoning and decision-making",
        "react_pattern": "Reason → Act → Observe cycles for complex problem-solving",
        "multi_agent": "Specialized agents working in coordination via LangGraph",
        "background_processing": "Async Analysis & Coach agents for KPI-driven insights",
        "safety_guardrails": "Dual safety checks on input and output",
        "agentic_rag": "Intelligent retrieval-augmented generation",
        "tool_integration": "Vector DB querying and data analysis",
        "state_management": "LangGraph for stateful workflows",
        "privacy_by_design": "Local-first data architecture",
        "nvidia_embeddings": "NVIDIA NeMo Retriever embeddings for better retrieval"
    }
    
    return {"features": features}


@router.get("/demo-questions")
async def get_demo_questions():
    """Get demo questions for quick testing."""
    questions = [
        "What patterns do you see in my sleep quality?",
        "How does exercise impact my mood and energy levels?",
        "What's the relationship between my work productivity and sleep?",
        "When do I feel most productive during the week?",
        "What recommendations do you have for improving my overall well-being?",
        "Are there any correlations between my daily activities and mood scores?"
    ]
    
    return {"questions": questions}
