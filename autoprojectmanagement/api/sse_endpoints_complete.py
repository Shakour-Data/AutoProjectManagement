#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/sse_endpoints_complete.py
File: sse_endpoints_complete.py
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
