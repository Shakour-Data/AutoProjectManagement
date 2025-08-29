#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/services/integration_services/integration_manager.py
File: integration_manager.py
Purpose: Integration management
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Integration management within the AutoProjectManagement system
"""

import logging
from typing import Dict, Any, Optional, List, Union
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
Integration management within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import subprocess
import logging
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable
import json
from datetime import datetime
import os
import threading
import time
from flask import Flask, request, jsonify

# Configure logging with proper formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integration_manager.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Constants for better maintainability
MODULES_PATH = "autoprojectmanagement/main_modules"
SUCCESS_EXIT_CODE = 0
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Module execution order based on dependencies
MODULE_EXECUTION_ORDER = [
    'setup_initialization.py',
    'time_management.py',
    'scope_management.py',
    'wbs_merger.py',
    'resource_allocation_manager.py',
    'scope_management.py',
    'resource_management.py',
    'resource_leveling.py',
    'risk_management.py',
    'communication_management.py',
    'quality_management.py',
    'commit_progress_manager.py',
    'reporting.py'
]

class IntegrationManager:
    """
    Central integration manager for coordinating all project management modules.
    
    This class provides a unified interface for executing project management
    workflows by managing module dependencies, execution order, error handling,
    and GitHub webhook integration for real-time synchronization.
    
    Attributes:
        modules (List[str]): List of module filenames to execute
        execution_results (Dict[str, Any]): Results from module executions
        config (Dict[str, Any]): Configuration settings
        webhook_server (Flask): Flask app for handling GitHub webhooks
        webhook_thread (threading.Thread): Thread for running webhook server
        github_integration (GitHubIntegration): GitHub integration instance
        event_handlers (Dict[str, Callable]): Registered event handlers
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the IntegrationManager with configuration.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.modules = MODULE_EXECUTION_ORDER
        self.execution_results = {}
        self.config = self._load_config(config_path)
        self.start_time = None
        self.end_time = None
        
        # Webhook and GitHub integration setup
        self.webhook_server = None
        self.webhook_thread = None
        self.github_integration = None
        self.event_handlers = {}
        
        logger.info("IntegrationManager initialized successfully")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        default_config = {
            "max_retries": MAX_RETRIES,
            "retry_delay": RETRY_DELAY,
            "log_level": "INFO",
            "modules_path": MODULES_PATH
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    logger.info(f"Configuration loaded from {config_path}")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def _get_module_path(self, module_name: str) -> Path:
        """Get the full path for a module file."""
        module_path = Path(self.config.get("modules_path", MODULES_PATH)) / module_name
        
        if not module_path.exists():
            alternative_paths = [
                Path("autoprojectmanagement/main_modules") / module_name,
                Path("main_modules") / module_name,
                Path(module_name)
            ]
            
            for alt_path in alternative_paths:
                if alt_path.exists():
                    return alt_path
            
            raise FileNotFoundError(f"Module {module_name} not found at {module_path}")
        
        return module_path
    
    def run_module(self, module_name: str, retry_count: int = 0) -> bool:
        """Execute a single module with error handling and retry logic."""
        try:
            module_path = self._get_module_path(module_name)
            logger.info(f"Running {module_name} (attempt {retry_count + 1})...")
            
            env = os.environ.copy()
            env['PYTHONPATH'] = str(Path.cwd())
            
            result = subprocess.run(
                [sys.executable, str(module_path)],
                capture_output=True,
                text=True,
                timeout=300,
                env=env
            )
            
            self.execution_results[module_name] = {
                'success': result.returncode == SUCCESS_EXIT_CODE,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'timestamp': datetime.now().isoformat()
            }
            
            if result.returncode == SUCCESS_EXIT_CODE:
                logger.info(f"✅ {module_name} executed successfully")
                return True
            else:
                logger.error(f"❌ {module_name} failed with return code {result.returncode}")
                return False
                
        except Exception as e:
            logger.error(f"💥 Unexpected error running {module_name}: {e}")
            return False
    
    def run_all(self, continue_on_error: bool = False) -> Dict[str, Any]:
        """Execute all modules in the defined order."""
        self.start_time = datetime.now()
        logger.info("🚀 Starting integration execution...")
        
        successful_modules = []
        failed_modules = []
        
        for module in self.modules:
            success = self.run_module(module)
            
            if success:
                successful_modules.append(module)
            else:
                failed_modules.append(module)
                if not continue_on_error:
                    logger.error(f"🛑 Stopping integration due to error in {module}")
                    break
        
        self.end_time = datetime.now()
        
        summary = {
            'total_modules': len(self.modules),
            'successful_modules': successful_modules,
            'failed_modules': failed_modules,
            'success_rate': len(successful_modules) / len(self.modules) if self.modules else 0,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration': str(self.end_time - self.start_time),
        }
        
        return summary
    
    def generate_report(self) -> str:
        """Generate a comprehensive execution report."""
        if not self.execution_results:
            return "No execution data available"
        
        report = [
            "Integration Report",
            "=" * 50,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"Total Modules: {len(self.modules)}",
            f"Successful: {len([m for m in self.execution_results.values() if m['success']])}",
            f"Failed: {len([m for m in self.execution_results.values() if not m['success']])}",
            "",
            "Detailed Results:",
            "-" * 30,
        ]
        
        for module, result in self.execution_results.items():
            status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
            report.append(f"{module}: {status}")
        
        return "\n".join(report)

    def setup_github_integration(self, owner: str, repo: str, token: Optional[str] = None) -> None:
        """
        Set up GitHub integration for webhook handling and real-time synchronization.
        
        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            token: GitHub personal access token (optional)
        """
        try:
            from src.autoprojectmanagement.services.integration_services.github_integration import GitHubIntegration
            self.github_integration = GitHubIntegration(owner, repo, token)
            logger.info(f"GitHub integration set up for {owner}/{repo}")
        except ImportError:
            logger.error("GitHub integration module not found")
        except Exception as e:
            logger.error(f"Failed to set up GitHub integration: {e}")

    def register_event_handler(self, event_type: str, handler: Callable[[str, Dict[str, Any]], None]) -> None:
        """
        Register a handler for specific GitHub webhook events.
        
        Args:
            event_type: GitHub event type (e.g., 'issues', 'issue_comment')
            handler: Function to handle the event
        """
        self.event_handlers[event_type] = handler
        logger.info(f"Registered handler for {event_type} events")

    def _handle_webhook_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """
        Internal method to handle webhook events and route to appropriate handlers.
        
        Args:
            event_type: GitHub event type
            payload: Webhook payload data
        """
        try:
            logger.info(f"Processing {event_type} webhook event")
            
            # Route to specific handler if registered
            if event_type in self.event_handlers:
                self.event_handlers[event_type](event_type, payload)
                logger.info(f"Handled {event_type} event with registered handler")
            else:
                # Default handling for common events
                if event_type == 'issues':
                    action = payload.get('action')
                    issue = payload.get('issue', {})
                    issue_number = issue.get('number')
                    logger.info(f"Issue #{issue_number} {action}: {issue.get('title')}")
                    
                elif event_type == 'issue_comment':
                    comment = payload.get('comment', {})
                    issue = payload.get('issue', {})
                    issue_number = issue.get('number')
                    logger.info(f"New comment on issue #{issue_number} by {comment.get('user', {}).get('login')}")
                    
                logger.info(f"Processed {event_type} event with default handling")
                
        except Exception as e:
            logger.error(f"Error handling {event_type} event: {e}")

    def start_webhook_server(self, port: int = 5000, webhook_secret: Optional[str] = None) -> None:
        """
        Start a webhook server to receive GitHub events.
        
        Args:
            port: Port to run the webhook server on
            webhook_secret: Secret for webhook verification
        """
        if not self.github_integration:
            logger.error("GitHub integration not set up. Call setup_github_integration first.")
            return
            
        self.webhook_server = Flask(__name__)
        
        @self.webhook_server.route('/webhook', methods=['POST'])
        def handle_webhook():
            try:
                # Verify webhook signature if secret is provided
                signature = request.headers.get('X-Hub-Signature-256')
                if webhook_secret and signature:
                    if not self.github_integration.verify_webhook_signature(
                        request.data, signature, webhook_secret
                    ):
                        logger.warning("Invalid webhook signature")
                        return jsonify({"error": "Invalid signature"}), 401
                
                event_type = request.headers.get('X-GitHub-Event')
                payload = request.json
                
                if not event_type or not payload:
                    return jsonify({"error": "Missing event type or payload"}), 400
                
                # Process the event asynchronously
                threading.Thread(
                    target=self._handle_webhook_event,
                    args=(event_type, payload),
                    daemon=True
                ).start()
                
                return jsonify({"status": "processing"}), 202
                
            except Exception as e:
                logger.error(f"Webhook processing error: {e}")
                return jsonify({"error": str(e)}), 500
        
        def run_server():
            self.webhook_server.run(host='0.0.0.0', port=port, debug=False)
        
        self.webhook_thread = threading.Thread(target=run_server, daemon=True)
        self.webhook_thread.start()
        logger.info(f"Webhook server started on port {port}")

    def stop_webhook_server(self) -> None:
        """Stop the webhook server."""
        if self.webhook_server:
            # Flask doesn't have a built-in stop method, so we'll just mark it for cleanup
            logger.info("Webhook server stopped")
            self.webhook_server = None
            self.webhook_thread = None

    def create_github_webhook(self, webhook_url: str, events: List[str], secret: Optional[str] = None) -> bool:
        """
        Create a GitHub webhook for the repository.
        
        Args:
            webhook_url: URL to receive webhook events
            events: List of events to subscribe to
            secret: Webhook secret for verification
            
        Returns:
            True if webhook creation was successful
        """
        if not self.github_integration:
            logger.error("GitHub integration not set up")
            return False
            
        try:
            webhook = self.github_integration.create_webhook(webhook_url, events, secret)
            logger.info(f"Created GitHub webhook for {len(events)} events")
            return True
        except Exception as e:
            logger.error(f"Failed to create GitHub webhook: {e}")
            return False

    def sync_with_github(self) -> Dict[str, Any]:
        """
        Perform a full synchronization with GitHub repository.
        
        Returns:
            Dictionary with synchronization results
        """
        if not self.github_integration:
            return {"success": False, "error": "GitHub integration not set up"}
            
        try:
            results = {
                "issues": [],
                "pull_requests": [],
                "last_sync": datetime.now().isoformat()
            }
            
            # Sync open issues
            issues = self.github_integration.get_issues(state="open")
            results["issues"] = [{"number": issue["number"], "title": issue["title"]} for issue in issues]
            
            logger.info(f"Synchronized {len(issues)} open issues from GitHub")
            return {"success": True, "results": results}
            
        except Exception as e:
            logger.error(f"GitHub synchronization failed: {e}")
            return {"success": False, "error": str(e)}

def main():
    """Main entry point for the integration manager."""
    manager = IntegrationManager()
    results = manager.run_all()
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
