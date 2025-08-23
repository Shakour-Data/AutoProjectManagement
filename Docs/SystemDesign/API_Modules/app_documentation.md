### App Module

- **Method:** N/A
- **Path:** `/api/v1/app`
- **Description:** FastAPI application setup for the AutoProjectManagement system.
- **Authentication:** Optional
- **Rate Limit:** N/A

#### Parameters
N/A

#### Response
**Success Response (200 OK):**
```json
{
  "message": "Welcome to the AutoProjectManagement API",
  "version": "1.0.0",
  "api_version": "v1",
  "documentation": {
    "swagger": "/docs",
    "redoc": "/redoc",
    "openapi": "/openapi.json"
  },
  "endpoints": {
    "projects": "/api/v1/projects",
