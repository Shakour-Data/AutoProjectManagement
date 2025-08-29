#!/usr/bin/env python3
"""
Simple WebSocket debug script to test connection and subscription.
"""

import asyncio
import json
import logging
import websockets

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_websocket():
    """Test WebSocket connection and subscription."""
    try:
        logger.info("Connecting to WebSocket...")
        
        async with websockets.connect("ws://localhost:8000/api/v1/dashboard/ws") as websocket:
            logger.info("WebSocket connected")
            
            # Wait for connection established message
            response = await websocket.recv()
            response_data = json.loads(response)
            logger.info(f"Connection response: {response_data}")
            
            # Send subscription
            subscription = {
                "type": "subscribe",
                "event_types": ["file_change", "auto_commit"],
                "project_id": "test_project"
            }
            logger.info(f"Sending subscription: {subscription}")
            await websocket.send(json.dumps(subscription))
            
            # Wait for subscription confirmation with timeout
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                response_data = json.loads(response)
                logger.info(f"Subscription response: {response_data}")
                
                if response_data.get("type") == "subscription_confirmed":
                    logger.info("✅ Subscription confirmed successfully")
                    return True
                else:
                    logger.error(f"❌ Unexpected response type: {response_data.get('type')}")
                    return False
                    
            except asyncio.TimeoutError:
                logger.error("❌ Timeout waiting for subscription confirmation")
                return False
                
    except Exception as e:
        logger.error(f"❌ WebSocket test failed: {e}")
        return False

async def main():
    """Run WebSocket debug test."""
    result = await test_websocket()
    if result:
        logger.info("🎉 WebSocket test passed!")
    else:
        logger.error("💥 WebSocket test failed!")

if __name__ == "__main__":
    asyncio.run(main())
