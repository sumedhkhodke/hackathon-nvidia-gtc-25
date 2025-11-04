"""Workflow service wrapper for async operations."""
import asyncio
from typing import Dict, AsyncGenerator, Any
from datetime import datetime

from src.agentic_workflow import LifelogAgentWorkflow


class WorkflowService:
    """Service wrapper for the agentic workflow to handle async operations."""
    
    def __init__(self, workflow: LifelogAgentWorkflow):
        """Initialize with an existing workflow instance."""
        self.workflow = workflow
    
    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process a message asynchronously.
        
        Args:
            message: User's message to process
            
        Returns:
            Dictionary with response and metadata
        """
        # Run the synchronous workflow in an executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.workflow.run, message)
        return result
    
    async def stream_message(self, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream the message processing for WebSocket updates.
        
        Args:
            message: User's message to process
            
        Yields:
            Dictionary events with intermediate and final results
        """
        start_time = datetime.now()
        
        try:
            # Since the original workflow has a stream method, we'll use it
            # but wrap it for async operation
            loop = asyncio.get_event_loop()
            
            # Create a queue to handle the streaming
            queue = asyncio.Queue()
            
            def stream_handler():
                """Run the stream in a thread and put results in queue."""
                try:
                    for event in self.workflow.stream(message):
                        # Put event in queue
                        asyncio.run_coroutine_threadsafe(
                            queue.put(event), loop
                        )
                    # Signal completion
                    asyncio.run_coroutine_threadsafe(
                        queue.put(None), loop
                    )
                except Exception as e:
                    # Put error in queue
                    asyncio.run_coroutine_threadsafe(
                        queue.put({"type": "error", "error": str(e)}), loop
                    )
            
            # Run stream handler in executor
            loop.run_in_executor(None, stream_handler)
            
            # Yield events from queue
            while True:
                event = await queue.get()
                
                if event is None:
                    # Stream completed
                    break
                
                # Add elapsed time to events
                if event.get("type") in ["intermediate", "final"]:
                    event["elapsed_time"] = (datetime.now() - start_time).total_seconds()
                
                yield event
                
        except Exception as e:
            yield {
                "type": "error",
                "error": str(e),
                "elapsed_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow statistics.
        
        Returns:
            Dictionary with workflow stats
        """
        # For now, just return basic info
        # In a real app, this could track usage, performance, etc.
        return {
            "status": "ready",
            "max_iterations": self.workflow.max_iterations,
            "agents": {
                "query_analyzer": "active",
                "reasoning_agent": "active", 
                "safety_guard": "active",
                "react_agent": "active"
            }
        }
