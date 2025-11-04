"""Chat API endpoints including WebSocket support."""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse, StreamingResponse
import json
import asyncio

from backend.models.schemas import ChatRequest, ChatResponse, ChatMessage, WSMessage
from backend.services.workflow import WorkflowService

router = APIRouter()

# In-memory chat history (in production, use a database)
chat_history: List[ChatMessage] = []


async def get_workflow_service():
    """Dependency to get workflow service."""
    from backend.main import app
    return WorkflowService(app.state.workflow)


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Process a chat message and return response."""
    try:
        # Add user message to history
        user_message = ChatMessage(
            role="user",
            content=request.message,
            timestamp=datetime.now()
        )
        chat_history.append(user_message)
        
        # Process message through workflow
        start_time = datetime.now()
        result = await workflow_service.process_message(request.message)
        elapsed_time = (datetime.now() - start_time).total_seconds()
        
        if result["success"]:
            # Add assistant message to history
            assistant_message = ChatMessage(
                role="assistant",
                content=result["response"],
                timestamp=datetime.now(),
                reasoning_steps=result.get("reasoning_steps", []),
                safety_checks=result.get("safety_checks", []),
                metrics={
                    "react_cycles": result.get("react_cycles", 0),
                    "retrieved_entries": result.get("retrieved_entries", 0),
                    "elapsed_time": elapsed_time
                }
            )
            chat_history.append(assistant_message)
            
            return ChatResponse(
                success=True,
                response=result["response"],
                reasoning_steps=result.get("reasoning_steps", []),
                safety_checks=result.get("safety_checks", []),
                react_cycles=result.get("react_cycles", 0),
                retrieved_entries=result.get("retrieved_entries", 0),
                elapsed_time=elapsed_time
            )
        else:
            error_msg = result.get("error", "Unknown error occurred")
            raise HTTPException(status_code=500, detail=error_msg)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[ChatMessage])
async def get_chat_history(limit: Optional[int] = None):
    """Get chat history."""
    if limit:
        return chat_history[-limit:]
    return chat_history


@router.delete("/history")
async def clear_chat_history():
    """Clear chat history."""
    chat_history.clear()
    return {"message": "Chat history cleared"}


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """WebSocket endpoint for streaming chat responses."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            if not message:
                await websocket.send_json({
                    "type": "error",
                    "content": "No message provided"
                })
                continue
            
            # Add user message to history
            user_message = ChatMessage(
                role="user",
                content=message,
                timestamp=datetime.now()
            )
            chat_history.append(user_message)
            
            # Stream the workflow execution
            try:
                async for event in workflow_service.stream_message(message):
                    ws_message = WSMessage(
                        type=event["type"],
                        content=event.get("content"),
                        reasoning_step=event.get("reasoning_step"),
                        metrics=event.get("metrics")
                    )
                    await websocket.send_json(ws_message.dict())
                    
                    # If this is the final message, add to history
                    if event["type"] == "final" and event.get("success"):
                        assistant_message = ChatMessage(
                            role="assistant",
                            content=event.get("response", ""),
                            timestamp=datetime.now(),
                            reasoning_steps=event.get("reasoning_steps", []),
                            safety_checks=event.get("safety_checks", []),
                            metrics={
                                "react_cycles": event.get("react_cycles", 0),
                                "retrieved_entries": event.get("retrieved_entries", 0),
                                "elapsed_time": event.get("elapsed_time", 0)
                            }
                        )
                        chat_history.append(assistant_message)
                        
            except Exception as e:
                error_message = WSMessage(
                    type="error",
                    content=f"Error processing message: {str(e)}"
                )
                await websocket.send_json(error_message.dict())
                
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Stream chat response using Server-Sent Events."""
    
    async def event_generator():
        try:
            # Stream the LangGraph execution
            async for event in workflow_service.workflow.graph.astream({
                "query": request.message,
                "reasoning_steps": [],
                "safety_checks": [],
                "react_context": {},
                "observations": [],
                "iteration_count": 0,
                "should_continue": True
            }):
                # Send each event as SSE
                node_name = list(event.keys())[0]
                node_data = event[node_name]
                
                data = json.dumps({
                    "type": "intermediate",
                    "node": node_name,
                    "data": node_data
                })
                yield f"data: {data}\n\n"
                
                # Small delay to prevent overwhelming the client
                await asyncio.sleep(0.01)
            
            # Send final event
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
        except Exception as e:
            # Send error event
            error_data = json.dumps({
                "type": "error",
                "error": str(e)
            })
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable Nginx buffering
        }
    )
