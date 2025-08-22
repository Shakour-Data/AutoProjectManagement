#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/sse_endpoints.py
File: sse_endpoints.py
Purpose: Server-Sent Events (SSE) endpoints for real-time updates
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: SSE implementation for browser-compatible real-time event streaming
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import real-time service
try:
    from autoprojectmanagement.api.realtime_service import EventService, EventType, Connection, event_service
except ImportError:
    # Handle import for development
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.api.realtime_service import EventService, EventType, Connection, event_service

# Create router
router = APIRouter(prefix="/sse", tags=["Server-Sent Events"])

class SSEConnection(Connection):
    """SSE connection for Server-Sent Events."""
    
    def __init__(self, connection_id: str):
        super().__init__(connection_id)
        self.message_queue: asyncio.Queue = asyncio.Queue()
    
    async def send(self, message: Dict[str, Any]):
        """Add message to SSE queue."""
        await self.message_queue.put(message)
        self.update_activity()
    
    async def get_messages(self) -> AsyncGenerator[str, None]:
        """Generator for SSE messages."""
        while True:
            try:
                message = await self.message_queue.get()
                yield f"data: {json.dumps(message)}\n\n"
                self.message_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in SSE message generator: {e}")
                break

class SSEConnectionManager:
    """Manager for SSE connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, SSEConnection] = {}
    
    async def create_connection(self) -> SSEConnection:
        """Create a new SSE connection."""
        connection_id = event_service.generate_connection_id()
        connection = SSEConnection(connection_id)
        
        await event_service.register_connection(connection)
        self.active_connections[connection_id] = connection
        
        logger.info(f"New SSE connection: {connection_id}. Total: {len(self.active_connections)}")
        return connection
    
    async def close_connection(self, connection_id: str):
        """Close SSE connection."""
        if connection_id in self.active_connections:
            await event_service.unregister_connection(connection_id)
            del self.active_connections[connection_id]
            logger.info(f"SSE connection closed: {connection_id}. Total: {len(self.active_connections)}")

# Global SSE connection manager
sse_manager = SSEConnectionManager()

class SSESubscriptionRequest(BaseModel):
    """Model for SSE subscription requests."""
    event_types: List[str] = Field(..., description="Event types to subscribe to")
    project_id: Optional[str] = Field(None, description="Project ID filter")
    last_event_id: Optional[str] = Field(None, description="Last received event ID for reconnection")

@router.get("/events")
async def sse_endpoint(
    request: Request,
    event_types: Optional[str] = Query(None, description="Comma-separated event types to subscribe to"),
    project_id: Optional[str] = Query(None, description="Project ID filter"),
    last_event_id: Optional[str] = Query(None, description="Last received event ID")
):
    """
    Server-Sent Events endpoint for real-time updates.
    
    Provides event streaming for browser clients with support for:
    - Event type subscriptions
    - Project filtering
    - Reconnection with last event ID
    - Heartbeat messages
    """
    try:
        # Create SSE connection
        connection = await sse_manager.create_connection()
        
        # Parse event types from query parameter
        subscribed_event_types = []
        if event_types:
            for event_type_str in event_types.split(','):
                try:
                    event_type = EventType(event_type_str.strip())
                    event_service.subscribe(connection.connection_id, event_type)
                    subscribed_event_types.append(event_type.value)
                except ValueError:
                    logger.warning(f"Invalid event type in SSE request: {event_type_str}")
        
        # Set project filter
        if project_id:
            event_service.set_project_filter(connection.connection_id, project_id)
        
        # Handle reconnection with last event ID
        if last_event_id:
            logger.info(f"SSE reconnection with last_event_id: {last_event_id}")
            # In a real implementation, you might want to send missed events here
        
        async def event_generator():
            """Generator for SSE events."""
            try:
                # Send initial connection message
                initial_message = {
                    "type": "connection_established",
                    "connection_id": connection.connection_id,
                    "timestamp": datetime.now().isoformat(),
                    "message": "SSE connection established",
                    "subscribed_event_types": subscribed_event_types,
                    "project_id": project_id
                }
                yield f"data: {json.dumps(initial_message)}\n\n"
                
                # Send heartbeat every 30 seconds to keep connection alive
                heartbeat_task = asyncio.create_task(_send_heartbeats(connection))
                
                # Stream messages from connection
                async for message in connection.get_messages():
                    yield message
                    
            except asyncio.CancelledError:
                logger.info(f"SSE connection cancelled: {connection.connection_id}")
            except Exception as e:
                logger.error(f"Error in SSE event generator: {e}")
            finally:
                heartbeat_task.cancel()
                await sse_manager.close_connection(connection.connection_id)
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
            }
        )
        
    except Exception as e:
        logger.error(f"Error creating SSE connection: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating SSE stream: {str(e)}")

async def _send_heartbeats(connection: SSEConnection):
    """Send heartbeat messages to keep SSE connection alive."""
    try:
        while True:
            await asyncio.sleep(30)  # Send heartbeat every 30 seconds
            heartbeat_message = {
                "type": "heartbeat",
                "timestamp": datetime.now().isoformat(),
                "message": "SSE connection heartbeat"
            }
            await connection.send(heartbeat_message)
    except asyncio.CancelledError:
        logger.debug(f"Heartbeat task cancelled for connection: {connection.connection_id}")
    except Exception as e:
        logger.error(f"Error in heartbeat task: {e}")

@router.post("/subscribe")
async def sse_subscribe(subscription: SSESubscriptionRequest):
    """
    Update SSE subscription for an existing connection.
    
    Note: This is a placeholder for future implementation where we might
    want to support dynamic subscription changes without reconnecting.
    """
    # In a real implementation, you would manage connection IDs and update subscriptions
    # For now, clients should reconnect with new subscription parameters
    return {
        "message": "SSE subscriptions updated on reconnect",
        "event_types": subscription.event_types,
        "project_id": subscription.project_id
    }

@router.get("/stats")
async def get_sse_stats():
    """Get SSE connection statistics."""
    try:
        stats = event_service.get_connection_stats()
        return {
            "sse_connections": len(sse_manager.active_connections),
            "total_connections": stats["total_connections"],
            "subscription_counts": stats["subscription_counts"],
            "message_queue_size": stats["message_queue_size"]
        }
    except Exception as e:
        logger.error(f"Error getting SSE stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

# Utility function for testing SSE
@router.post("/test-event")
async def test_sse_event(
    event_type: str = Query(..., description="Event type for test"),
    project_id: Optional[str] = Query(None, description="Project ID for test")
):
    """Send a test event to all SSE subscribers (for development/testing)."""
    try:
        from autoprojectmanagement.api.realtime_service import Event, EventType
        
        event = Event(
            type=EventType(event_type),
            data={
                "test": True,
                "message": "Test event from SSE endpoint",
                "timestamp": time.time()
            },
            project_id=project_id
        )
        
        await event_service.publish_event(event)
        
        return {
            "message": f"Test {event_type} event published",
            "project_id": project_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid event type: {event_type}")
    except Exception as e:
        logger.error(f"Error publishing test event: {e}")
        raise HTTPException(status_code=500, detail=f"Error publishing test event: {str(e)}")
