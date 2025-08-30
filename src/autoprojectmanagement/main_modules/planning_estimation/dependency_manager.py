"""
Dependency Manager Module - Handles task dependencies and validation
"""

from typing import Dict, List, Set, Any
import json

class DependencyManager:
    """
    Manages task dependencies including validation, circular dependency detection,
    and dependency relationship processing.
    """
    
    def __init__(self):
        self.task_dependencies: Dict[str, List[str]] = {}
        self.task_reverse_dependencies: Dict[str, List[str]] = {}
        
    def load_dependencies_from_wbs(self, wbs_data: Dict[str, Any]) -> None:
        """
        Load dependencies from WBS structure.
        
        Args:
            wbs_data: The WBS structure containing tasks with dependencies
        """
        self._extract_dependencies(wbs_data)
        
    def _extract_dependencies(self, task: Dict[str, Any]) -> None:
        """
        Recursively extract dependencies from WBS tasks.
        """
        task_id = task.get('id')
        dependencies = task.get('dependencies', [])
        
        if task_id and dependencies:
            self.task_dependencies[task_id] = dependencies
            # Build reverse dependency mapping
            for dep_id in dependencies:
                if dep_id not in self.task_reverse_dependencies:
                    self.task_reverse_dependencies[dep_id] = []
                self.task_reverse_dependencies[dep_id].append(task_id)
        
        # Process subtasks recursively
        for subtask in task.get('subtasks', []):
            self._extract_dependencies(subtask)
    
    def validate_dependencies(self) -> List[str]:
        """
        Validate all dependencies in the system.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Check for missing dependency targets
        for task_id, dependencies in self.task_dependencies.items():
            for dep_id in dependencies:
                if dep_id not in self.task_dependencies and dep_id not in self.task_reverse_dependencies:
                    errors.append(f"Task '{task_id}' depends on non-existent task '{dep_id}'")
        
        # Check for circular dependencies
        circular_deps = self.detect_circular_dependencies()
        if circular_deps:
            errors.append(f"Circular dependencies detected: {circular_deps}")
            
        return errors
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """
        Detect circular dependencies using DFS.
        
        Returns:
            List of circular dependency chains
        """
        visited: Set[str] = set()
        recursion_stack: Set[str] = set()
        circular_chains: List[List[str]] = []
        
        def dfs(current_task: str, path: List[str]) -> None:
            if current_task in recursion_stack:
                # Found a cycle
                cycle_start = path.index(current_task)
                circular_chains.append(path[cycle_start:] + [current_task])
                return
                
            if current_task in visited:
                return
                
            visited.add(current_task)
            recursion_stack.add(current_task)
            path.append(current_task)
            
            # Check all dependencies of current task
            for dep_id in self.task_dependencies.get(current_task, []):
                if dep_id in self.task_dependencies:  # Only follow if it's a task that has dependencies
                    dfs(dep_id, path.copy())
                elif dep_id in self.task_reverse_dependencies:  # Task exists but has no dependencies
                    pass  # No circular dependency from leaf nodes
            
            recursion_stack.remove(current_task)
            path.pop()
        
        # Start DFS from all tasks that have dependencies
        for task_id in list(self.task_dependencies.keys()):
            if task_id not in visited:
                dfs(task_id, [])
                
        return circular_chains
    
    def get_task_predecessors(self, task_id: str) -> List[str]:
        """
        Get all direct predecessors of a task.
        
        Args:
            task_id: The task ID
            
        Returns:
            List of predecessor task IDs
        """
        return self.task_dependencies.get(task_id, [])
    
    def get_task_successors(self, task_id: str) -> List[str]:
        """
        Get all direct successors of a task.
        
        Args:
            task_id: The task ID
            
        Returns:
            List of successor task IDs
        """
        return self.task_reverse_dependencies.get(task_id, [])
    
    def get_all_dependencies(self, task_id: str) -> Dict[str, List[str]]:
        """
        Get all dependencies (predecessors and successors) for a task.
        
        Args:
            task_id: The task ID
            
        Returns:
            Dictionary with 'predecessors' and 'successors' lists
        """
        return {
            'predecessors': self.get_task_predecessors(task_id),
            'successors': self.get_task_successors(task_id)
        }
    
    def is_task_blocked(self, task_id: str, completed_tasks: Set[str]) -> bool:
        """
        Check if a task is blocked by incomplete dependencies.
        
        Args:
            task_id: The task ID to check
            completed_tasks: Set of completed task IDs
            
        Returns:
            True if task is blocked, False otherwise
        """
        predecessors = self.get_task_predecessors(task_id)
        return any(predecessor not in completed_tasks for predecessor in predecessors)
    
    def get_critical_path(self, task_durations: Dict[str, int]) -> List[str]:
        """
        Calculate critical path using topological sort and longest path algorithm.
        
        Args:
            task_durations: Dictionary mapping task IDs to durations
            
        Returns:
            List of task IDs in the critical path
        """
        # This is a simplified implementation
        # In a real system, you'd use topological sort and dynamic programming
        
        # For now, return tasks with the longest duration as a placeholder
        critical_tasks = []
        max_duration = 0
        
        for task_id, duration in task_durations.items():
            if duration > max_duration:
                max_duration = duration
                critical_tasks = [task_id]
            elif duration == max_duration:
                critical_tasks.append(task_id)
                
        return critical_tasks

# Example usage
if __name__ == "__main__":
    # Load sample WBS with dependencies
    sample_wbs = {
        "id": "project_root",
        "name": "Test Project",
        "subtasks": [
            {
                "id": "task_1",
                "name": "Task 1",
                "dependencies": []
            },
            {
                "id": "task_2", 
                "name": "Task 2",
                "dependencies": ["task_1"]
            },
            {
                "id": "task_3",
                "name": "Task 3",
                "dependencies": ["task_2"]
            }
        ]
    }
    
    manager = DependencyManager()
    manager.load_dependencies_from_wbs(sample_wbs)
    
    # Validate dependencies
    errors = manager.validate_dependencies()
    if errors:
        print("Dependency validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Dependencies are valid!")
    
    # Test circular dependency detection
    circular_deps = manager.detect_circular_dependencies()
    if circular_deps:
        print("Circular dependencies found:")
        for chain in circular_deps:
            print(f"  - {' -> '.join(chain)}")
    else:
        print("No circular dependencies found")
