# Real-Time Implementation Guide

This document provides comprehensive guidance on the WebSocket and Server-Sent Events (SSE) implementation for the AutoProjectManagement dashboard.

## Overview

The real-time implementation provides two methods for live updates:

1. **WebSocket** (`/api/v1/dashboard/ws`) - Full-duplex communication for modern browsers
2. **Server-Sent Events** (`/api/v1/sse/events`) - One-way event streaming with browser compatibility

## WebSocket Implementation

### Connection Endpoint
```
ws://localhost:8000/api/v1/dashboard/ws
```

### Message Types

#### Client to Server
- **subscribe**: Subscribe to specific event types
- **ping**: Keep connection alive

#### Server to Client
- **connection_established**: Initial connection confirmation
- **subscription_confirmed**: Subscription acknowledgment
- **pong**: Response to ping
- **heartbeat**: Periodic keep-alive
- **event**: Real-time event data

### Subscription Example

```javascript
// Connect to WebSocket
const socket = new WebSocket('ws://localhost:8000/api/v1/dashboard/ws');

socket.onopen = () => {
  console.log('WebSocket connected');
  
  // Subscribe to events
  socket.send(JSON.stringify({
    type: 'subscribe',
    event_types: ['file_change', 'auto_commit', 'progress_update'],
    project_id: 'my-project'
  }));
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
  
  switch(data.type) {
    case 'file_change':
      handleFileChange(data.data);
      break;
    case 'auto_commit':
      handleAutoCommit(data.data);
      break;
    case 'progress_update':
      updateProgress(data.data);
      break;
  }
};
```

## Server-Sent Events (SSE) Implementation

### Endpoint
```
GET /api/v1/sse/events?event_types=file_change,auto_commit&project_id=my-project
```

### Usage Example

```javascript
// Connect to SSE endpoint
const eventSource = new EventSource('/api/v1/sse/events?event_types=file_change,auto_commit&project_id=my-project');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('SSE Event:', data);
  
  switch(data.type) {
    case 'file_change':
      handleFileChange(data.data);
      break;
    case 'auto_commit':
      handleAutoCommit(data.data);
      break;
  }
};

eventSource.onerror = (error) => {
  console.error('SSE Error:', error);
  // SSE automatically reconnects
};
```

## Available Event Types

### File Change Events (`file_change`)
```json
{
  "type": "file_change",
  "data": {
    "file_path": "src/main.py",
    "change_type": "modified",
    "project_id": "my-project",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Auto Commit Events (`auto_commit`)
```json
{
  "type": "auto_commit",
  "data": {
    "event": "start|result|error",
    "success": true,
    "changes_count": 5,
    "project_id": "my-project",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Progress Update Events (`progress_update`)
```json
{
  "type": "progress_update",
  "data": {
    "project_id": "my-project",
    "progress_percentage": 75.5,
    "completed_tasks": 15,
    "total_tasks": 20,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Risk Alert Events (`risk_alert`)
```json
{
  "type": "risk_alert",
  "data": {
    "severity": "high",
    "message": "Progress slowing down",
    "project_id": "my-project",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Integration with Auto File Watcher

The auto file watcher service now publishes events for:

1. **File changes** (created, modified, deleted, moved)
2. **Auto-commit starts and results**
3. **Scheduled commit events**
4. **Error events**

### Example File Change Event Flow

1. User modifies `src/main.py`
2. File watcher detects change
3. Event published: `file_change` with `change_type: "modified"`
4. WebSocket/SSE clients receive real-time notification
5. Dashboard updates file change counter

## JavaScript Client Implementation

### Enhanced Dashboard Integration

Update your dashboard JavaScript to use the event-driven approach:

```javascript
class RealTimeDashboard {
  constructor() {
    this.socket = null;
    this.eventSource = null;
    this.subscriptions = new Set();
  }

  // WebSocket connection
  connectWebSocket() {
