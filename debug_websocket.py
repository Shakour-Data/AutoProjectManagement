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
