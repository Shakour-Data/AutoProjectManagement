#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/sse_endpoints_enhanced.py
File: sse_endpoints_enhanced.py
Purpose: Enhanced Server-Sent Events (SSE) endpoints for real-time updates
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
            logger.error(f"Error sending message to SSE connection {极.connection_id}: {e}")
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
                logger.error(f"Error in SSE message generator for {self.connection_id}: {e}")
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
                logger.error(f"极 closing SSE connection {connection_id}: {e}")
    
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
    project_id: Optional[str极= Query(None, description="Project ID filter"),
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
