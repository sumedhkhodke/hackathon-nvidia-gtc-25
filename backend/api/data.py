"""Data retrieval API endpoints."""
from typing import List, Optional
import pandas as pd
import numpy as np
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from backend.models.schemas import (
    SystemStats, 
    LifelogEntry, 
    DataInsights,
    CategorySummary,
    CorrelationData
)

router = APIRouter()


@router.get("/stats", response_model=SystemStats)
async def get_system_stats():
    """Get system statistics."""
    try:
        from backend.main import app
        stats = app.state.stats
        
        return SystemStats(
            total_entries=stats.get("total_entries", 0),
            collection_name=stats.get("collection_name", "lifelog_entries"),
            status=stats.get("status", "Ready")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entries", response_model=List[LifelogEntry])
async def get_lifelog_entries(
    limit: Optional[int] = Query(default=50, description="Number of entries to return"),
    offset: Optional[int] = Query(default=0, description="Number of entries to skip"),
    category: Optional[str] = Query(default=None, description="Filter by category")
):
    """Get lifelog entries with pagination."""
    try:
        # Load the CSV data
        df = pd.read_csv("data/sample_lifelog.csv")
        df['date'] = pd.to_datetime(df['date'])
        
        # Apply category filter if provided
        if category:
            df = df[df['category'] == category]
        
        # Sort by date descending
        df = df.sort_values('date', ascending=False)
        
        # Apply pagination
        df_page = df.iloc[offset:offset + limit]
        
        # Convert to response model
        entries = []
        for _, row in df_page.iterrows():
            entries.append(LifelogEntry(
                date=row['date'],
                category=row['category'],
                entry=row['entry'],
                mood_score=row['mood_score']
            ))
        
        return entries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights", response_model=DataInsights)
async def get_data_insights():
    """Get aggregated data insights."""
    try:
        # Load the CSV data
        df = pd.read_csv("data/sample_lifelog.csv")
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculate category summaries
        category_summaries = []
        for category in df['category'].unique():
            cat_df = df[df['category'] == category]
            category_summaries.append(CategorySummary(
                category=category,
                average_score=float(cat_df['mood_score'].mean()),
                entry_count=len(cat_df),
                min_score=int(cat_df['mood_score'].min()),
                max_score=int(cat_df['mood_score'].max())
            ))
        
        # Calculate overall statistics
        insights = DataInsights(
            total_entries=len(df),
            date_range={
                "start": df['date'].min().isoformat(),
                "end": df['date'].max().isoformat()
            },
            overall_average_score=float(df['mood_score'].mean()),
            category_summaries=category_summaries
        )
        
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/correlations", response_model=CorrelationData)
async def get_correlation_data():
    """Get correlation matrix between categories."""
    try:
        # Load the CSV data
        df = pd.read_csv("data/sample_lifelog.csv")
        df['date'] = pd.to_datetime(df['date'])
        
        # Pivot to get categories as columns
        pivot_df = df.pivot_table(
            index='date', 
            columns='category', 
            values='mood_score',
            aggfunc='mean'  # Handle multiple entries per date
        )
        
        # Calculate correlation matrix
        corr_matrix = pivot_df.corr()
        
        # Convert to response format
        categories = corr_matrix.columns.tolist()
        matrix = corr_matrix.values.tolist()
        
        # Replace NaN with None for JSON serialization
        matrix = [[None if np.isnan(x) else round(x, 3) for x in row] for row in matrix]
        
        return CorrelationData(
            categories=categories,
            correlation_matrix=matrix
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeline")
async def get_timeline_data(
    category: Optional[str] = Query(default=None, description="Filter by category")
):
    """Get timeline data for charts."""
    try:
        # Load the CSV data
        df = pd.read_csv("data/sample_lifelog.csv")
        df['date'] = pd.to_datetime(df['date'])
        
        # Apply category filter if provided
        if category:
            df = df[df['category'] == category]
        
        # Sort by date
        df = df.sort_values('date')
        
        # Group by date and category for timeline
        timeline_data = []
        for _, row in df.iterrows():
            timeline_data.append({
                "date": row['date'].isoformat(),
                "category": row['category'],
                "mood_score": row['mood_score'],
                "entry": row['entry']
            })
        
        return {"data": timeline_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
