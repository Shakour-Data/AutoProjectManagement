"""
path: autoprojectmanagement/main_modules/task_workflow_management/do_important_tasks.py
File: do_important_tasks.py
Purpose: Handle important (non-urgent) tasks with strategic planning and execution
Author: AutoProjectManagement System
Version: 1.0.0
License: MIT
Description: Core module for managing important tasks using Eisenhower Matrix principles,
focusing on strategic, long-term value tasks that are important but not urgent.
"""

import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml
from enum import Enum
import uuid
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Phase 1: Basic Structure & Foundation
class TaskStatus(Enum):
    """Enumeration for task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    CANCELLED = "cancelled"

class TaskCategory(Enum):
    """Enumeration for task categories"""
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    TACTICAL = "tactical"
    DEVELOPMENT = "development"
    RESEARCH = "research"

@dataclass
class ImportantTask:
    """Data class for important task structure - Phase 1"""
    id: str
    title: str
    description: str
    priority: int  # 1-5 scale (1=highest)
    estimated_hours: float
    strategic_value: float  # 0-100 scale
    dependencies: List[str]
    deadline: Optional[datetime] = None
    created_at: datetime = None
    updated_at: datetime = None
    status: TaskStatus = TaskStatus.PENDING
    category: TaskCategory = TaskCategory.STRATEGIC
    tags: List[str] = None
    notes: List[str] = None
    completion_percentage: float = 0.0
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.tags is None:
            self.tags = []
        if self.notes is None:
            self.notes = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'estimated_hours': self.estimated_hours,
            'strategic_value': self.strategic_value,
            'dependencies': self.dependencies,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status.value,
            'category': self.category.value,
            'tags': self.tags,
            'notes': self.notes,
            'completion_percentage': self.completion_percentage
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImportantTask':
        """Create task from dictionary"""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            estimated_hours=data['estimated_hours'],
            strategic_value=data['strategic_value'],
            dependencies=data['dependencies'],
            deadline=datetime.fromisoformat(data['deadline']) if data['deadline'] else None,
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            status=TaskStatus(data['status']),
            category=TaskCategory(data['category']),
            tags=data['tags'],
            notes=data['notes'],
            completion_percentage=data['completion_percentage']
        )

# Phase 2: Core Functionality & Business Logic
class TaskStorageInterface(ABC):
    """Abstract interface for task storage - Phase 2"""
    
    @abstractmethod
    async def save_task(self, task: ImportantTask) -> bool:
        pass
    
    @abstractmethod
    async def load_tasks(self) -> List[ImportantTask]:
        pass
    
    @abstractmethod
    async def delete_task(self, task_id: str) -> bool:
        pass
    
    @abstractmethod
    async def update_task(self, task: ImportantTask) -> bool:
        pass

class JsonTaskStorage(TaskStorageInterface):
    """JSON file-based task storage implementation"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure storage file exists"""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text(json.dumps([]))
    
    async def save_task(self, task: ImportantTask) -> bool:
        """Save a single task"""
        try:
            tasks = await self.load_tasks()
            tasks.append(task)
            await self._save_all_tasks(tasks)
            return True
        except Exception as e:
            logger.error(f"Error saving task: {e}")
            return False
    
    async def load_tasks(self) -> List[ImportantTask]:
        """Load all tasks"""
        try:
            data = json.loads(self.file_path.read_text())
            return [ImportantTask.from_dict(task_data) for task_data in data]
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            return []
    
    async def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID"""
        try:
            tasks = await self.load_tasks()
            tasks = [t for t in tasks if t.id != task_id]
            await self._save_all_tasks(tasks)
            return True
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return False
    
    async def update_task(self, task: ImportantTask) -> bool:
        """Update an existing task"""
        try:
            tasks = await self.load_tasks()
            for i, t in enumerate(tasks):
                if t.id == task.id:
                    tasks[i] = task
                    break
            await self._save_all_tasks(tasks)
            return True
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return False
    
    async def _save_all_tasks(self, tasks: List[ImportantTask]) -> bool:
        """Save all tasks to storage"""
        try:
            data = [task.to_dict() for task in tasks]
            self.file_path.write_text(json.dumps(data, indent=2))
            return True
        except Exception as e:
            logger.error(f"Error saving all tasks: {e}")
            return False

# Phase 3: Advanced Features & Optimization
class TaskPrioritizer:
    """Advanced task prioritization system - Phase 3"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.weights = config.get('priority_weights', {
            'strategic_value': 0.4,
            'urgency': 0.3,
            'effort': 0.2,
            'dependencies': 0.1
        })
    
    def calculate_priority_score(self, task: ImportantTask) -> float:
        """Calculate comprehensive priority score"""
        strategic_score = task.strategic_value / 100.0
        
        # Urgency based on deadline proximity
        urgency_score = self._calculate_urgency_score(task)
        
        # Effort consideration (lower effort = higher priority)
        effort_score = 1.0 / max(task.estimated_hours, 0.5)
        
        # Dependencies impact
        dependency_score = 1.0 / max(len(task.dependencies) + 1, 1)
        
        # Weighted calculation
        score = (
            strategic_score * self.weights['strategic_value'] +
            urgency_score * self.weights['urgency'] +
            effort_score * self.weights['effort'] +
            dependency_score * self.weights['dependencies']
        )
        
        return score
    
    def _calculate_urgency_score(self, task: ImportantTask) -> float:
        """Calculate urgency score based on deadline"""
        if not task.deadline:
            return 0.5
        
        days_until_deadline = (task.deadline - datetime.now()).days
        if days_until_deadline <= 0:
            return 1.0
        elif days_until_deadline <= 7:
            return 0.8
        elif days_until_deadline <= 30:
            return 0.6
        else:
            return 0.3
    
    def sort_tasks_by_priority(self, tasks: List[ImportantTask]) -> List[ImportantTask]:
        """Sort tasks by calculated priority score"""
        return sorted(tasks, key=self.calculate_priority_score, reverse=True)

class TaskScheduler:
    """Advanced task scheduling system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.working_hours_per_day = config.get('working_hours_per_day', 8)
    
    def create_schedule(self, tasks: List[ImportantTask]) -> Dict[str, Any]:
        """Create optimal schedule for tasks"""
        # Filter pending tasks
        pending_tasks = [t for t in tasks if t.status == TaskStatus.PENDING]
        
        # Sort by priority
        prioritizer = TaskPrioritizer(self.config)
        sorted_tasks = prioritizer.sort_tasks_by_priority(pending_tasks)
        
        # Create schedule
        schedule = {
            'total_tasks': len(sorted_tasks),
            'total_hours': sum(t.estimated_hours for t in sorted_tasks),
            'estimated_days': sum(t.estimated_hours for t in sorted_tasks) / self.working_hours_per_day,
            'tasks': []
        }
        
        current_date = datetime.now()
        for task in sorted_tasks:
            task_schedule = {
                'task_id': task.id,
                'title': task.title,
                'estimated_start': current_date.isoformat(),
                'estimated_end': (current_date + timedelta(hours=task.estimated_hours)).isoformat(),
                'priority_score': prioritizer.calculate_priority_score(task)
            }
            schedule['tasks'].append(task_schedule)
            current_date += timedelta(hours=task.estimated_hours)
        
        return schedule
    
    def check_deadline_conflicts(self, tasks: List[ImportantTask]) -> List[Dict[str, Any]]:
        """Check for potential deadline conflicts"""
        conflicts = []
        schedule = self.create_schedule(tasks)
        
        for task_data in schedule['tasks']:
            task_id = task_data['task_id']
            task = next(t for t in tasks if t.id == task_id)
            
            if task.deadline:
                estimated_end = datetime.fromisoformat(task_data['estimated_end'])
                if estimated_end > task.deadline:
                    conflicts.append({
                        'task_id': task_id,
                        'title': task.title,
                        'deadline': task.deadline.isoformat(),
                        'estimated_completion': estimated_end.isoformat(),
                        'days_overdue': (estimated_end - task.deadline).days
                    })
        
        return conflicts

# Phase 4: Production-Ready Features & Integration
class ImportantTaskManager:
    """Production-ready important task manager - Phase 4"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        self.storage = JsonTaskStorage(
            self.config.get('storage_path', 'important_tasks.json')
        )
        self.prioritizer = TaskPrioritizer(self.config)
        self.scheduler = TaskScheduler(self.config)
        
    async def initialize(self) -> bool:
        """Initialize the manager"""
        try:
            await self.storage.load_tasks()
            self.logger.info("Important task manager initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize: {e}")
            return False
    
    async def create_important_task(self, 
                                  title: str,
                                  description: str,
                                  priority: int,
                                  estimated_hours: float,
                                  strategic_value: float,
                                  dependencies: List[str] = None,
                                  deadline: Optional[datetime] = None,
                                  category: TaskCategory = TaskCategory.STRATEGIC,
                                  tags: List[str] = None) -> Optional[str]:
        """Create new important task with validation"""
        try:
            if dependencies is None:
                dependencies = []
            if tags is None:
                tags = []
            
            # Validate inputs
            if not (1 <= priority <= 5):
                raise ValueError("Priority must be between 1 and 5")
            if not (0 <= strategic_value <= 100):
                raise ValueError("Strategic value must be between 0 and 100")
            if estimated_hours <= 0:
                raise ValueError("Estimated hours must be positive")
            
            task = ImportantTask(
                id=str(uuid.uuid4()),
                title=title,
                description=description,
                priority=priority,
                estimated_hours=estimated_hours,
                strategic_value=strategic_value,
                dependencies=dependencies,
                deadline=deadline,
                category=category,
                tags=tags
            )
            
            await self.storage.save_task(task)
            self.logger.info(f"Created important task: {task.title} (ID: {task.id})")
            return task.id
            
        except Exception as e:
            self.logger.error(f"Error creating task: {e}")
            return None
    
    async def get_task(self, task_id: str) -> Optional[ImportantTask]:
        """Get task by ID"""
        try:
            tasks = await self.storage.load_tasks()
            return next((t for t in tasks if t.id == task_id), None)
        except Exception as e:
            self.logger.error(f"Error getting task: {e}")
            return None
    
    async def update_task_status(self, task_id: str, status: TaskStatus, 
                               completion_percentage: float = None) -> bool:
        """Update task status and completion percentage"""
        try:
            task = await self.get_task(task_id)
            if not task:
                return False
            
            task.status = status
            if completion_percentage is not None:
                task.completion_percentage = completion_percentage
            task.updated_at = datetime.now()
            
            await self.storage.update_task(task)
            self.logger.info(f"Updated task {task_id} status to {status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating task status: {e}")
            return False
    
    async def get_prioritized_tasks(self, limit: Optional[int] = None) -> List[ImportantTask]:
        """Get tasks sorted by priority"""
        try:
            tasks = await self.storage.load_tasks()
            sorted_tasks = self.prioritizer.sort_tasks_by_priority(tasks)
            return sorted_tasks[:limit] if limit else sorted_tasks
        except Exception as e:
            self.logger.error(f"Error getting prioritized tasks: {e}")
            return []
    
    async def get_schedule(self) -> Dict[str, Any]:
        """Get optimized schedule for all pending tasks"""
        try:
            tasks = await self.storage.load_tasks()
            return self.scheduler.create_schedule(tasks)
        except Exception as e:
            self.logger.error(f"Error creating schedule: {e}")
            return {}
    
    async def get_deadline_conflicts(self) -> List[Dict[str, Any]]:
        """Get potential deadline conflicts"""
        try:
            tasks = await self.storage.load_tasks()
            return self.scheduler.check_deadline_conflicts(tasks)
        except Exception as e:
            self.logger.error(f"Error checking deadline conflicts: {e}")
            return []
    
    async def get_strategic_insights(self) -> Dict[str, Any]:
        """Get strategic insights and analytics"""
        try:
            tasks = await self.storage.load_tasks()
            
            insights = {
                'total_tasks': len(tasks),
                'completed_tasks': len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
                'pending_tasks': len([t for t in tasks if t.status == TaskStatus.PENDING]),
                'in_progress_tasks': len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS]),
                'total_strategic_value': sum(t.strategic_value for t in tasks),
                'total_estimated_hours': sum(t.estimated_hours for t in tasks),
                'average_priority': sum(t.priority for t in tasks) / len(tasks) if tasks else 0,
                'category_distribution': {},
                'high_priority_tasks': [t.to_dict() for t in tasks if t.priority <= 2],
                'overdue_tasks': []
            }
            
            # Category distribution
            for category in TaskCategory:
                count = len([t for t in tasks if t.category == category])
                insights['category_distribution'][category.value] = count
            
            # Overdue tasks
            for task in tasks:
                if task.deadline and task.deadline < datetime.now() and task.status != TaskStatus.COMPLETED:
                    insights['overdue_tasks'].append(task.to_dict())
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error getting strategic insights: {e}")
            return {}
    
    async def cleanup_completed_tasks(self, days_to_keep: int = 30) -> int:
        """Clean up old completed tasks"""
        try:
            tasks = await self.storage.load_tasks()
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            cleaned_count = 0
            for task in tasks:
                if (task.status == TaskStatus.COMPLETED and 
                    task.updated_at < cutoff_date):
                    await self.storage.delete_task(task.id)
                    cleaned_count += 1
            
            self.logger.info(f"Cleaned up {cleaned_count} old completed tasks")
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up tasks: {e}")
            return 0
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration with defaults"""
        default_config = {
            'storage_path': 'important_tasks.json',
            'max_tasks': 100,
            'priority_threshold': 3,
            'strategic_value_threshold': 70,
            'working_hours_per_day': 8,
            'priority_weights': {
                'strategic_value': 0.4,
                'urgency': 0.3,
                'effort': 0.2,
                'dependencies': 0.1
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                    default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Error loading config file: {e}")
                
        return default_config

# Utility functions for backward compatibility
async def create_important_task_manager(config_path: Optional[str] = None) -> ImportantTaskManager:
    """Factory function to create task manager"""
    manager = ImportantTaskManager(config_path)
    await manager.initialize()
    return manager

# Example usage and testing
async def main():
    """Example usage of the important task manager"""
    manager = await create_important_task_manager()
    
    # Create sample important tasks
    task1_id = await manager.create_important_task(
        title="Develop Strategic Project Roadmap",
        description="Create comprehensive 6-month project roadmap with milestones",
        priority=1,
        estimated_hours=8.0,
        strategic_value=95.0,
        deadline=datetime.now() + timedelta(days=14),
        category=TaskCategory.STRATEGIC,
        tags=["planning", "roadmap", "strategy"]
    )
    
    task2_id = await manager.create_important_task(
        title="Implement Automated Testing Framework",
        description="Set up comprehensive testing framework for all modules",
        priority=2,
        estimated_hours=16.0,
        strategic_value=85.0,
        category=TaskCategory.DEVELOPMENT,
        tags=["testing", "automation", "quality"]
    )
    
    # Get prioritized tasks
    prioritized = await manager.get_prioritized_tasks()
    print(f"Top priority tasks: {len(prioritized)}")
    
    # Get schedule
    schedule = await manager.get_schedule()
    print(f"Total estimated days: {schedule.get('estimated_days', 0)}")
    
    # Get insights
    insights = await manager.get_strategic_insights()
    print(f"Total strategic value: {insights.get('total_strategic_value', 0)}")
    
    return manager

if __name__ == "__main__":
    asyncio.run(main())
