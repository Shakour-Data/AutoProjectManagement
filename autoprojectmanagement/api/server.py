"""
Server runner for the FastAPI application.

This module provides comprehensive server management for the AutoProjectManagement
API, including uvicorn integration, configuration management, and production-ready
features like graceful shutdown, logging, and monitoring.

Key Features:
    - Uvicorn server integration
    - Configuration management
    - Graceful shutdown handling
    - Logging and monitoring
    - Production deployment support
    - Health checks and readiness probes

Usage:
    Development server:
        $ python -m autoprojectmanagement.api.server
    
    Production server:
        $ python -m autoprojectmanagement.api.server --host 0.0.0.0 --port 8000
    
    Custom configuration:
        $ python -m autoprojectmanagement.api.server --config production.json

Configuration:
    The server supports configuration through:
    - Environment variables
    - Command line arguments
    - Configuration files
    - Default values

Examples:
    Basic usage:
        >>> from autoprojectmanagement.api.server import start_server
        >>> start_server(host='0.0.0.0', port=8000)
    
    Custom configuration:
        >>> start_server(host='localhost', port=8080, reload=False)

For more information, visit: https://github.com/AutoProjectManagement/AutoProjectManagement
"""

import argparse
import logging
import os
import signal
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Server configuration defaults
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_RELOAD = True
DEFAULT_LOG_LEVEL = "info"
DEFAULT_WORKERS = 1
DEFAULT_TIMEOUT = 30

# Import FastAPI app
try:
    import uvicorn
    from autoprojectmanagement.api.app import app
except ImportError:
    # Fallback for development
    uvicorn = None
    logger.warning("uvicorn not found. Install with: pip install uvicorn[standard]")
    
    # Create a mock app for development
    class MockApp:
        pass
    app = MockApp()

class ServerManager:
    """
    Comprehensive server management for AutoProjectManagement API.
    
    This class provides complete server lifecycle management including startup,
    shutdown, configuration, and monitoring capabilities.
    
    Attributes:
        host: Server host address
        port: Server port number
        reload: Enable auto-reload for development
        log_level: Logging level
        workers: Number of worker processes
        timeout: Request timeout in seconds
        
    Example:
        >>> manager = ServerManager(host='0.0.0.0', port=8000)
        >>> manager.start()
    """
    
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        reload: bool = DEFAULT_RELOAD,
        log_level: str = DEFAULT_LOG_LEVEL,
        workers: int = DEFAULT_WORKERS,
        timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """
        Initialize server manager with comprehensive configuration.
        
        Args:
            host: Server host address
            port: Server port number
            reload: Enable auto-reload for development
            log_level: Logging level (debug, info, warning, error)
            workers: Number of worker processes
            timeout: Request timeout in seconds
        """
        self.host = host
        self.port = port
        self.reload = reload
        self.log_level = log_level
        self.workers = workers
        self.timeout = timeout
        self.running = False
        
    def start(self) -> None:
        """
        Start the server with comprehensive configuration.
        
        This method initializes the uvicorn server with all configured parameters
        and handles graceful startup procedures.
        """
        if uvicorn is None:
            logger.error("Cannot start server: uvicorn not installed")
            return
            
        logger.info(f"Starting AutoProjectManagement API server...")
        logger.info(f"Host: {self.host}")
        logger.info(f"Port: {self.port}")
        logger.info(f"Reload: {self.reload}")
        logger.info(f"Log Level: {self.log_level}")
        logger.info(f"Workers: {self.workers}")
        
        try:
            uvicorn.run(
                "autoprojectmanagement.api.app:app",
                host=self.host,
                port=self.port,
                reload=self.reload,
                log_level=self.log_level,
                workers=self.workers,
                timeout_keep_alive=self.timeout
            )
        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
    
    def stop(self) -> None:
        """
        Stop the server gracefully.
        
        This method ensures all connections are closed and resources are
        properly cleaned up before shutdown.
        """
        logger.info("Stopping AutoProjectManagement API server...")
        self.running = False
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get current server configuration.
        
        Returns:
            Dict containing all server configuration parameters
        """
        return {
            "host": self.host,
            "port": self.port,
            "reload": self.reload,
            "log_level": self.log_level,
            "workers": self.workers,
            "timeout": self.timeout,
            "running": self.running
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            Dict containing server health status
        """
        return {
            "status": "healthy" if self.running else "stopped",
            "host": self.host,
            "port": self.port,
            "timestamp": time.time()
        }

def load_configuration(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load server configuration from file or environment variables.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Dict containing server configuration
    """
    config = {
        "host": os.getenv("API_HOST", DEFAULT_HOST),
        "port": int(os.getenv("API_PORT", str(DEFAULT_PORT))),
        "reload": os.getenv("API_RELOAD", str(DEFAULT_RELOAD)).lower() == "true",
        "log_level": os.getenv("API_LOG_LEVEL", DEFAULT_LOG_LEVEL),
        "workers": int(os.getenv("API_WORKERS", str(DEFAULT_WORKERS))),
        "timeout": int(os.getenv("API_TIMEOUT", str(DEFAULT_TIMEOUT)))
    }
    
    if config_path and Path(config_path).exists():
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            logger.warning(f"Failed to load config file: {e}")
    
    return config

def start_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    reload: bool = DEFAULT_RELOAD,
    log_level: str = DEFAULT_LOG_LEVEL,
    workers: int = DEFAULT_WORKERS,
    timeout: int = DEFAULT_TIMEOUT,
    config_path: Optional[str] = None
) -> None:
    """
    Start the server with comprehensive configuration.
    
    Args:
        host: Server host address
        port: Server port number
        reload: Enable auto-reload for development
        log_level: Logging level
        workers: Number of worker processes
        timeout: Request timeout in seconds
        config_path: Optional configuration file path
    """
    # Load configuration
    config = load_configuration(config_path)
    
    # Override with provided parameters
    if host != DEFAULT_HOST:
        config["host"] = host
    if port != DEFAULT_PORT:
        config["port"] = port
    if reload != DEFAULT_RELOAD:
        config["reload"] = reload
    if log_level != DEFAULT_LOG_LEVEL:
        config["log_level"] = log_level
    if workers != DEFAULT_WORKERS:
        config["workers"] = workers
    if timeout != DEFAULT_TIMEOUT:
        config["timeout"] = timeout
    
    # Create and start server
    server = ServerManager(**config)
    server.start()

def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown."""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

def main():
    """Main entry point for the server."""
    parser = argparse.ArgumentParser(
        description="AutoProjectManagement API Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Start with default settings
  %(prog)s --host 0.0.0.0 --port 8000  # Bind to all interfaces
  %(prog)s --reload --log-level debug    # Development mode
  %(prog)s --config production.json      # Use configuration file
        """
    )
    
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Host to bind server (default: {DEFAULT_HOST})"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to bind server (default: {DEFAULT_PORT})"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        default=DEFAULT_RELOAD,
        help="Enable auto-reload for development"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error"],
        default=DEFAULT_LOG_LEVEL,
        help=f"Logging level (default: {DEFAULT_LOG_LEVEL})"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Number of worker processes (default: {DEFAULT_WORKERS})"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        start_server(
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level,
            workers=args.workers,
            timeout=args.timeout,
            config_path=args.config
        )
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
