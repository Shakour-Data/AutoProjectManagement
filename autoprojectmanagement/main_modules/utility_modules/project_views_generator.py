import os
import json
import yaml
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from pathlib import Path

class ProjectViewsGenerator:
    """
    Automated project views generator for Board, Table, and Roadmap views
    based on WBS structure with automatic status updates from commits
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.workflows_dir = os.path.join(project_root, '.github', 'workflows')
        self.projects_dir = os.path.join(project_root, '.github', 'projects')
        self.wbs_dir = os.path.join(project_root, 'JSonDataBase', 'Inputs', 'UserInputs', 'wbs_parts')
        self.logger = logging.getLogger(__name__)
        
    def create_complete_project_views(self, project_config: Dict[str, Any]) -> bool:
        """
        Create complete project views: Board, Table, and Roadmap
        based on WBS structure with automatic updates
        
        Args:
            project_config: Project configuration
            
        Returns:
            bool: Success status
        """
        try:
            # Create directory structure
            self._create_views_structure()
            
            # Load WBS data
            wbs_data = self._load_wbs_data()
            
            # Create views based on WBS
            self._create_board_view(wbs_data, project_config)
            self._create_table_view(wbs_data, project_config)
            self._create_roadmap_view(wbs_data, project_config)
            
            # Create automated workflows
            self._create_views_workflows()
            
            # Create view templates
            self._create_views_templates()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating project views: {str(e)}")
            return False
    
    def _create_views_structure(self):
        """Create directory structure for views"""
        os.makedirs(self.projects_dir, exist_ok=True)
        os.makedirs(self.workflows_dir, exist_ok=True)
    
    def _load_wbs_data(self) -> Dict[str, Any]:
        """Load WBS data from JSON files"""
        wbs_data = {}
        if os.path.exists(self.wbs_dir):
            for root, dirs, files in os.walk(self.wbs_dir):
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                wbs_data[file] = data
                        except Exception as e:
                            self.logger.warning(f"Could not load {file_path}: {e}")
        return wbs_data
    
    def _create_board_view(self, wbs_data: Dict[str, Any], config: Dict[str, Any]):
        """Create Kanban board view based on WBS structure"""
        board_config = {
            'name': 'Project Kanban Board',
            'description': 'Automated Kanban board based on WBS structure',
            'type': 'board',
            'columns': self._generate_board_columns(wbs_data),
            'automation': {
                'status_updates': 'commit-based',
                'progress_calculation': 'automatic',
                'cost_tracking': 'enabled',
                'assignee_sync': 'enabled'
            }
        }
        
        with open(os.path.join(self.projects_dir, 'board-config.json'), 'w') as f:
            json.dump(board_config, f, indent=4)
    
    def _create_table_view(self, wbs_data: Dict[str, Any], config: Dict[str, Any]):
        """Create detailed table view based on WBS structure"""
        table_config = {
            'name': 'Project Table View',
            'description': 'Detailed table view with WBS-based tracking',
            'type': 'table',
            'columns': [
                {
                    'name': 'WBS Code',
                    'field': 'wbs_code',
                    'type': 'text',
                    'description': 'WBS hierarchical code (e.g., 1.2.3)'
                },
                {
                    'name': 'Task',
                    'field': 'title',
                    'type': 'text',
                    'description': 'WBS task title'
                },
                {
                    'name': 'Status',
                    'field': 'status',
                    'type': 'single_select',
                    'options': ['Not Started', 'In Progress', 'Review', 'Completed'],
                    'auto_update': True
                },
                {
                    'name': 'Progress',
                    'field': 'progress',
                    'type': 'number',
                    'description': 'Completion percentage (0-100)',
                    'auto_calculate': True
                },
                {
                    'name': 'Planned Progress',
                    'field': 'planned_progress',
                    'type': 'number',
                    'description': 'Expected progress based on timeline'
                },
                {
                    'name': 'Actual Progress',
                    'field': 'actual_progress',
                    'type': 'number',
                    'description': 'Actual progress from commits'
                },
                {
                    'name': 'Assignee',
                    'field': 'assignee',
                    'type': 'text'
                },
                {
                    'name': 'Priority',
                    'field': 'priority',
                    'type': 'single_select',
                    'options': ['Critical', 'High', 'Medium', 'Low']
                },
                {
                    'name': 'Due Date',
                    'field': 'due_date',
                    'type': 'date'
                },
                {
                    'name': 'Estimated Hours',
                    'field': 'estimated_hours',
                    'type': 'number'
                },
                {
                    'name': 'Actual Hours',
                    'field': 'actual_hours',
                    'type': 'number'
                }
            ],
            'filters': [
                {
                    'name': 'Status',
                    'field': 'status',
                    'type': 'select'
                },
                {
                    'name': 'Assignee',
                    'field': 'assignee',
                    'type': 'text'
                }
            ],
            'sorting': [
                {
                    'field': 'priority',
                    'direction': 'desc'
                },
                {
                    'field': 'due_date',
                    'direction': 'asc'
                }
            ]
        }
        
        with open(os.path.join(self.projects_dir, 'table-config.json'), 'w') as f:
            json.dump(table_config, f, indent=4)
    
    def _create_roadmap_view(self, wbs_data: Dict[str, Any], config: Dict[str, Any]):
        """Create roadmap view based on WBS structure"""
        roadmap_config = {
            'name': 'Project Roadmap',
            'description': 'Timeline-based roadmap view with WBS milestones',
            'type': 'roadmap',
            'timeline': {
                'start_date': config.get('start_date', datetime.now().isoformat()),
                'end_date': config.get('end_date', None),
                'milestones': self._generate_roadmap_milestones(wbs_data)
            },
            'phases': self._generate_roadmap_phases(wbs_data),
            'dependencies': self._generate_dependencies(wbs_data)
        }
        
        with open(os.path.join(self.projects_dir, 'roadmap-config.json'), 'w') as f:
            json.dump(roadmap_config, f, indent=4)
    
    def _generate_board_columns(self, wbs_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate board columns based on WBS structure"""
        columns = []
        
        # Standard Kanban columns
        standard_columns = [
            {'name': 'Backlog', 'description': 'Tasks ready to start'},
            {'name': 'In Progress', 'description': 'Tasks currently being worked on'},
            {'name': 'Review', 'description': 'Tasks ready for review'},
            {'name': 'Completed', 'description': 'Completed tasks'}
        ]
        
        for col in standard_columns:
            columns.append({
                'name': col['name'],
                'description': col['description'],
                'wip_limit': 5,
                'auto_assignment': True
            })
        
        return columns
    
    def _generate_roadmap_milestones(self, wbs_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate roadmap milestones from WBS data"""
        milestones = []
        
        # Extract milestones from WBS phases
        for filename, data in wbs_data.items():
            if isinstance(data, dict) and 'phases' in data:
                for phase in data['phases']:
                    milestones.append({
                        'name': phase.get('name', 'Milestone'),
                        'description': phase.get('description', ''),
                        'due_date': phase.get('end_date', ''),
                        'progress': 0,
                        'status': 'planned'
                    })
        
        return milestones
    
    def _generate_roadmap_phases(self, wbs_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate roadmap phases from WBS structure"""
        phases = []
        
        for filename, data in wbs_data.items():
            if isinstance(data, dict) and 'phases' in data:
                for phase in data['phases']:
                    phases.append({
                        'name': phase.get('name', 'Phase'),
                        'description': phase.get('description', ''),
                        'start_date': phase.get('start_date', ''),
                        'end_date': phase.get('end_date', ''),
                        'tasks': phase.get('tasks', []),
                        'progress': 0
                    })
        
        return phases
    
    def _generate_dependencies(self, wbs_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate task dependencies from WBS data"""
        dependencies = []
        
        # Simple dependency generation based on WBS structure
        task_ids = []
        for filename, data in wbs_data.items():
            if isinstance(data, dict) and 'tasks' in data:
                for task in data['tasks']:
                    task_ids.append(task.get('id', ''))
        
        # Create sequential dependencies
        for i in range(1, len(task_ids)):
            dependencies.append({
                'from': task_ids[i-1],
                'to': task_ids[i],
                'type': 'finish_to_start'
            })
        
        return dependencies
    
    def _create_views_workflows(self):
        """Create GitHub Actions workflows for automated view updates"""
        workflow_content = {
            'name': 'Update Project Views',
            'on': {
                'push': {
                    'branches': ['main', 'develop']
                },
                'pull_request': {
                    'types': ['opened', 'synchronize', 'closed']
                },
                'schedule': [
                    {'cron': '0 9 * * 1'}  # Weekly on Monday at 9 AM
                ]
            },
            'jobs': {
                'update-views': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {
                            'name': 'Checkout code',
                            'uses': 'actions/checkout@v3'
                        },
                        {
                            'name': 'Set up Python',
                            'uses': 'actions/setup-python@v4',
                            'with': {
                                'python-version': '3.9'
                            }
                        },
                        {
                            'name': 'Install dependencies',
                            'run': 'pip install -r requirements.txt'
                        },
                        {
                            'name': 'Update project views',
                            'run': 'python -m autoprojectmanagement.main_modules.project_views_generator'
                        },
                        {
                            'name': 'Commit changes',
                            'run': 'git config --local user.email "action@github.com" && git config --local user.name "GitHub Action" && git add . && git diff --staged --quiet || git commit -m "Auto-update project views [skip ci]" && git push'
                        }
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'update-views.yml'), 'w') as f:
            yaml.dump(workflow_content, f, default_flow_style=False)
    
    def _create_views_templates(self):
        """Create view templates for consistent formatting"""
        templates = {
            'board_template': {
                'columns': ['Backlog', 'In Progress', 'Review', 'Completed'],
                'labels': ['bug', 'feature', 'enhancement', 'documentation'],
                'assignees': [],
                'milestones': []
            },
            'table_template': {
                'columns': ['Task', 'Status', 'Priority', 'Assignee', 'Due Date', 'Progress'],
                'filters': ['status', 'priority', 'assignee'],
                'sorting': ['priority', 'due_date']
            },
            'roadmap_template': {
                'phases': ['Planning', 'Development', 'Testing', 'Deployment'],
                'milestones': ['Alpha', 'Beta', 'Release Candidate', 'Final Release']
            }
        }
        
        with open(os.path.join(self.projects_dir, 'view-templates.json'), 'w') as f:
            json.dump(templates, f, indent=4)
    
    def update_views_from_commits(self, commit_data: Dict[str, Any]) -> bool:
        """
        Update project views based on commit data
        
        Args:
            commit_data: Commit information with task updates
            
        Returns:
            bool: Success status
        """
        try:
            # Update board view
            self._update_board_from_commits(commit_data)
            
            # Update table view
            self._update_table_from_commits(commit_data)
            
            # Update roadmap view
            self._update_roadmap_from_commits(commit_data)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating views from commits: {str(e)}")
            return False
    
    def _update_board_from_commits(self, commit_data: Dict[str, Any]):
        """Update board view based on commit data"""
        # Implementation for updating board view
        pass
    
    def _update_table_from_commits(self, commit_data: Dict[str, Any]):
        """Update table view based on commit data"""
        # Implementation for updating table view
        pass
    
    def _update_roadmap_from_commits(self, commit_data: Dict[str, Any]):
        """Update roadmap view based on commit data"""
        # Implementation for updating roadmap view
        pass
