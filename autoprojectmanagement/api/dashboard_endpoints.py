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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import business logic
try:
    from autoprojectmanagement.api.services import ProjectService
    from autoprojectmanagement.main_modules.progress_reporting.progress_report import ProgressReporter
    from autoprojectmanagement.main_modules.progress_reporting.dashboards_reports import DashboardReporter
except ImportError:
    # Handle import for development
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.api.services import ProjectService
    from autoprojectmanagement.main_modules.progress_reporting.progress_report import ProgressReporter
    from autoprojectmanagement.main_modules.progress_reporting.dashboards_reports import DashboardReporter

# Create router
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Initialize services
project_service = ProjectService()
progress_reporter = ProgressReporter()
dashboard_reporter = DashboardReporter()

# Pydantic models for dashboard requests/responses
class DashboardOverview(BaseModel):
    """Model for dashboard overview response."""
    project_id: str = Field(..., description="Unique project identifier")
    total_tasks: int = Field(..., description="Total number of tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    progress_percentage: float = Field(..., description="Progress percentage")
    health_score: float = Field(..., description="Project health score (0-100)")
    risk_level: str = Field(..., description="Risk level (low, medium, high, critical)")
    last_updated: datetime = Field(..., description="Last update timestamp")
    team_performance: float = Field(..., description="Team performance score")
    quality_metrics: Dict[str, float] = Field(..., description="Quality metrics")

class DashboardMetrics(BaseModel):
    """Model for dashboard metrics response."""
    timestamp: datetime = Field(..., description="Metrics timestamp")
    metrics: Dict[str, Any] = Field(..., description="Comprehensive metrics data")
    trends: Dict[str, List[float]] = Field(..., description="Historical trends")

class DashboardAlert(BaseModel):
    """Model for dashboard alerts."""
    id: str = Field(..., description="Alert identifier")
    type: str = Field(..., description="Alert type (risk, progress, quality, team)")
    severity: str = Field(..., description="Severity (info, warning, error, critical)")
    message: str = Field(..., description="Alert message")
    timestamp: datetime = Field(..., description="Alert timestamp")
    project_id: str = Field(..., description="Affected project ID")
    resolved: bool = Field(False, description="Whether alert is resolved")

class DashboardLayout(BaseModel):
    """Model for dashboard layout configuration."""
    layout_type: str = Field(..., description="Layout type (standard, minimal, custom)")
    widgets: List[str] = Field(..., description="List of enabled widgets")
    refresh_rate: int = Field(3000, description="Refresh rate in milliseconds")
    theme: str = Field("light", description="Theme (light, dark)")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New dashboard connection. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Dashboard connection closed. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                self.disconnect(connection)

# Global connection manager
manager = ConnectionManager()

# Utility functions (to be implemented in separate modules)
def calculate_health_score(status_data: Dict[str, Any]) -> float:
    """Calculate project health score based on multiple factors."""
    # Placeholder implementation - will be implemented in business logic
    """
    Get comprehensive dashboard overview for a project.
    
    Returns real-time project health, progress, risks, and team performance metrics.
    """
    try:
        # Get project status data
        status_data = project_service.get_status(project_id)
        
        if not status_data:
            raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
        
        # Calculate health score based on multiple factors
        health_score = calculate_health_score(status_data)
        
        # Determine risk level
        risk_level = determine_risk_level(status_data)
        
        # Get team performance metrics
        team_performance = get_team_performance(project_id)
        
        # Get quality metrics
        quality_metrics = get_quality_metrics(project_id)
        
        return DashboardOverview(
            project_id=project_id,
            total_tasks=status_data.get('total_tasks', 0),
            completed_tasks=status_data.get('completed_tasks', 0),
            progress_percentage=status_data.get('progress_percentage', 0),
            health_score=health_score,
            risk_level=risk_level,
            last_updated=datetime.now(),
            team_performance=team_performance,
            quality_metrics=quality_metrics
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dashboard overview: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    project_id: str = Query(..., description="Project ID for metrics"),
    timeframe: str = Query("24h", description="Timeframe for metrics (1h, 24h, 7d, 30d)")
) -> DashboardMetrics:
    """
    Get detailed metrics and trends for dashboard visualization.
    
    Provides comprehensive metrics data for charts and graphs.
    """
    try:
        metrics_data = get_metrics_data(project_id, timeframe)
        trends_data = get_trends_data(project_id, timeframe)
        
        return DashboardMetrics(
            timestamp=datetime.now(),
            metrics=metrics_data,
            trends=trends_data
        )
        
    except Exception as e:
        logger.error(f"Error getting dashboard metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/alerts", response_model=List[DashboardAlert])
async def get_dashboard_alerts(
    project_id: Optional[str] = Query(None, description="Filter alerts by project ID"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    resolved: bool = Query(False, description="Include resolved alerts")
) -> List[DashboardAlert]:
    """
    Get active alerts and notifications for the dashboard.
    
    Returns real-time alerts for risk, progress, quality, and team issues.
    """
    try:
        alerts = get_alerts(project_id, severity, resolved)
        return alerts
        
    except Exception as e:
        logger.error(f"Error getting dashboard alerts: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/health", response_model=Dict[str, Any])
async def get_dashboard_health(
    project_id: str = Query(..., description="Project ID for health check")
) -> Dict[str, Any]:
    """
    Get comprehensive project health status for dashboard.
    
    Detailed health assessment with component-level status.
    """
    try:
        health_data = get_health_data(project_id)
        return health_data
        
    except Exception as e:
        logger.error(f"Error getting dashboard health: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/team-performance", response_model=Dict[str, Any])
async def get_team_performance_metrics(
    project_id: str = Query(..., description="Project ID for team performance")
) -> Dict[str, Any]:
    """
    Get team performance metrics for dashboard.
    
    Individual and team-level performance statistics.
    """
    try:
        performance_data = get_performance_data(project_id)
        return performance_data
        
    except Exception as e:
        logger.error(f"Error getting team performance: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time dashboard updates.
    
    Provides live updates for all dashboard metrics and alerts.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Send initial data
            initial_data = {
                "type": "initial",
                "timestamp": datetime.now().isoformat(),
                "message": "Connected to dashboard WebSocket"
            }
            await websocket.send_json(initial_data)
            
            # Send periodic updates
            await asyncio.sleep(3)  # Update every 3 seconds
            
            # Get latest data and broadcast
            update_data = get_realtime_update()
            await websocket.send_json(update_data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@router.post("/layout", response_model=Dict[str, Any])
async def save_dashboard_layout(layout: DashboardLayout):
    """
    Save dashboard layout configuration.
    
    Persists widget arrangement, theme, and refresh settings.
    """
    try:
        saved = save_layout_config(layout.dict())
        return {"message": "Layout saved successfully", "layout": saved}
        
    except Exception as e:
        logger.error(f"Error saving layout: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving layout: {str(e)}")

@router.get("/layout", response_model=DashboardLayout)
async def get_dashboard_layout(
    layout_type: str = Query("standard", description="Layout type to retrieve")
) -> DashboardLayout:
    """
    Get saved dashboard layout configuration.
    
    Retrieves previously saved layout settings.
    """
    try:
        layout_config = get_layout_config(layout_type)
        return DashboardLayout(**layout_config)
        
    except Exception as e:
        logger.error(f"Error getting layout: {e}")
        raise HTTPException(status_code=500, detail
