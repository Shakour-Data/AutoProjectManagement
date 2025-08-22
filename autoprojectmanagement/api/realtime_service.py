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
    COMMIT = "commit"
    PROGRESS_UPDATE = "progress_update"
    RISK_ALERT = "risk_alert"
    TASK_UPDATE = "task_update"
    SYSTEM_STATUS = "system_status"
    DASHBOARD_UPDATE = "dashboard_update"
    HEALTH_CHECK = "health_check"

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
