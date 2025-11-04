"""Pydantic models for API requests and responses."""
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field


# Chat related models
class ChatRequest(BaseModel):
    """Request model for chat messages."""
    message: str = Field(..., description="The user's message")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation context")


class ReasoningStep(BaseModel):
    """Model for a reasoning step in the agent workflow."""
    step: str = Field(..., description="Step title/name")
    description: str = Field(..., description="Description of what happened in this step")


class SafetyCheck(BaseModel):
    """Model for a safety check result."""
    type: str = Field(..., description="Type of safety check (input/output)")
    is_safe: bool = Field(..., description="Whether the content is safe")
    category: Optional[str] = Field(None, description="Category of safety issue if unsafe")
    should_block: bool = Field(False, description="Whether to block the message")
    needs_modification: Optional[bool] = Field(None, description="Whether output needs modification")


class ChatResponse(BaseModel):
    """Response model for chat messages."""
    success: bool
    response: str
    reasoning_steps: List[ReasoningStep] = []
    safety_checks: List[SafetyCheck] = []
    react_cycles: int = 0
    retrieved_entries: int = 0
    elapsed_time: float = 0.0
    error: Optional[str] = None


class ChatMessage(BaseModel):
    """Model for a chat message in history."""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime
    reasoning_steps: Optional[List[ReasoningStep]] = None
    safety_checks: Optional[List[SafetyCheck]] = None
    metrics: Optional[Dict[str, Any]] = None


# WebSocket models
class WSMessage(BaseModel):
    """WebSocket message format."""
    type: str = Field(..., description="Message type (intermediate/final/error)")
    content: Optional[str] = None
    reasoning_step: Optional[ReasoningStep] = None
    metrics: Optional[Dict[str, Any]] = None


# Data related models
class SystemStats(BaseModel):
    """System statistics model."""
    total_entries: int
    collection_name: str
    status: str


class LifelogEntry(BaseModel):
    """Model for a lifelog entry."""
    date: datetime
    category: str
    entry: str
    mood_score: int = Field(..., ge=1, le=5, description="Mood score from 1 to 5")


class CategorySummary(BaseModel):
    """Summary statistics for a category."""
    category: str
    average_score: float
    entry_count: int
    min_score: int
    max_score: int


class DataInsights(BaseModel):
    """Aggregated data insights."""
    total_entries: int
    date_range: Dict[str, str]
    overall_average_score: float
    category_summaries: List[CategorySummary]


class CorrelationData(BaseModel):
    """Correlation matrix data."""
    categories: List[str]
    correlation_matrix: List[List[Optional[float]]]


# System related models
class AgentInfo(BaseModel):
    """Information about an agent in the system."""
    name: str
    model: str
    description: str
    icon: str
    status: str = Field(..., description="active/inactive")


class SystemArchitecture(BaseModel):
    """System architecture information."""
    title: str
    description: str
    components: Dict[str, Dict[str, Union[str, List[str]]]]
    workflow: Dict[str, str]
    tech_stack: Dict[str, List[str]]


# Request/Response models for timeline
class TimelineRequest(BaseModel):
    """Request for timeline data."""
    category: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TimelineDataPoint(BaseModel):
    """A single data point in the timeline."""
    date: str
    category: str
    mood_score: int
    entry: str


class TimelineResponse(BaseModel):
    """Response containing timeline data."""
    data: List[TimelineDataPoint]
