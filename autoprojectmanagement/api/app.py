"""
FastAPI application definition.
This file contains only the FastAPI app and routes, without direct uvicorn imports.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Union

try:
    from fastapi import FastAPI, HTTPException
except ImportError:
    # Fallback for development
    class FastAPI:
        def __init__(self, *args, **kwargs):
            pass
    class HTTPException(Exception):
        def __init__(self, status_code, detail):
            self.status_code = status_code
            self.detail = detail

# Adjust imports to be relative to the project root
try:
    from autoprojectmanagement.services.configuration_cli.cli_commands import (
        get_project_status as cli_get_project_status
    )
except ImportError:
    # This allows running the script directly for development
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.services.configuration_cli.cli_commands import (
        get_project_status as cli_get_project_status
    )

# Create a FastAPI app instance
app: FastAPI = FastAPI(
    title="AutoProjectManagement API",
    description="API for the Automated Project Management System.",
    version="1.0.0",
)


@app.get("/", tags=["Root"])
def read_root() -> Dict[str, str]:
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the AutoProjectManagement API!"}


@app.get(
    "/api/v1/projects/{project_id}/status",
    tags=["Projects"],
    response_model=Dict[str, Any]
)
def get_project_status(
    project_id: str,
    format: str = 'json'
) -> Union[Dict[str, Any], Dict[str, str]]:
    """Get the status of a specific project."""
    status_data = cli_get_project_status(project_id, format)
    
    if not status_data:
        raise HTTPException(
            status_code=404,
            detail=f"Project '{project_id}' not found."
        )
    
    if format == 'json':
        try:
            return json.loads(status_data)
        except (json.JSONDecodeError, TypeError):
            return {"status_data": status_data}
    
    return {"status_data": status_data}
