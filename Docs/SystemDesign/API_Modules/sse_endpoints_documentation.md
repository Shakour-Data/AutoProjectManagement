### SSE Endpoints Module

- **Method:** N/A
- **Path:** `/api/v1/sse`
- **Description:** Server-Sent Events (SSE) endpoints for real-time updates in AutoProjectManagement.
- **Authentication:** Optional
- **Rate Limit:** N/A

#### Parameters
N/A

#### Response
**Success Response (200 OK):**
```json
{
  "message": "SSE endpoints available",
  "endpoints": {
    "events": "/api/v1/sse/events",
    "subscribe": "/api/v1/sse/subscribe",
    "stats": "/api/v1/sse/stats",
    "test-event": "/api/v1/sse/test-event",
    "connections": "/api/v1/sse/connections"
  },
  "timestamp": "2025-08-14T10:30:00.000Z"
}
```

**Error Responses:**
- `500 Internal Server Error`: If there is an issue with the SSE endpoints.

#### Example Request
```bash
curl -X GET "http://localhost:8000/api/v1/sse/events?event_types=file_change,commit&project_id=123"
```

#### Example Response
```json
{
  "type": "connection_established",
  "connection_id": "conn_1_1234567890",
  "timestamp": "2025-08-14T10:30:00.000Z",
  "message": "SSE connection established",
  "subscribed_event_types": ["file_change", "commit"],
  "project_id": "123"
}
```

#### Notes
- This module provides Server-Sent Events (SSE) endpoints for real-time updates in the AutoProjectManagement system.
- Ensure compatibility with Python 3.8+.
