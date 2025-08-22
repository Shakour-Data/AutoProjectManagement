#!/usr/bin/env python3
"""
Test script for WebSocket and SSE real-time implementation.
This script tests the real-time event system integration.
"""

import asyncio
import json
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

async def test_event_service():
    """Test the EventService functionality."""
    try:
        from autoprojectmanagement.api.realtime_service import EventService, EventType, Event
        
        logger.info("Testing EventService...")
        
        # Create event service instance
        event_service = EventService()
        
        # Test publishing events
        test_event = Event(
            type=EventType.FILE_CHANGE,
            data={
                "file_path": "test_file.py",
                "change_type": "modified",
                "project_id": "test_project"
            }
        )
        
        await event_service.publish_event(test_event)
        logger.info("✅ Event published successfully")
        
        # Test connection stats
        stats = event_service.get_connection_stats()
        logger.info(f"Connection stats: {stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ EventService test failed: {e}")
        return False

async def test_file_change_event_publishing():
    """Test file change event publishing."""
    try:
