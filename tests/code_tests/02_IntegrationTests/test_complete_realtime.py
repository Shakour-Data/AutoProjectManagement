#!/usr/bin/env python3
"""
Complete test for real-time WebSocket and SSE implementation.
This test starts the server and tests both WebSocket and SSE functionality.
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
import subprocess
import threading
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

class TestServer:
    """Test server management class."""
    
    def __init__(self):
        self.process = None
        self.server_url = "http://localhost:8000"
    
    def start_server(self):
        """Start the FastAPI server in a subprocess."""
        try:
            logger.info("Starting FastAPI server...")
            self.process = subprocess.Popen([
                "uvicorn", "autoprojectmanagement.api.app:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(3)
            
            # Test if server is running
            response = requests.get(f"{self.server_url}/", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Server started successfully")
                return True
            else:
                logger.error(f"❌ Server returned status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the server."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            logger.info("Server stopped")

async def test_websocket_functionality():
    """Test WebSocket functionality with the server running."""
    try:
        import websockets
        
        logger.info("Testing WebSocket functionality...")
        
        async with websockets.connect("ws://localhost:8000/api/v1/dashboard/ws") as websocket:
            # Wait for connection established message first
            response = await websocket.recv()
            response_data = json.loads(response)
            logger.info(f"Connection response: {response_data}")
            
            if response_data.get("type") != "connection_established":
                logger.error(f"❌ Expected connection_established, got: {response_data.get('type')}")
                return False
            
            # Test subscription
            subscription = {
                "type": "subscribe",
                "event_types": ["file_change", "auto_commit"],
                "project_id": "test_project"
            }
            await websocket.send(json.dumps(subscription))
            
            # Wait for subscription confirmation
            response = await websocket.recv()
            response_data = json.loads(response)
            logger.info(f"Subscription response: {response_data}")
            
            if response_data.get("type") == "subscription_confirmed":
                logger.info("✅ WebSocket subscription confirmed")
                
                # Test ping
                await websocket.send(json.dumps({"type": "ping"}))
                pong_response = await websocket.recv()
                pong_data = json.loads(pong_response)
                logger.info(f"Pong response: {pong_data}")
                
                if pong_data.get("type") == "pong":
                    logger.info("✅ WebSocket ping/pong working")
                    return True
                else:
                    logger.error("❌ WebSocket ping/pong failed")
                    return False
            else:
                logger.error(f"❌ WebSocket subscription failed. Expected 'subscription_confirmed', got: {response_data.get('type')}")
                return False
                
    except Exception as e:
        logger.error(f"❌ WebSocket test failed: {e}")
        return False

async def test_sse_functionality():
    """Test SSE functionality with the server running."""
    try:
        import aiohttp
        
        logger.info("Testing SSE functionality...")
        
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
                    
                    # Read connection message
                    async for line in response.content:
                        if line.startswith(b'data: '):
                            event_data = json.loads(line[6:].strip())
                            if event_data.get("type") == "connection_established":
                                logger.info("✅ SSE connection established")
                                return True
                            break
                    
                    return True
                else:
                    logger.error(f"❌ SSE endpoint returned status: {response.status}")
                    return False
                    
    except Exception as e:
        logger.error(f"❌ SSE test failed: {e}")
        return False

async def test_event_publishing():
    """Test event publishing functionality."""
    try:
        from autoprojectmanagement.api.realtime_service import publish_file_change_event
        
        logger.info("Testing event publishing...")
        
        # Test publishing file change event
        await publish_file_change_event(
            file_path="test_file.py",
            change_type="modified",
            project_id="test_project"
        )
        
        logger.info("✅ Event published successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Event publishing test failed: {e}")
        return False

async def test_api_endpoints():
    """Test API endpoints."""
    try:
        logger.info("Testing API endpoints...")
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/api/v1/health")
        if response.status_code == 200:
            logger.info("✅ Health endpoint working")
        else:
            logger.error(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test WebSocket stats
        response = requests.get("http://localhost:8000/api/v1/dashboard/ws/stats")
        if response.status_code == 200:
            logger.info("✅ WebSocket stats endpoint working")
        else:
            logger.error(f"❌ WebSocket stats endpoint failed: {response.status_code}")
            return False
        
        # Test SSE stats
        response = requests.get("http://localhost:8000/api/v1/sse/stats")
        if response.status_code == 200:
            logger.info("✅ SSE stats endpoint working")
        else:
            logger.error(f"❌ SSE stats endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ API endpoints test failed: {e}")
        return False

async def main():
    """Run complete real-time implementation test."""
    logger.info("Starting complete real-time implementation test...")
    
    # Start server
    server = TestServer()
    if not server.start_server():
        return 1
    
    try:
        # Run tests
        results = []
        
        # Test API endpoints
        api_result = await test_api_endpoints()
        results.append(("API Endpoints", api_result))
        
        # Test event publishing
        event_result = await test_event_publishing()
        results.append(("Event Publishing", event_result))
        
        # Test WebSocket
        websocket_result = await test_websocket_functionality()
        results.append(("WebSocket", websocket_result))
        
        # Test SSE
        sse_result = await test_sse_functionality()
        results.append(("SSE", sse_result))
        
        # Print results
        logger.info("\n" + "="*60)
        logger.info("COMPLETE TEST RESULTS:")
        logger.info("="*60)
        
        all_passed = True
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name:20} {status}")
            if not result:
                all_passed = False
        
        logger.info("="*60)
        
        if all_passed:
            logger.info("🎉 ALL TESTS PASSED! Real-time implementation is working correctly.")
            return 0
        else:
            logger.error("💥 SOME TESTS FAILED! Check the implementation.")
            return 1
            
    finally:
        # Stop server
        server.stop_server()

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
