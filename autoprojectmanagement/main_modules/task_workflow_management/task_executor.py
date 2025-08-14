"""
path: autoprojectmanagement/main_modules/task_workflow_management/task_executor.py
File: task_executor.py
Purpose: Execute and manage project tasks with comprehensive error handling, logging, and performance optimization
Author: AutoProjectManagement System
Version: 2.0.0
License: MIT
Description: Advanced task execution engine with phased code review improvements including security, performance, maintainability, and reliability enhancements
"""

import asyncio
import logging
import time
import traceback
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
import secrets
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import psutil
import signal
import sys
from contextlib import contextmanager
import functools
import warnings
from datetime import datetime, timedelta
import threading
from pathlib import Path
import os

# Phase 1: Security & Data Protection
class SecurityManager:
    """Handles security aspects of task execution"""
    
    @staticmethod
    def sanitize_input(data: Any) -> Any:
        """Sanitize input data to prevent injection attacks"""
        if isinstance(data, str):
            # Remove potential script tags and dangerous characters
            dangerous_chars = ['<script', 'javascript:', 'vbscript:', 'onload=', 'onerror=']
            for char in dangerous_chars:
                data = data.replace(char, '')
            return data.strip()
        elif isinstance(data, dict):
            return {k: SecurityManager.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityManager.sanitize_input(item) for item in data]
        return data
    
    @staticmethod
    def generate_secure_id(prefix: str = "task") -> str:
        """Generate cryptographically secure unique identifier"""
        random_bytes = secrets.token_bytes(16)
        hash_object = hashlib.sha256(random_bytes)
        return f"{prefix}_{hash_object.hexdigest()[:12]}"
    
    @staticmethod
    def validate_task_data(task_data: Dict[str, Any]) -> bool:
        """Validate task data for security compliance"""
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in task_data:
                return False
        
        # Check for suspicious patterns
        suspicious_patterns = ['eval(', 'exec(', 'import os', 'subprocess.']
        for value in task_data.values():
            if isinstance(value, str):
                for pattern in suspicious_patterns:
                    if pattern in value.lower():
                        return False
        
        return True

# Phase 2: Performance Optimization
class PerformanceMonitor:
    """Monitor and optimize task execution performance"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_monitoring(self, task_id: str):
        """Start performance monitoring for a task"""
        self.start_times[task_id] = time.time()
        self.metrics[task_id] = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_mb': psutil.virtual_memory().used / (1024 * 1024),
            'start_time': datetime.now()
        }
    
    def end_monitoring(self, task_id: str) -> Dict[str, Any]:
        """End performance monitoring and return metrics"""
        if task_id not in self.start_times:
            return {}
        
        end_time = time.time()
        duration = end_time - self.start_times[task_id]
        
        metrics = self.metrics.get(task_id, {})
        metrics.update({
            'duration_seconds': duration,
            'end_time': datetime.now(),
            'peak_memory_mb': psutil.virtual_memory().used / (1024 * 1024),
            'cpu_percent_end': psutil.cpu_percent()
        })
        
        # Clean up
        del self.start_times[task_id]
        return metrics
    
    @staticmethod
    def get_system_resources() -> Dict[str, float]:
        """Get current system resource usage"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'available_memory_mb': psutil.virtual_memory().available / (1024 * 1024)
        }

# Phase 3: Maintainability & Code Quality
class LoggingManager:
    """Centralized logging management"""
    
    def __init__(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger('TaskExecutor')
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            # File handler
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(
                log_dir / f"task_executor_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def log_task_start(self, task_id: str, task_name: str):
        """Log task execution start"""
        self.logger.info(f"Starting task execution: {task_name} (ID: {task_id})")
    
    def log_task_complete(self, task_id: str, duration: float, success: bool):
        """Log task execution completion"""
        status = "completed successfully" if success else "failed"
        self.logger.info(f"Task {task_id} {status} in {duration:.2f} seconds")
    
    def log_error(self, task_id: str, error: Exception, context: str = ""):
        """Log error with full context"""
        self.logger.error(
            f"Error in task {task_id}: {str(error)} - Context: {context}",
            exc_info=True
        )
    
    def log_performance_metrics(self, task_id: str, metrics: Dict[str, Any]):
        """Log performance metrics"""
        self.logger.info(f"Performance metrics for {task_id}: {json.dumps(metrics, default=str)}")

# Enhanced Task Status with additional states
class TaskStatus(Enum):
    """Enhanced enumeration for task status values with additional states"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    RETRYING = "retrying"
    PAUSED = "paused"

# Phase 4: Reliability & Error Handling
class RetryPolicy:
    """Configurable retry policy for failed tasks"""
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0, max_wait: float = 60.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.max_wait = max_wait
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt"""
        delay = min(self.backoff_factor ** attempt, self.max_wait)
        return delay
    
    def should_retry(self, attempt: int, exception: Exception) -> bool:
        """Determine if task should be retried"""
        return attempt < self.max_retries and not isinstance(exception, (KeyboardInterrupt, SystemExit))

# Data classes for enhanced task management
@dataclass
class TaskConfig:
    """Configuration for task execution"""
    timeout_seconds: float = 300.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    enable_monitoring: bool = True
    enable_logging: bool = True
    max_concurrent_tasks: int = 10
    resource_threshold: float = 80.0  # CPU/memory usage threshold

@dataclass
class TaskResult:
    """Result of task execution"""
    task_id: str
    success: bool
    duration: float
    error_message: Optional[str] = None
    output: Any = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0

# Enhanced Task class with all phases implemented
class Task:
    """Enhanced task with security, performance, and reliability features"""
    
    def __init__(self, task_id: str, name: str, description: str = "", 
                 priority: int = 1, estimated_hours: float = 0.0,
                 dependencies: List[str] = None, metadata: Dict[str, Any] = None):
        """
        Initialize a new enhanced task.
        
        Args:
            task_id: Unique identifier for the task
            name: Human-readable task name
            description: Detailed task description
            priority: Task priority (1-5, where 1 is highest)
            estimated_hours: Estimated time to complete in hours
            dependencies: List of task IDs this task depends on
            metadata: Additional task metadata
        """
        # Security: Validate and sanitize inputs
        self.task_id = SecurityManager.sanitize_input(task_id)
        self.name = SecurityManager.sanitize_input(name)
        self.description = SecurityManager.sanitize_input(description)
        
        # Validate priority and estimated hours
        self.priority = max(1, min(5, int(priority)))
        self.estimated_hours = max(0.0, float(estimated_hours))
        
        self.dependencies = dependencies or []
        self.metadata = metadata or {}
        
        # Status tracking
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.error_message = None
        self.retry_count = 0
        
        # Performance tracking
        self.performance_metrics = {}
        
        # Thread safety
        self._lock = threading.Lock()
    
    @contextmanager
    def task_context(self):
        """Context manager for safe task execution"""
        with self._lock:
            yield
    
    def start(self):
        """Mark the task as in progress with thread safety"""
        with self.task_context():
            if self.status != TaskStatus.PENDING:
                raise RuntimeError(f"Cannot start task in {self.status.value} state")
            self.status = TaskStatus.IN_PROGRESS
            self.started_at = datetime.now()
    
    def complete(self, output: Any = None):
        """Mark the task as completed with output"""
        with self.task_context():
            self.status = TaskStatus.COMPLETED
            self.completed_at = datetime.now()
            return output
    
    def fail(self, error_message: str, retry: bool = False):
        """Mark the task as failed with error handling"""
        with self.task_context():
            self.status = TaskStatus.RETRYING if retry else TaskStatus.FAILED
            self.error_message = SecurityManager.sanitize_input(error_message)
            self.completed_at = datetime.now()
            if not retry:
                self.retry_count += 1
    
    def cancel(self):
        """Cancel the task execution"""
        with self.task_context():
            if self.status in [TaskStatus.IN_PROGRESS, TaskStatus.PENDING]:
                self.status = TaskStatus.CANCELLED
                self.completed_at = datetime.now()
    
    async def execute_async(self, config: TaskConfig = None) -> TaskResult:
        """
        Execute the task asynchronously with full error handling and monitoring.
        
        Args:
            config: Task execution configuration
            
        Returns:
            TaskResult: Detailed execution result
        """
        config = config or TaskConfig()
        
        # Initialize logging and monitoring
        logger = LoggingManager().logger
        monitor = PerformanceMonitor()
        
        start_time = time.time()
        retry_count = 0
        
        try:
            # Security validation
            if not SecurityManager.validate_task_data({
                'name': self.name,
                'description': self.description
            }):
                raise ValueError("Task data validation failed")
            
            # Check system resources
            resources = PerformanceMonitor.get_system_resources()
            if resources['cpu_percent'] > config.resource_threshold:
                logger.warning(f"High CPU usage detected: {resources['cpu_percent']}%")
            
            # Execute with retry policy
            while retry_count <= config.retry_policy.max_retries:
                try:
                    # Start monitoring
                    if config.enable_monitoring:
                        monitor.start_monitoring(self.task_id)
                    
                    # Execute task with timeout
                    result = await asyncio.wait_for(
                        self._execute_task_logic(),
                        timeout=config.timeout_seconds
                    )
                    
                    # Complete task
                    self.complete(result)
                    
                    # Get performance metrics
                    metrics = monitor.end_monitoring(self.task_id) if config.enable_monitoring else {}
                    
                    # Log completion
                    duration = time.time() - start_time
                    if config.enable_logging:
                        LoggingManager().log_task_complete(self.task_id, duration, True)
                    
                    return TaskResult(
                        task_id=self.task_id,
                        success=True,
                        duration=duration,
                        output=result,
                        performance_metrics=metrics,
                        retry_count=retry_count
                    )
                    
                except asyncio.TimeoutError:
                    self.fail("Task execution timeout", retry=True)
                    retry_count += 1
                    
                except Exception as e:
                    error_msg = str(e)
                    should_retry = config.retry_policy.should_retry(retry_count, e)
                    
                    if should_retry:
                        delay = config.retry_policy.calculate_delay(retry_count)
                        await asyncio.sleep(delay)
                        retry_count += 1
                        continue
                    else:
                        self.fail(error_msg)
                        break
            
            # Task failed after retries
            duration = time.time() - start_time
            return TaskResult(
                task_id=self.task_id,
                success=False,
                duration=duration,
                error_message=self.error_message,
                retry_count=retry_count
            )
            
        except Exception as e:
            # Critical error handling
            duration = time.time() - start_time
            error_msg = f"Critical error: {str(e)}"
            self.fail(error_msg)
            
            if config.enable_logging:
                LoggingManager().log_error(self.task_id, e, "execute_async")
            
            return TaskResult(
                task_id=self.task_id,
                success=False,
                duration=duration,
                error_message=error_msg,
                retry_count=retry_count
            )
    
    async def _execute_task_logic(self) -> Any:
        """Override this method in subclasses for actual task logic"""
        # Default implementation - subclasses should override
        await asyncio.sleep(0.1)  # Simulate async work
        return {"status": "completed", "message": f"Task {self.task_id} executed successfully"}

# Enhanced TaskExecutor with all phases implemented
class TaskExecutor:
    """Enhanced task executor with security, performance, and reliability features"""
    
    def __init__(self, config: TaskConfig = None):
        """
        Initialize a new enhanced task executor.
        
        Args:
            config: Task execution configuration
        """
        self.config = config or TaskConfig()
        self.tasks: Dict[str, Task] = {}
        self.logger = LoggingManager().logger
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_tasks)
        
        # Graceful shutdown handling
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Performance monitoring
        self.performance_monitor = PerformanceMonitor()
        
        # Thread safety
        self._lock = threading.Lock()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.shutdown()
        sys.exit(0)
    
    def shutdown(self):
        """Gracefully shutdown the executor"""
        self.logger.info("Shutting down task executor...")
        self.executor.shutdown(wait=True)
        self.logger.info("Task executor shutdown complete")
    
    def add_task(self, task: Task) -> bool:
        """
        Add a task to the executor with validation.
        
        Args:
            task: Task instance to add
            
        Returns:
            bool: True if task was added successfully
        """
        with self._lock:
            if task.task_id in self.tasks:
                self.logger.warning(f"Task with ID {task.task_id} already exists")
                return False
            
            # Security validation
            if not SecurityManager.validate_task_data({
                'name': task.name,
                'description': task.description
            }):
                self.logger.error(f"Task validation failed for {task.task_id}")
                return False
            
            self.tasks[task.task_id] = task
            self.logger.info(f"Added task: {task.name} (ID: {task.task_id})")
            return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID with security check"""
        sanitized_id = SecurityManager.sanitize_input(task_id)
        return self.tasks.get(sanitized_id)
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task with logging"""
        sanitized_id = SecurityManager.sanitize_input(task_id)
        with self._lock:
            if sanitized_id in self.tasks:
                task = self.tasks[sanitized_id]
                del self.tasks[sanitized_id]
                self.logger.info(f"Removed task: {task.name} (ID: {sanitized_id})")
                return True
            return False
    
    async def execute_task(self, task_id: str) -> TaskResult:
        """Execute a specific task with full monitoring"""
        task = self.get_task(task_id)
        if not task:
            return TaskResult(
                task_id=task_id,
                success=False,
                duration=0.0,
                error_message="Task not found"
            )
        
        return await task.execute_async(self.config)
    
    async def execute_batch(self, task_ids: List[str]) -> List[TaskResult]:
        """Execute multiple tasks concurrently with resource management"""
        # Check system resources
        resources = PerformanceMonitor.get_system_resources()
        if resources['cpu_percent'] > self.config.resource_threshold:
            self.logger.warning(f"High system load: {resources['cpu_percent']}% CPU")
        
        # Limit concurrent executions
        semaphore = asyncio.Semaphore(self.config.max_concurrent_tasks)
        
        async def execute_with_semaphore(task_id: str) -> TaskResult:
            async with semaphore:
                return await self.execute_task(task_id)
        
        tasks = [execute_with_semaphore(tid) for tid in task_ids if self.get_task(tid)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(TaskResult(
                    task_id=task_ids[i],
                    success=False,
                    duration=0.0,
                    error_message=str(result)
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get tasks by status with thread safety"""
        with self._lock:
            return [task for task in self.tasks.values() if task.status == status]
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks with thread safety"""
        with self._lock:
            return list(self.tasks.values())
    
    def get_task_statistics(self) -> Dict[str, int]:
        """Get comprehensive task statistics"""
        with self._lock:
            stats = {status.value: 0 for status in TaskStatus}
            for task in self.tasks.values():
                stats[task.status.value] += 1
            return stats
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report for all tasks"""
        with self._lock:
            completed_tasks = self.get_tasks_by_status(TaskStatus.COMPLETED)
            failed_tasks = self.get_tasks_by_status(TaskStatus.FAILED)
            
            total_tasks = len(self.tasks)
            completed_count = len(completed_tasks)
            failed_count = len(failed_tasks)
            
            if completed_tasks:
                avg_duration = sum(
                    task.performance_metrics.get('duration_seconds', 0)
                    for task in completed_tasks
                ) / completed_count
            else:
                avg_duration = 0.0
            
            return {
                'total_tasks': total_tasks,
                'completed': completed_count,
                'failed': failed_count,
                'success_rate': (completed_count / total_tasks * 100) if total_tasks > 0 else 0,
                'average_duration_seconds': avg_duration,
                'system_resources': PerformanceMonitor.get_system_resources()
            }
    
    def clear_completed_tasks(self) -> int:
        """Remove completed tasks and return count"""
        with self._lock:
            completed_tasks = self.get_tasks_by_status(TaskStatus.COMPLETED)
            removed_count = 0
            for task in completed_tasks:
                if self.remove_task(task.task_id):
                    removed_count += 1
            return removed_count
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task"""
        task = self.get_task(task_id)
        if task and task.status in [TaskStatus.IN_PROGRESS, TaskStatus.PENDING]:
            task.cancel()
            self.logger.info(f"Cancelled task: {task_id}")
            return True
        return False
    
    def pause_task(self, task_id: str) -> bool:
        """Pause a running task"""
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.IN_PROGRESS:
            task.status = TaskStatus.PAUSED
            self.logger.info(f"Paused task: {task_id}")
            return True
        return False
    
    def resume_task(self, task_id: str) -> bool:
        """Resume a paused task"""
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.PAUSED:
            task.status = TaskStatus.IN_PROGRESS
            self.logger.info(f"Resumed task: {task_id}")
            return True
        return False

# Utility functions for backward compatibility
def create_task_executor(config: TaskConfig = None) -> TaskExecutor:
    """Factory function to create a new task executor"""
    return TaskExecutor(config)

# Example usage and testing
if __name__ == "__main__":
    async def main():
        # Create a task executor
        executor = TaskExecutor()
        
        # Create enhanced tasks
        task1 = Task(
            SecurityManager.generate_secure_id("setup"),
            "Setup project infrastructure",
            "Initialize and configure project environment",
            priority=1,
            estimated_hours=2.0,
            metadata={"environment": "development", "team": "backend"}
        )
        
        task2 = Task(
            SecurityManager.generate_secure_id("test"),
            "Implement comprehensive tests",
            "Create unit and integration tests",
            priority=2,
            estimated_hours=4.0,
            dependencies=[task1.task_id]
        )
        
        # Add tasks
        executor.add_task(task1)
        executor.add_task(task2)
        
        # Execute tasks
        results = await executor.execute_batch([task1.task_id, task2.task_id])
        
        # Print results
        for result in results:
            print(f"Task {result.task_id}: {'SUCCESS' if result.success else 'FAILED'}")
            if result.success:
                print(f"  Duration: {result.duration:.2f}s")
                print(f"  Performance: {result.performance_metrics}")
            else:
                print(f"  Error: {result.error_message}")
        
        # Print statistics
        stats = executor.get_performance_report()
        print("\nPerformance Report:")
        print(json.dumps(stats, indent=2, default=str))
    
    # Run the example
    asyncio.run(main())
