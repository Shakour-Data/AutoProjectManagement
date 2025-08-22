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
        from autoprojectmanagement.api.realtime_service import publish_file_change_event
        
        logger.info("Testing file change event publishing...")
        
        # Test publishing a file change event
        await publish_file_change_event(
            file_path="test_file.py",
            change_type="modified",
            project_id="test_project"
        )
        
        logger.info("✅ File change event published successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ File change event test failed: {e}")
        return False

async def test_websocket_connection():
    """Test WebSocket connection functionality."""
    try:
        import websockets
        
        logger.info("Testing WebSocket connection...")
        
        # Try to connect to WebSocket endpoint
        async with websockets.connect("ws://localhost:8000/api/v1/dashboard/ws") as websocket:
            # Send initial message
            await websocket.send(json.dumps({
                "type": "subscribe",
                "event_types": ["file_change", "auto_commit"],
                "project_id": "test_project"
            }))
            
            # Wait for response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            logger.info(f"WebSocket response: {response_data}")
            
            if response_data.get("type") == "subscription_confirmed":
                logger.info("✅ WebSocket subscription confirmed")
                return True
            else:
                logger.error(f"❌ Unexpected WebSocket response: {response_data}")
                return False
                
    except Exception as e:
        logger.error(f"❌ WebSocket test failed: {e}")
        return False

async def test_sse_endpoint():
    """Test SSE endpoint functionality."""
    try:
        import aiohttp
        
        logger.info("Testing SSE endpoint...")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://localhost:8000/api/v1/sse/events",
                params={
                    "event_types": "file_change,auto_commit",
                    "project_id": "test_project"
                }
            ) as response:
                
                if response.status == 200:
                    logger.info("✅ SSE endpoint connected successfully")
                    
                    # Read first event
                    async for line in response.content:
                        if line.startswith(b'data: '):
                            event_data = json.loads(line[6:].strip())
                            logger.info(f"SSE event received: {event_data}")
                            break
                    
                    return True
                else:
                    logger.error(f"❌ SSE endpoint returned status: {response.status}")
                    return False
                    
    except Exception as e:
        logger.error(f"❌ SSE test failed: {e}")
        return False

async def main():
    """Run all tests."""
    logger.info("Starting real-time implementation tests...")
    
    # Test EventService
    event_service_result = await test_event_service()
    
    # Test file change events
    file_change_result = await test_file_change_event_publishing()
    
    # Note: WebSocket and SSE tests require the server to be running
    # Uncomment these if you want to test with a running server
    
    # websocket_result = await test_websocket_connection()
    # sse_result = await test_sse_endpoint()
    
    logger.info("\n" + "="*50)
    logger.info("TEST RESULTS:")
    logger.info(f"EventService: {'✅ PASS' if event_service_result else '❌ FAIL'}")
    logger.info(f"FileChange Events: {'✅ PASS' if file_change_result else '❌ FAIL'}")
    # logger.info(f"WebSocket: {'✅ PASS' if websocket_result else '❌ FAIL'}")
    # logger.info(f"SSE: {'✅ PASS' if sse_result else '❌ FAIL'}")
    logger.info("="*50)
    
    # Overall result
    all_passed = all([event_service_result, file_change_result])  # Add websocket_result, sse_result when uncommented
    if all_passed:
        logger.info("🎉 All tests passed!")
        return 0
    else:
        logger.error("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
