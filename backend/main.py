"""FastAPI main application for Agentic Lifelog."""
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

# Add parent directory to path so we can import src modules
sys.path.append(str(Path(__file__).parent.parent))

from src.data_store import LifelogDataStore
from src.agentic_workflow import LifelogAgentWorkflow

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - initialize resources on startup."""
    # Initialize data store
    try:
        app.state.data_store = LifelogDataStore()
        count = app.state.data_store.load_and_store_csv("data/sample_lifelog.csv")
        print(f"✅ Loaded {count} entries into vector database")
        
        # Initialize workflow
        app.state.workflow = LifelogAgentWorkflow(app.state.data_store)
        print("✅ Initialized agentic workflow")
        
        # Get stats
        app.state.stats = app.state.data_store.get_stats()
        print(f"📊 System ready with {app.state.stats['total_entries']} entries")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        raise
    
    yield
    
    # Cleanup (if needed)
    print("👋 Shutting down application")


# Create FastAPI app
app = FastAPI(
    title="Agentic Lifelog API",
    description="Backend API for NVIDIA GTC Hackathon 2025 - Nemotron Prize Track",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Agentic Lifelog API",
        "version": "1.0.0",
        "description": "NVIDIA GTC Hackathon 2025 - Nemotron Prize Track",
        "endpoints": {
            "chat": "/api/chat",
            "data": "/api/data",
            "system": "/api/system",
            "websocket": "/ws/chat"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        stats = app.state.stats
        return {
            "status": "healthy",
            "data_store": "connected",
            "total_entries": stats.get("total_entries", 0),
            "workflow": "ready"
        }
    except:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": "Services not initialized"}
        )


# Import and include routers
from backend.api import chat, data, system

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(system.router, prefix="/api/system", tags=["system"])


if __name__ == "__main__":
    # Run with uvicorn when executed directly
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
