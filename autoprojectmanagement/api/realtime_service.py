#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/realtime_service.py
File: realtime_service.py
Purpose: Centralized real-time event service for WebSocket and SSE
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Event service for managing real-time connections and broadcasting events
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Any, Optional, Set, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventType(str, Enum):
    """Types of real-time events."""
    FILE_CHANGE = "file_change"

@dataclass
class Event:
    """Real-time event data structure."""
    type: EventType
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    source: str = "system"
    project_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp,
            "source": self.source,
            "project_id": self.project_id,
            "iso_timestamp": datetime.fromtimestamp(self.timestamp).isoformat()
        }

class Connection:
    """Base connection class for WebSocket and SSE."""
    def __init__(self, connection_id: str):
        self.connection_id = connection_id
        self.connected_at = time.time()
        self.last_activity = time.time()
        self.subscriptions: Set[EventType] = set()
        self.project_filter: Optional[str] = None

    def is_subscribed(self, event_type: EventType) -> bool:
        """Check if connection is subscribed to event type."""
        return event_type in self.subscriptions

    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = time.time()

    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information."""
        return {
            "connection_id": self.connection_id,
            "connected_at": self.connected_at,
            "last_activity": self.last_activity,
            "subscriptions": [sub.value for sub in self.subscriptions],
            "project_filter": self.project_filter,
            "duration_seconds": time.time() - self.connected_at
        }

class EventService:
    """Centralized event service for real-time communications."""
    
    def __init__(self):
        self.connections: Dict[str, Connection] = {}
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.running = False
        self.connection_counter = 0
        
    def generate_connection_id(self) -> str:
        """Generate unique connection ID."""
        self.connection_counter += 1
        return f"conn_{self.connection_counter}_{int(time.time())}"
    
    async def start(self):
        """Start the event service."""
        if self.running:
            return
            
        self.running = True
        logger.info("Event service started")
        
        # Start background tasks
        asyncio.create_task(self._cleanup_inactive_connections())
        asyncio.create_task(self._process_message_queue())
    
    async def stop(self):
        """Stop the event service."""
        self.running = False
        logger.info("Event service stopped")
    
    async def register_connection(self, connection: Connection) -> str:
        """Register a new connection."""
        self.connections[connection.connection_id] = connection
        logger.info(f"New connection registered: {connection.connection_id}")
        return connection.connection_id
    
    async def unregister_connection(self, connection_id: str):
        """Unregister a connection."""
        if connection_id in self.connections:
            del self.connections[connection_id]
            logger.info(f"Connection unregistered: {connection_id}")
    
    def subscribe(self, connection_id: str, event_type: EventType):
        """Subscribe connection to event type."""
        if connection_id in self.connections:
            self.connections[connection_id].subscriptions.add(event_type)
            logger.debug(f"Connection {connection_id} subscribed to {event_type}")
    
    def unsubscribe(self, connection_id: str, event_type: EventType):
        """Unsubscribe connection from event type."""
        if connection_id in self.connections:
            self.connections[connection_id].subscriptions.discard(event_type)
            logger.debug(f"Connection {connection_id} unsubscribed from {event_type}")
    
    def set_project_filter(self, connection_id: str, project_id: Optional[str]):
        """Set project filter for connection."""
        if connection_id in self.connections:
            self.connections[connection_id].project_filter = project_id
            logger.debug(f"Connection {connection_id} project filter set to {project_id}")
    
    async def publish_event(self, event: Event):
        """Publish an event to all subscribed connections."""
        await self.message_queue.put(event)
    
    async def _process_message_queue(self):
        """Process events from the message queue."""
        while self.running:
            try:
                event = await self.message_queue.get()
                await self._broadcast_event(event)
                self.message_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing message queue: {e}")
    
    async def _broadcast_event(self, event: Event):
        """Broadcast event to all subscribed connections."""
        event_dict = event.to_dict()
        subscribers = 0
        
        for connection_id, connection in list(self.connections.items()):
            try:
                # Check if connection is subscribed to this event type
                if not connection.is_subscribed(event.type):
                    continue
                
                # Apply project filter if set
                if (connection.project_filter and 
                    event.project_id and 
                    connection.project_filter != event.project_id):
                    continue
                
                # This is a base class - actual sending is implemented in subclasses
                # WebSocket and SSE connections will override the send method
                if hasattr(connection, 'send'):
                    await connection.send(event_dict)
                    subscribers += 1
                    
            except Exception as e:
                logger.error(f"Error broadcasting to connection {connection_id}: {e}")
                # Remove faulty connection
                await self.unregister_connection(connection_id)
        
        if subscribers > 0:
            logger.debug(f"Event {event.type} broadcast to {subscribers} subscribers")
    
    async def _cleanup_inactive_connections(self, timeout: int = 300):
        """Clean up inactive connections."""
        while self.running:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                current_time = time.time()
                inactive_connections = []
                
                for connection_id, connection in list(self.connections.items()):
                    if current_time - connection.last_activity > timeout:
                        inactive_connections.append(connection_id)
                
                for connection_id in inactive_connections:
                    logger.info(f"Cleaning up inactive connection: {connection_id}")
                    await self.unregister_connection(connection_id)
                    
            except Exception as e:
                logger.error(f"Error in connection cleanup: {e}")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        total_connections = len(self.connections)
        subscription_counts = {et.value: 0 for et in EventType}
        
        for connection in self.connections.values():
            for event_type in connection.subscriptions:
                subscription_counts[event_type.value] += 1
        
        return {
            "total_connections": total_connections,
            "subscription_counts": subscription_counts,
            "message_queue_size": self.message_queue.qsize(),
            "uptime_seconds": time.time() - getattr(self, '_start_time', time.time())
        }
    
    def register_event_handler(self, event_type: EventType, handler: Callable):
        """Register event handler for specific event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        logger.debug(f"Handler registered for event type: {event_type}")
    
    async def trigger_event_handlers(self, event: Event):
        """Trigger handlers for specific event type."""
        if event.type in self.event_handlers:
            for handler in self.event_handlers[event.type]:
                try:
                    await handler(event)
                except Exception as e:
                    logger.error(f"Error in event handler for {event.type}: {e}")

# Global event service instance
event_service = EventService()

async def initialize_event_service():
    """Initialize the global event service."""
    await event_service.start()
    logger.info("Global event service initialized")

async def shutdown_event_service():
    """Shutdown the global event service."""
    await event_service.stop()
    logger.info("Global event service shutdown")

# Utility functions for common event types
async def publish_file_change_event(file_path: str, change_type: str, project_id: Optional[str] = None):
    """Publish file change event."""
    event = Event(
        type=EventType.FILE_CHANGE,
        data={
            "file_path": file_path,
            "change_type": change_type,
            "timestamp": time.time()
        },
        project_id=project_id
    )
    await event_service.publish_event(event)

async def publish_commit_event(commit_hash: str, message: str, author: str, files_changed: List[str], project_id: Optional[str] = None):
    """Publish commit event."""
    event = Event(
        type=EventType.COMMIT,
        data={
            "commit_hash": commit_hash,
            "message": message,
            "author": author,
            "files_changed": files_changed,
            "timestamp": time.time()
        },
        project_id=project_id
    )
    await event_service.publish_event(event)

async def publish_progress_update(progress_data: Dict[str, Any], project_id: Optional[str] = None):
    """Publish progress update event."""
    event = Event(
        type=EventType.PROGRESS_UPDATE,
        data=progress_data,
        project_id=project_id
    )
    await event_service.publish_event(event)

async def publish_risk_alert(risk_data: Dict[str, Any], project_id: Optional[str] = None):
    """Publish risk alert event."""
    event = Event(
        type=EventType.RISK_ALERT,
        data=risk_data,
        project_id=project_id
    )
    await event_service.publish_event(event)

async def publish_task_update(task_data: Dict[str, Any], project_id: Optional[str] = None):
    """Publish task update event."""
    event = Event(
        type=EventType.TASK_UPDATE,
        data=task_data,
        project_id=project_id
    )
    await event_service.publish_event(event)
