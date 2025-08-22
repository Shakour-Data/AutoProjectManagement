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
