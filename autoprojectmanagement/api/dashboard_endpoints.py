#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/dashboard_endpoints.py
File: dashboard_endpoints.py
Purpose: Dashboard-specific API endpoints for AutoProjectManagement
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Comprehensive dashboard API endpoints including real-time data, metrics, and project health monitoring
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

