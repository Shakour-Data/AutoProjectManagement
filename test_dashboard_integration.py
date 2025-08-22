#!/usr/bin/env python3
"""
Integration test for the dashboard WebSocket functionality.
Tests the complete flow including the JavaScript dashboard.
"""

import asyncio
import json
import logging
import websockets
import threading
import time
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DashboardIntegrationTest:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.ws_url = "ws://localhost:8000/api/v1/dashboard/ws"
        self.received_messages = []
        self.connection_id = None
    
    def test_api_endpoints(self):
        """Test that all API endpoints are working."""
        logger.info("Testing API endpoints...")
        
        # Test health endpoint
        response = requests.get(f"{self.base_url}/api/v1/health")
        assert response.status_code == 200, f"Health endpoint failed: {response.status_code}"
        logger.info("✅ Health endpoint working")
        
        # Test dashboard overview
        response = requests.get(f"{self.base_url}/api/v1/dashboard/overview?project_id=test_project")
        assert response.status_code == 200, f"Dashboard overview failed: {response.status_code}"
        logger.info("✅ Dashboard overview endpoint working")
        
        # Test WebSocket stats
        response = requests.get(f"{self.base_url}/api/v1/dashboard/ws/stats")
        assert response.status_code == 200, f"WebSocket stats failed: {response.status_code}"
        logger.info("✅ WebSocket stats endpoint working")
    
    async def test_websocket_connection(self):
        """Test WebSocket connection and subscription."""
        logger.info("Testing WebSocket connection...")
        
        async with websockets.connect(self.ws_url) as websocket:
            # Wait for connection message
            response = await websocket.recv()
            data = json.loads(response)
            self.connection_id = data.get('connection_id')
            logger.info(f"✅ WebSocket connected: {self.connection_id}")
            
            # Subscribe to events
            subscription = {
                "type": "subscribe",
                "event_types": ["file_change", "progress_update"],
                "project_id": "test_project"
            }
            await websocket.send(json.dumps(subscription))
            
            # Wait for subscription confirmation
            response = await websocket.recv()
            data = json.loads(response)
            assert data.get('type') == 'subscription_confirmed', "Subscription not confirmed"
            logger.info("✅ WebSocket subscription confirmed")
            
            # Test ping/pong
            ping = {"type": "ping"}
            await websocket.send(json.dumps(ping))
            
            response = await websocket.recv()
            data = json.loads(response)
