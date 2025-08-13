"""
Main entry point for the API.
This file provides backward compatibility and can be used as a simple launcher.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import the app and server
from autoprojectmanagement.api.app import app
from autoprojectmanagement.api.server import start_server

# Export the app for uvicorn
__all__ = ['app']

if __name__ == "__main__":
    start_server()
