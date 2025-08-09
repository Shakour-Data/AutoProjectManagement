"""
Unit tests for progress_data_generator_refactored module.

Tests data generation logic and output format validation.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from project_management.modules.main_modules.progress_data_generator_refactored import ProgressDataGenerator


class TestProgressDataGenerator:
    """Test cases for ProgressDataGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ProgressDataGenerator()
    
    def test_generate_progress_summary_valid_data(self):
        """Test progress summary generation with valid data."""
        tasks = [
            {"id": 1, "name": "Task 1", "status": "completed", "progress": 100},
            {"id": 2, "name": "Task 2", "status": "in_progress", "progress": 50},
            {"id": 3, "name": "Task 3", "status": "not_started", "progress": 0}
        ]
        
        result = self.generator.generate_progress_summary(tasks)
        
        assert "total_tasks" in result
        assert "completed_tasks" in result
        assert "in_progress_tasks" in result
        assert "not_started_tasks" in result
        assert "overall_progress" in result
        assert result["total_tasks"] == 3
    
    def test_generate_task_progress_report(self):
        """Test task progress report generation."""
        tasks = [
            {"id": 1, "name": "Task 1", "status": "completed", "progress": 100, "estimated_hours": 10, "actual_hours": 8},
            {"id": 2, "name": "Task 2", "status": "in_progress", "progress": 75, "estimated_hours": 20, "actual_hours": 15}
        ]
        
        result = self.generator.generate_task_progress_report(tasks)
        
        assert isinstance(result, dict)
        assert "tasks" in result
        assert "summary" in result
    
    def test_generate_milestone_report(self):
        """Test milestone report generation."""
        milestones = [
            {"id": 1, "name": "Milestone 1", "status": "completed", "due_date": "2023-12-01", "completion_date": "2023-11-30"},
            {"id": 2, "name": "Milestone 2", "status": "in_progress", "due_date": "2024-01-15", "completion_date": None}
        ]
        
        result = self.generator.generate_milestone_report(milestones)
        
        assert isinstance(result, dict)
        assert "milestones" in result
        assert "summary" in result
    
    def test_generate_resource_utilization_report(self):
        """Test resource utilization report generation."""
        resources = [
            {"id": 1, "name": "Resource 1", "allocated_hours": 40, "used_hours": 30},
            {"id": 2, "name": "Resource 2", "allocated_hours": 60, "used_hours": 45}
        ]
        
        result = self.generator.generate_resource_utilization_report(resources)
        
        assert isinstance(result, dict)
        assert "resources" in result
        assert "summary" in result
    
    def test_generate_time_tracking_report(self):
        """Test time tracking report generation."""
        time_entries = [
            {"task_id": 1, "hours": 5, "date": "2023-12-01"},
            {"task_id": 2, "hours": 3, "date": "2023-12-02"},
            {"task_id": 1, "hours": 2, "date": "2023-12-03"}
        ]
        
        result = self.generator.generate_time_tracking_report(time_entries)
        
        assert isinstance(result, dict)
        assert "time_entries" in result
        assert "summary" in result
    
    def test_generate_burndown_chart_data(self):
        """Test burndown chart data generation."""
        sprint_data = {
            "start_date": "2023-12-01",
            "end_date": "2023-12-15",
            "total_story_points": 100,
            "daily_progress": [
                {"date": "2023-12-01", "remaining_points": 100},
                {"date": "2023-12-02", "remaining_points": 90},
                {"date": "2023-12-03", "remaining_points": 80}
            ]
        }
        
        result = self.generator.generate_burndown_chart_data(sprint_data)
        
        assert isinstance(result, dict)
        assert "chart_data" in result
        assert "ideal_line" in result
        assert "actual_line" in result
    
    def test_generate_velocity_chart_data(self):
        """Test velocity chart data generation."""
        velocity_data = {
            "sprints": [
                {"name": "Sprint 1", "completed_points": 40},
                {"name": "Sprint 2", "completed_points": 50},
                {"name": "Sprint 3", "completed_points": 45}
            ]
        }
        
        result = self.generator.generate_velocity_chart_data(velocity_data)
        
        assert isinstance(result, dict)
        assert "chart_data" in result
        assert "average_velocity" in result
    
    def test_generate_cumulative_flow_diagram_data(self):
        """Test cumulative flow diagram data generation."""
        cfd_data = {
            "dates": ["2023-12-01", "2023-12-02", "2023-12-03"],
            "status_counts": {
                "todo": [10, 8, 6],
                "in_progress": [5, 7, 8],
                "done": [15, 20, 25]
            }
        }
        
        result = self.generator.generate_cumulative_flow_diagram_data(cfd_data)
        
        assert isinstance(result, dict)
        assert "chart_data" in result
        assert "dates" in result
    
    def test_generate_workload_distribution_report(self):
        """Test workload distribution report generation."""
        workload_data = {
            "team_members": [
                {"name": "Alice", "assigned_tasks": 5, "estimated_hours": 40},
                {"name": "Bob", "assigned_tasks": 3, "estimated_hours": 24},
                {"name": "Charlie", "assigned_tasks": 7, "estimated_hours": 56}
            ]
        }
        
        result = self.generator.generate_workload_distribution_report(workload_data)
        
        assert isinstance(result, dict)
        assert "team_members" in result
        assert "distribution" in result
    
    def test_generate_risk_assessment_report(self):
        """Test risk assessment report generation."""
        risks = [
            {"id": 1, "description": "Risk 1", "probability": 0.3, "impact": "high"},
            {"id": 2, "description": "Risk 2", "probability": 0.7, "impact": "medium"}
        ]
        
        result = self.generator.generate_risk_assessment_report(risks)
        
        assert isinstance(result, dict)
        assert "risks" in result
        assert "summary" in result
    
    def test_generate_quality_metrics_report(self):
        """Test quality metrics report generation."""
        quality_data = {
            "defects": [
                {"severity": "high", "count": 5},
                {"severity": "medium", "count": 15},
                {"severity": "low", "count": 25}
            ],
            "test_coverage": 85,
            "code_quality_score": 7.5
        }
        
        result = self.generator.generate_quality_metrics_report(quality_data)
        
        assert isinstance(result, dict)
        assert "metrics" in result
        assert "summary" in result
    
    def test_generate_sprint_retrospective_data(self):
        """Test sprint retrospective data generation."""
        retrospective_data = {
            "sprint_name": "Sprint 1",
            "completed_stories": 10,
            "planned_stories": 12,
            "team_feedback": ["Good communication", "Need better estimation"],
            "improvements": ["Improve story estimation", "Better daily standups"]
        }
        
        result = self.generator.generate_sprint_retrospective_data(retrospective_data)
        
        assert isinstance(result, dict)
        assert "sprint_name" in result
        assert "completed_stories" in result
        assert "improvements" in result
    
    def test_generate_project_health_report(self):
        """Test project health report generation."""
        health_data = {
            "schedule_variance": 0.1,
            "cost_variance": -0.05,
            "quality_score": 8.5,
            "team_satisfaction": 9.0,
            "stakeholder_satisfaction": 8.0
        }
        
        result = self.generator.generate_project_health_report(health_data)
        
        assert isinstance(result, dict)
        assert "health_score" in result
        assert "status" in result
        assert "recommendations" in result
    
    def test_generate_performance_dashboard_data(self):
        """Test performance dashboard data generation."""
        dashboard_data = {
            "kpis": [
                {"name": "Task Completion Rate", "value": 85, "target": 90},
                {"name": "On-time Delivery", "value": 92, "target": 95},
                {"name": "Quality Score", "value": 8.5, "target": 9.0}
            ]
        }
        
        result = self.generator.generate_performance_dashboard_data(dashboard_data)
        
        assert isinstance(result, dict)
        assert "kpis" in result
        assert "dashboard" in result
