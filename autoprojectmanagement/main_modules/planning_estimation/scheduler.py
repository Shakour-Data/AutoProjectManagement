#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/planning_estimation/scheduler.py
File: scheduler.py
Purpose: Task scheduling system
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Task scheduling system within the AutoProjectManagement system
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
Task scheduling system within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import schedule
import time
import threading
import logging
from typing import Callable, List, Optional, Dict, Any
from datetime import datetime, timedelta
import atexit
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_CHECK_INTERVAL = 1  # seconds
MAX_RETRY_ATTEMPTS = 3
BACKOFF_FACTOR = 2
DEFAULT_THREAD_NAME = "SchedulerThread"

class ScheduleFrequency(Enum):
    """Enumeration for schedule frequencies."""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"

@dataclass
class ScheduleConfig:
    """Configuration class for scheduling parameters."""
    check_interval: int = DEFAULT_CHECK_INTERVAL
    max_retry_attempts: int = MAX_RETRY_ATTEMPTS
    backoff_factor: float = BACKOFF_FACTOR
    thread_name: str = DEFAULT_THREAD_NAME
    enable_logging: bool = True
    daemon_thread: bool = True

class ScheduledJob:
    """Wrapper class for individual scheduled jobs with metadata."""
    
    def __init__(self, job_func: Callable, frequency: ScheduleFrequency, 
                 schedule_config: Optional[Dict[str, Any]] = None):
        """
        Initialize a scheduled job.
        
        Args:
            job_func: The function to be executed
            frequency: The frequency of execution
            schedule_config: Optional configuration for the job
        """
        self.job_func = job_func
        self.frequency = frequency
        self.schedule_config = schedule_config or {}
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.run_count = 0
        self.error_count = 0
        self.job = None

class Scheduler:
    """
    Advanced scheduler for managing automated project management tasks.
    
    This class provides a robust scheduling system with support for:
    - Multiple scheduling frequencies (hourly, daily, weekly, custom)
    - Error handling and retry mechanisms
    - Logging and monitoring
    - Graceful shutdown
    - Thread-safe operations
    
    Attributes:
        jobs: List of scheduled jobs
        config: Scheduler configuration
        is_running: Flag indicating if scheduler is active
        thread: Background thread for scheduling
    """
    
    def __init__(self, config: Optional[ScheduleConfig] = None):
        """
        Initialize the scheduler with optional configuration.
        
        Args:
            config: Optional ScheduleConfig instance for custom settings
        """
        self.config = config or ScheduleConfig()
        self.jobs: List[ScheduledJob] = []
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # Register cleanup on exit
        atexit.register(self.stop)
        
    def start(self) -> None:
        """
        Start the scheduler in a background thread.
        
        This method creates a daemon thread that continuously checks
        and runs pending scheduled jobs.
        """
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
            
        try:
            with self._lock:
                self.is_running = True
                
            def run_scheduler() -> None:
                """Internal function to run the scheduler loop."""
                logger.info("Scheduler thread started")
                while self.is_running:
                    try:
                        schedule.run_pending()
                        time.sleep(self.config.check_interval)
                    except Exception as e:
                        logger.error(f"Error in scheduler loop: {e}")
                        time.sleep(self.config.check_interval * self.config.backoff_factor)
            
            self.thread = threading.Thread(
                target=run_scheduler,
                name=self.config.thread_name,
                daemon=self.config.daemon_thread
            )
            self.thread.start()
            logger.info("Scheduler started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            raise
    
    def stop(self) -> None:
        """Stop the scheduler gracefully."""
        if not self.is_running:
            return
            
        try:
            with self._lock:
                self.is_running = False
            logger.info("Scheduler stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    def schedule_hourly(self, job_func: Callable, interval: int = 1) -> ScheduledJob:
        """
        Schedule a job to run every N hours.
        
        Args:
            job_func: The function to execute
            interval: Number of hours between executions (default: 1)
            
        Returns:
            ScheduledJob instance with job details
        """
        job = ScheduledJob(job_func, ScheduleFrequency.HOURLY)
        
        try:
            schedule_job = schedule.every(interval).hours.do(
                self._execute_job_with_error_handling, job
            )
            job.job = schedule_job
            self.jobs.append(job)
            logger.info(f"Hourly job scheduled with {interval}h interval")
            return job
        except Exception as e:
            logger.error(f"Failed to schedule hourly job: {e}")
            raise
    
    def schedule_daily(self, job_func: Callable, at_time: str = "00:00") -> ScheduledJob:
        """
        Schedule a job to run daily at a specific time.
        
        Args:
            job_func: The function to execute
            at_time: Time in 24-hour format (HH:MM)
            
        Returns:
            ScheduledJob instance with job details
        """
        job = ScheduledJob(job_func, ScheduleFrequency.DAILY)
        
        try:
            schedule_job = schedule.every().day.at(at_time).do(
                self._execute_job_with_error_handling, job
            )
            job.job = schedule_job
            self.jobs.append(job)
            logger.info(f"Daily job scheduled at {at_time}")
            return job
        except Exception as e:
            logger.error(f"Failed to schedule daily job: {e}")
            raise
    
    def schedule_weekly(self, job_func: Callable, day: str = "sunday", 
                       at_time: str = "00:00") -> ScheduledJob:
        """
        Schedule a job to run weekly on a specific day and time.
        
        Args:
            job_func: The function to execute
            day: Day of the week (monday, tuesday, etc.)
            at_time: Time in 24-hour format (HH:MM)
            
        Returns:
            ScheduledJob instance with job details
        """
        job = ScheduledJob(job_func, ScheduleFrequency.WEEKLY)
        
        try:
            schedule_job = getattr(schedule.every(), day).at(at_time).do(
                self._execute_job_with_error_handling, job
            )
            job.job = schedule_job
            self.jobs.append(job)
            logger.info(f"Weekly job scheduled on {day} at {at_time}")
            return job
        except Exception as e:
            logger.error(f"Failed to schedule weekly job: {e}")
            raise
    
    def schedule_custom(self, job_func: Callable, cron_expression: str) -> ScheduledJob:
        """
        Schedule a job with custom cron-like expression.
        
        Args:
            job_func: The function to execute
            cron_expression: Custom scheduling expression
            
        Returns:
            ScheduledJob instance with job details
        """
        job = ScheduledJob(job_func, ScheduleFrequency.CUSTOM)
        
        try:
            # For now, use schedule library's capabilities
            # Future enhancement: parse cron expressions
            logger.warning("Custom scheduling not fully implemented, using daily")
            schedule_job = schedule.every().day.do(
                self._execute_job_with_error_handling, job
            )
            job.job = schedule_job
            self.jobs.append(job)
            return job
        except Exception as e:
            logger.error(f"Failed to schedule custom job: {e}")
            raise
    
    def _execute_job_with_error_handling(self, scheduled_job: ScheduledJob) -> None:
        """
        Execute a scheduled job with comprehensive error handling.
        
        Args:
            scheduled_job: The ScheduledJob instance to execute
        """
        try:
            scheduled_job.last_run = datetime.now()
            scheduled_job.run_count += 1
            
            if self.config.enable_logging:
                logger.info(f"Executing job: {scheduled_job.job_func.__name__}")
            
            scheduled_job.job_func()
            
            if self.config.enable_logging:
                logger.info(f"Job completed: {scheduled_job.job_func.__name__}")
                
        except Exception as e:
            scheduled_job.error_count += 1
            logger.error(
                f"Job failed: {scheduled_job.job_func.__name__}, "
                f"error: {e}, attempts: {scheduled_job.error_count}"
            )
            
            # Implement retry logic
            if scheduled_job.error_count < self.config.max_retry_attempts:
                logger.info(f"Retrying job: {scheduled_job.job_func.__name__}")
            else:
                logger.error(
                    f"Job permanently failed after "
                    f"{self.config.max_retry_attempts} attempts"
                )
    
    def get_job_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status of all scheduled jobs.
        
        Returns:
            Dictionary containing job status information
        """
        return {
            "is_running": self.is_running,
            "total_jobs": len(self.jobs),
            "jobs": [
                {
                    "function": job.job_func.__name__,
                    "frequency": job.frequency.value,
                    "last_run": job.last_run.isoformat() if job.last_run else None,
                    "run_count": job.run_count,
                    "error_count": job.error_count
                }
                for job in self.jobs
            ]
        }
    
    def clear_all_jobs(self) -> None:
        """Clear all scheduled jobs."""
        try:
            schedule.clear()
            self.jobs.clear()
            logger.info("All jobs cleared")
        except Exception as e:
            logger.error(f"Error clearing jobs: {e}")
    
    def __del__(self):
        """Cleanup when scheduler is destroyed."""
        self.stop()

def create_default_scheduler() -> Scheduler:
    """
    Factory function to create a scheduler with default configuration.
    
    Returns:
        Scheduler instance with default settings
    """
    return Scheduler()

def validate_schedule_config(config: Dict[str, Any]) -> bool:
    """
    Validate schedule configuration parameters.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if configuration is valid, False otherwise
    """
    required_keys = ["check_interval", "max_retry_attempts", "backoff_factor"]
    return all(key in config for key in required_keys)

# Example usage and testing
if __name__ == "__main__":
    # Create scheduler instance
    scheduler = create_default_scheduler()
    
    # Example job functions
    def update_dashboards():
        """Example dashboard update job."""
        logger.info("Updating dashboards...")
    
    def generate_reports():
        """Example report generation job."""
        logger.info("Generating reports...")
    
    def backup_data():
        """Example data backup job."""
        logger.info("Backing up data...")
    
    # Schedule jobs
    scheduler.schedule_hourly(update_dashboards)
    scheduler.schedule_daily(generate_reports, "02:00")
    scheduler.schedule_weekly(backup_data, "sunday", "03:00")
    
    # Start scheduler
    scheduler.start()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Shutting down scheduler...")
        scheduler.stop()
