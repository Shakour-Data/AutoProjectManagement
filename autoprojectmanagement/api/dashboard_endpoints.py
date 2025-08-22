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
    from autoprojectmanagement.main_modules.progress_reporting.progress_report import ProgressReport
    from autoprojectmanagement.main_modules.progress_reporting.dashboards_reports import DashboardReports
    from autoprojectmanagement.api.realtime_service import EventService, EventType, Connection, event_service
except ImportError:
    # Handle import for development
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.api.services import ProjectService
    from autoprojectmanagement.main_modules.progress_reporting.progress_report import ProgressReport
    from autoprojectmanagement.main_modules.progress_reporting.dashboards_reports import DashboardReports
    from autoprojectmanagement.api.realtime_service import EventService, EventType, Connection, event_service

# Create router
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Initialize services
project_service = ProjectService()
progress_reporter = ProgressReport()
dashboard_reporter = DashboardReports()

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

class WebSocketSubscriptionRequest(BaseModel):
    """Model for WebSocket subscription requests."""
    event_types: List[str] = Field(..., description="Event types to subscribe to")
    project_id: Optional[str] = Field(None, description="Project ID filter")

# WebSocket connection class
class WebSocketConnection(Connection):
    """WebSocket connection with event subscription support."""
    
    def __init__(self, connection_id: str, websocket: WebSocket):
        super().__init__(connection_id)
        self.websocket = websocket
    
    async def send(self, message: Dict[str, Any]):
        """Send message through WebSocket."""
        try:
            await self.websocket.send_json(message)
            self.update_activity()
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
            raise

# WebSocket connection manager
class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocketConnection] = {}
    
    async def connect(self, websocket: WebSocket) -> WebSocketConnection:
        """Register a new WebSocket connection."""
        connection_id = event_service.generate_connection_id()
        connection = WebSocketConnection(connection_id, websocket)
        
        await websocket.accept()
        await event_service.register_connection(connection)
        self.active_connections[connection_id] = connection
        
        logger.info(f"New WebSocket connection: {connection_id}. Total: {len(self.active_connections)}")
        return connection
    
    async def disconnect(self, connection_id: str):
        """Disconnect WebSocket connection."""
        if connection_id in self.active_connections:
            await event_service.unregister_connection(connection_id)
            del self.active_connections[connection_id]
            logger.info(f"WebSocket connection closed: {connection_id}. Total: {len(self.active_connections)}")
    
    async def handle_subscription(self, connection_id: str, subscription_request: Dict[str, Any]):
        """Handle subscription request from client."""
        if connection_id not in self.active_connections:
            return
        
        connection = self.active_connections[connection_id]
        
        # Parse event types
        event_types = subscription_request.get('event_types', [])
        for event_type_str in event_types:
            try:
                event_type = EventType(event_type_str)
                event_service.subscribe(connection_id, event_type)
            except ValueError:
                logger.warning(f"Invalid event type: {event_type_str}")
        
        # Set project filter
        project_id = subscription_request.get('project_id')
        event_service.set_project_filter(connection_id, project_id)
        
        logger.debug(f"Connection {connection_id} subscriptions updated: {event_types}, project: {project_id}")

# Global connection manager
websocket_manager = WebSocketConnectionManager()

# Utility functions (to be implemented in separate modules)
def calculate_health_score(status_data: Dict[str, Any]) -> float:
    """Calculate project health score based on multiple factors."""
    # Placeholder implementation - will be implemented in business logic
    return 85.0  # Default health score

def determine_risk_level(status_data: Dict[str, Any]) -> str:
    """Determine risk level based on project status."""
    # Placeholder implementation
    return "low"

def get_team_performance(project_id: str) -> float:
    """Get team performance metrics."""
    # Placeholder implementation
    return 90.0

def get_quality_metrics(project_id: str) -> Dict[str, float]:
    """Get quality metrics for the project."""
    # Placeholder implementation
    return {"test_coverage": 85.0, "code_quality": 88.0, "bug_density": 2.5}

def get_metrics_data(project_id: str, timeframe: str) -> Dict[str, Any]:
    """Get comprehensive metrics data."""
    # Placeholder implementation
    return {
        "velocity": 25,
        "throughput": 18,
        "cycle_time": 2.5,
        "lead_time": 4.2
    }

def get_trends_data(project_id: str, timeframe: str) -> Dict[str, List[float]]:
    """Get historical trends data."""
    # Placeholder implementation
    return {
        "velocity": [20, 22, 25, 23, 26],
        "throughput": [15, 16, 18, 17, 19]
    }

def get_alerts(project_id: Optional[str], severity: Optional[str], resolved: bool) -> List[DashboardAlert]:
    """Get active alerts."""
    # Placeholder implementation
    return [
        DashboardAlert(
            id="alert-001",
            type="risk",
            severity="warning",
            message="Progress slowing down in sprint",
            timestamp=datetime.now(),
            project_id=project_id or "default",
            resolved=False
        )
    ]

def get_health_data(project_id: str) -> Dict[str, Any]:
    """Get comprehensive health data."""
    # Placeholder implementation
    return {
        "overall_health": 85,
        "components": {
            "code_quality": "healthy",
            "test_coverage": "degraded",
            "documentation": "healthy",
            "deployment": "healthy"
        }
    }

def get_performance_data(project_id: str) -> Dict[str, Any]:
    """Get team performance data."""
    # Placeholder implementation
    return {
        "team_velocity": 25,
        "individual_performance": {
            "developer1": 95,
            "developer2": 88,
            "developer3": 92
        }
    }

def get_realtime_update() -> Dict[str, Any]:
    """Get real-time update data for WebSocket."""
    # Placeholder implementation
    return {
        "type": "update",
        "timestamp": datetime.now().isoformat(),
        "metrics": get_metrics_data("default", "1h"),
        "alerts": get_alerts(None, None, False)
    }

def save_layout_config(layout_config: Dict[str, Any]) -> Dict[str, Any]:
    """Save layout configuration."""
    # Placeholder implementation
    return layout_config

def get_layout_config(layout_type: str) -> Dict[str, Any]:
    """Get layout configuration."""
    # Placeholder implementation
    return {
        "layout_type": layout_type,
        "widgets": ["health", "progress", "risks", "team"],
        "refresh_rate": 3000,
        "theme": "light"
    }

@router.get("/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    project_id: str = Query(..., description="Project ID for dashboard overview")
) -> DashboardOverview:
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
    
    Provides live updates for all dashboard metrics and alerts using event-driven architecture.
    """
    connection = await websocket_manager.connect(websocket)
    
    try:
        # Send initial connection confirmation
        await connection.send({
            "type": "connection_established",
            "connection_id": connection.connection_id,
            "timestamp": datetime.now().isoformat(),
            "message": "WebSocket connection established",
            "available_event_types": [et.value for et in EventType]
        })
        
        # Main message loop
        while True:
            try:
                # Wait for messages from client (subscription requests, etc.)
                data = await websocket.receive_json(timeout=300.0)
                
                if data.get('type') == 'subscribe':
                    # Handle subscription request
                    await websocket_manager.handle_subscription(connection.connection_id, data)
                    
                    # Send subscription confirmation
                    await connection.send({
                        "type": "subscription_confirmed",
                        "timestamp": datetime.now().isoformat(),
                        "event_types": data.get('event_types', []),
                        "project_id": data.get('project_id')
                    })
                
                elif data.get('type') == 'ping':
                    # Handle ping request
                    await connection.send({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
                
            except asyncio.TimeoutError:
                # Send heartbeat to keep connection alive
                await connection.send({
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.warning(f"Error processing WebSocket message: {e}")
                break
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {connection.connection_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket_manager.disconnect(connection.connection_id)

@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics."""
    try:
        stats = event_service.get_connection_stats()
        return {
            "websocket_connections": len(websocket_manager.active_connections),
            "total_connections": stats["total_connections"],
            "subscription_counts": stats["subscription_counts"],
            "message_queue_size": stats["message_queue_size"]
        }
    except Exception as e:
        logger.error(f"Error getting WebSocket stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

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
        raise HTTPException(status_code=500, detail=f"Error getting layout: {str(e)}")
