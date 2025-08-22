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
