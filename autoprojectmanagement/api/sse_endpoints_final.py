#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/sse_endpoints_final.py
File: sse_endpoints_final.py
Purpose: Complete Server-Sent Events (SSE) endpoints for real-time updates
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Complete SSE implementation for browser-compatible real-time event streaming
"""

import asyncio
import json
import logging
import time
import uuid
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
    """SSE connection for Server-Sent Events with proper event service integration."""
    
    def __init__(self, connection_id: str):
        super().__init__(connection_id)
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.last_event_id: Optional[str] = None
    
    async def send(self, message: Dict[str, Any]):
        """Send message through SSE with proper formatting."""
        try:
            # Add event ID for reconnection support
            event_id = str(uuid.uuid4())
            message['event_id'] = event_id
            self.last_event_id = event_id
            
            await self.message_queue.put(message)
            self.update_activity()
            logger.debug(f"Message queued for SSE connection {self.connection_id}: {message['type']}")
        except Exception as e:
            logger.error(f"Error sending message to SSE connection {self.connection_id}: {e}")
            raise
    
    async def get_messages(self) -> AsyncGenerator[str, None]:
        """Generator for SSE messages with proper SSE protocol formatting."""
        while True:
            try:
                message = await self.message_queue.get()
                
                # Format according to SSE specification
                event_id = message.get('event_id', '')
                event_type = message.get('type', 'message')
                data = json.dumps(message)
                
                # Build SSE message with proper fields
                sse_message = f"id: {event_id}\n"
                sse_message += f"event: {event_type}\n"
                sse_message += f"data: {data}\n\n"
                
                yield sse_message
                self.message_queue.task_done()
                
            except asyncio.CancelledError:
                logger.debug(f"SSE message generator cancelled for {self.connection_id}")
                break
            except Exception as e:
                logger.error(f"Error in SSE message generator for {self.connection极}: {e}")
                break

class SSEConnectionManager:
    """Manager for SSE connections with proper integration."""
    
    def __init__(self):
        self.active_connections: Dict[str, SSEConnection] = {}
    
    async def create_connection(self) -> SSEConnection:
        """Create a new SSE connection and register with event service."""
        connection_id = event_service.generate_connection_id()
        connection = SSEConnection(connection_id)
        
        await event_service.register_connection(connection)
        self.active_connections[connection_id] = connection
        
        logger.info(f"New SSE connection: {connection_id}. Total: {len(self.active_connections)}")
        return connection
    
    async def close_connection(self, connection_id: str):
        """Close SSE connection and clean up resources."""
        if connection_id in self.active_connections:
            try:
                await event_service.unregister_connection(connection_id)
                del self.active_connections[connection_id]
                logger.info(f"SSE connection closed: {connection_id}. Total: {len(self.active_connections)}")
            except Exception as e:
                logger.error(f"Error closing SSE connection {connection_id}: {e}")
    
    async def handle_subscription(self, connection_id: str, event_types: List[str], project_id: Optional[str] = None):
        """Handle subscription request for SSE connection."""
        if connection_id not in self.active_connections:
            logger.warning(f"Connection {connection_id} not found for subscription")
            return
        
        connection = self.active_connections[connection_id]
        
        # Clear existing subscriptions
        for event_type in list(connection.subscriptions):
            event_service.unsubscribe(connection_id, event_type)
        
        # Add new subscriptions
        subscribed_types = []
        for event_type_str in event_types:
            try:
                event_type = EventType(event_type_str.strip())
                event_service.subscribe(connection_id, event_type)
                subscribed_types.append(event_type.value)
                logger.debug(f"SSE connection {connection_id} subscribed to {event_type}")
            except ValueError:
                logger.warning(f"Invalid event type in SSE subscription: {event_type_str}")
        
        # Set project filter
        event_service.set_project_filter(connection_id, project_id)
        
        logger.info(f"SSE connection {connection_id} subscriptions updated: {subscribed_types}, project: {project_id}")
        return subscribed_types

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
    - Automatic reconnection
    """
    try:
        # Create SSE connection
        connection = await sse_manager.create_connection()
        
        # Parse event types from query parameter
        subscribed_event_types = []
        if event_types:
            event_type_list = [et.strip() for et in event_types.split(',') if et.strip()]
            subscribed_event_types = await sse_manager.handle_subscription(
                connection.connection_id, event_type_list, project_id
            )
        
        # Handle reconnection with last event ID
        missed_events = []
        if last_event_id:
            logger.info(f"SSE reconnection with last_event_id: {last_event_id}")
            # In a production system, you might retrieve missed events from a persistent store
            missed_events.append({
                "type": "reconnection",
                "message": "Reconnected with last event ID",
                "last_event_id": last_event_id,
                "timestamp": datetime.now().isoformat()
            })
        
        async def event_generator():
            """Generator for SSE events with proper error handling."""
            heartbeat_task = None
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
                
                # Send any missed events for reconnection
                for missed_event in missed_events:
                    yield f"data: {json.dumps(missed_event)}\n\n"
                
                # Send heartbeat every 30 seconds to keep connection alive
                heartbeat_task = asyncio.create_task(_send_heartbeats(connection))
                
                # Stream messages from connection with timeout handling
                async for message in connection.get_messages():
                    yield message
                    
            except asyncio.CancelledError:
                logger.info(f"SSE connection cancelled: {connection.connection_id}")
            except Exception as e:
                logger.error(f"Error in SSE event generator for {connection.connection_id}: {e}")
            finally:
                if heartbeat_task:
                    heartbeat_task.cancel()
                    try:
                        await heartbeat_task
                    except asyncio.CancelledError:
                        pass
                await sse_manager.close_connection(connection.connection_id)
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "X-Accel-Buffering": "no"  # Disable buffering for nginx
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
                "message": "SSE connection heartbeat",
                "connection_id": connection.connection_id
            }
            await connection.send(heartbeat_message)
            logger.debug(f"Heartbeat sent to SSE connection {connection.connection_id}")
    except asyncio.CancelledError:
        logger.debug(f"Heartbeat task cancelled for connection: {connection.connection_id}")
    except Exception as e:
        logger.error(f"Error in heartbeat task for {connection.connection_id}: {e}")

@router.post("/subscribe")
async def sse_subscribe(
    subscription: SSESubscriptionRequest,
    connection_id: str = Query(..., description="SSE connection ID")
):
    """
    Update SSE subscription for an existing connection.
    
    Allows dynamic subscription changes without reconnecting.
    """
    try:
        subscribed_types = await sse_manager.handle_subscription(
            connection_id, subscription.event_types, subscription.project_id
        )
        
        return {
            "message": "SSE subscriptions updated successfully",
            "connection_id": connection_id,
            "event_types": subscribed_types,
            "project_id": subscription.project_id
