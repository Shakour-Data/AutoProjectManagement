"""
path: autoprojectmanagement/services/integration_services/integration_manager.py
File: integration_manager.py
Purpose: Central integration manager for coordinating all project management modules
Author: GravityWavesPr
Version: 2.0.0
License: MIT
Description: Manages the execution and integration of all project management modules
providing a unified interface for running project management workflows.
"""

import subprocess
import logging
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
import os

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
    workflows by managing module dependencies, execution order, and error handling.
    
    Attributes:
        modules (List[str]): List of module filenames to execute
        execution_results (Dict[str, Any]): Results from module executions
        config (Dict[str, Any]): Configuration settings
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

def main():
    """Main entry point for the integration manager."""
    manager = IntegrationManager()
    results = manager.run_all()
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
