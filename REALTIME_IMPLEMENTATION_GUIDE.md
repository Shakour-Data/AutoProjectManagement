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
