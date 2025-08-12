"""
Server runner for the FastAPI application.
This file handles uvicorn imports and server startup.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

try:
    import uvicorn
except ImportError:
    print("Warning: uvicorn not found. Install with: pip install uvicorn")
    uvicorn = None

from autoprojectmanagement.api.app import app


def start_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True) -> None:
    """Start the uvicorn server."""
    if uvicorn is None:
        print("Cannot start server: uvicorn not installed")
        return
    
    uvicorn.run(
        "autoprojectmanagement.api.app:app",
        host=host,
        port=port,
        reload=reload
    )


if __name__ == "__main__":
    start_server()
