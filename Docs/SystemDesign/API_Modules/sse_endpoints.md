# API Module Documentation: sse_endpoints.py

*Last updated: 2025-08-14*

## Overview

The `sse_endpoints.py` module provides complete Server-Sent Events (SSE) implementation for browser-compatible real-time event streaming in the AutoProjectManagement system. It enables efficient, low-latency communication with web clients through standardized SSE protocol.

## Architecture Diagram

```mermaid
graph TB
    subgraph "SSE Service Layer"
        A[SSE Router]
        B[Event Streaming]
        C[Connection Management]
        D[Subscription System]
    end
    
    subgraph "Real-time Integration"
        E[Event Service]
        F[Connection Pool]
        G[Event Broadcasting]
        H[Heartbeat System]
    end
    
    subgraph "Client Communication"
        I[Browser Clients]
        J[Mobile Applications]
        K[Third-party Integrations]
        L[Monitoring Tools]
    end
    
    subgraph "Support Services"
        M[Statistics Collection]
        N[Connection Monitoring]
        O[Error Handling]
        P[Reconnection Support]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    E --> G
    E --> H
    
    B --> I
    B --> J
    B --> K
    B --> L
    
    C --> M
    C --> N
    C --> O
    C --> P
```

## Module Purpose and Responsibilities

| Responsibility | Description |
|----------------|-------------|
| SSE Protocol | Standard-compliant Server-Sent Events implementation |
| Connection Management | SSE connection lifecycle and state management |
| Event Streaming | Efficient real-time data delivery to clients |
| Subscription System | Dynamic event type subscription management |
| Browser Compatibility | Cross-browser SSE support and fallback handling |
| Reconnection Support | Automatic reconnection with event replay |

## API Endpoints Structure

### SSE Streaming Endpoint

| Endpoint | Method | Description | Media Type |
|----------|--------|-------------|------------|
| `/sse/events` | GET | Main SSE event streaming endpoint | text/event-stream |

### Management Endpoints

| Endpoint | Method | Description | Purpose |
|----------|--------|-------------|---------|
| `/sse/subscribe` | POST | Dynamic subscription management | Runtime subscription changes |
| `/sse/stats` | GET | Connection statistics | Monitoring and diagnostics |
| `/sse/connections` | GET | Active connection listing | Connection management |
| `/sse/test-event` | POST | Test event publishing | Development and testing |

## SSE Protocol Implementation

### Event Format Specification

```mermaid
flowchart LR
    Event[Event Data] --> Format[SSE Formatting]
    Format --> Fields[Protocol Fields]
    Fields --> Delivery[Client Delivery]
    
    subgraph Format
        F1[Event ID]
        F2[Event Type]
        F3[Data Payload]
        F4[Empty Line]
    end
```

### Protocol Field Structure

| Field | Format | Description | Required |
|-------|--------|-------------|----------|
| id | `id: <value>\n` | Unique event identifier | Optional |
| event | `event: <type>\n` | Event type/category | Optional |
| data | `data: <json>\n` | Event payload data | Required |
| retry | `retry: <ms>\n` | Reconnection timeout | Optional |

### Message Example

```
id: event-12345
event: progress_update
data: {"progress":75,"message":"Update completed"}
```

## Data Models

### SSEConnection Model

| Field | Type | Description | Purpose |
|-------|------|-------------|---------|
| connection_id | string | Unique connection identifier | Connection tracking |
| message_queue | Queue | Outgoing message queue | Message buffering |
| last_event_id | string | Last delivered event ID | Reconnection support |
| subscriptions | set | Subscribed event types | Event filtering |
| project_filter | string | Project-specific filter | Data segregation |

### SSESubscriptionRequest Model

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| event_types | list | Event types to subscribe | Required |
| project_id | string | Project filter | Optional |
| last_event_id | string | Last received event ID | Reconnection |

## Connection Lifecycle

### Establishment Process

```mermaid
sequenceDiagram
    participant Client
    participant SSEEndpoint
    participant ConnectionManager
    participant EventService
    
    Client->>SSEEndpoint: GET /sse/events
    SSEEndpoint->>ConnectionManager: Create Connection
    ConnectionManager->>EventService: Register Connection
    EventService-->>ConnectionManager: Connection ID
    ConnectionManager-->>SSEEndpoint: SSEConnection
    SSEEndpoint-->>Client: Connection Established
```

### Message Flow

```mermaid
flowchart TD
    Start[Event Occurrence] --> Publish[Event Service Publish]
    Publish --> Queue[Add to Message Queue]
    Queue --> Format[SSE Formatting]
    Format --> Deliver[Client Delivery]
    Deliver --> Ack[Delivery Acknowledgment]
    
    Queue -->|Timeout| Drop[Drop Event]
    Deliver -->|Error| Retry[Retry Logic]
```

### Termination Process

```mermaid
sequenceDiagram
    participant Client
    participant SSEEndpoint
    participant ConnectionManager
    participant EventService
    
    Client->>SSEEndpoint: Connection Close
    SSEEndpoint->>ConnectionManager: Close Connection
    ConnectionManager->>EventService: Unregister Connection
    EventService-->>ConnectionManager: Confirmation
    ConnectionManager-->>SSEEndpoint: Cleanup Complete
```

## Subscription Management

### Subscription Types

| Event Type | Description | Data Format |
|------------|-------------|-------------|
| file_change | File system modifications | File metadata |
| commit | Version control operations | Commit details |
| progress_update | Task progress changes | Progress metrics |
| risk_alert | Risk assessment events | Risk data |
| task_update | Task status updates | Task information |
| system_status | System health status | Health metrics |

### Dynamic Subscription

```mermaid
flowchart LR
    Request[Subscription Request] --> Parse[Parse Event Types]
    Parse --> Validate[Validate Types]
    Validate --> Update[Update Subscriptions]
    Update --> Confirm[Send Confirmation]
    
    Validate -->|Invalid| Error[Return Error]
```

## Performance Characteristics

### Connection Capacity

| Metric | Value | Description |
|--------|-------|-------------|
| Maximum Connections | 1000+ | Concurrent SSE connections |
| Message Throughput | 500+ events/sec | Event processing rate |
| Memory Usage | 5-10MB per connection | Connection overhead |
| Latency | <100ms | End-to-end delivery time |

### Browser Compatibility

| Browser | SSE Support | Limitations |
|---------|-------------|-------------|
| Chrome | Full support | 6 concurrent connections |
| Firefox | Full support | 6 concurrent connections |
| Safari | Full support | 6 concurrent connections |
| Edge | Full support | 6 concurrent connections |
| IE11 | No support | Requires polyfill |

## Error Handling

### Connection Errors

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Network Failure | Connection loss | Automatic reconnection |
| Browser Limit | Connection quota | Connection pooling |
| Timeout | Inactivity | Heartbeat maintenance |
| Protocol Error | Invalid format | Connection reset |

### Server Errors

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Memory Pressure | High connection count | Connection cleanup |
| Event Queue Full | High event volume | Event dropping |
| Service Unavailable | Backend issues | Graceful degradation |

## Security Considerations

### Authentication & Authorization

| Aspect | Mechanism | Description |
|--------|-----------|-------------|
| Connection Auth | Optional | Bearer tokens or cookies |
| Event Filtering | Project-based | Data segregation |
