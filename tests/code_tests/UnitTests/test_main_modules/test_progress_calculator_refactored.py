"""
Unit tests for progress_calculator_refactored module.

Tests progress calculation algorithms and edge cases.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from project_management.modules.main_modules.progress_calculator_refactored import ProgressCalculator


class TestProgressCalculator:
    """Test cases for ProgressCalculator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = ProgressCalculator()
    
    def test_calculate_percentage_progress_normal_case(self):
        """Test percentage progress calculation with normal inputs."""
        test_cases = [
            (50, 100, 50.0),
            (75, 100, 75.0),
            (0, 100, 0.0),
            (100, 100, 100.0),
            (25, 50, 50.0),
            (10, 200, 5.0)
        ]
        
        for completed, total, expected in test_cases:
            result = self.calculator.calculate_percentage_progress(completed, total)
            assert abs(result - expected) < 0.001
    
    def test_calculate_percentage_progress_zero_total(self):
        """Test percentage progress calculation with zero total."""
        with pytest.raises(ValueError, match="Total cannot be zero"):
            self.calculator.calculate_percentage_progress(50, 0)
    
    def test_calculate_percentage_progress_negative_values(self):
        """Test percentage progress calculation with negative values."""
        with pytest.raises(ValueError, match="Values cannot be negative"):
            self.calculator.calculate_percentage_progress(-10, 100)
        
        with pytest.raises(ValueError, match="Values cannot be negative"):
            self.calculator.calculate_percentage_progress(50, -100)
    
    def test_calculate_percentage_progress_completed_exceeds_total(self):
        """Test percentage progress when completed exceeds total."""
        result = self.calculator.calculate_percentage_progress(150, 100)
        assert result == 150.0
    
    def test_calculate_task_completion_rate(self):
        """Test task completion rate calculation."""
        test_cases = [
            (5, 10, 0.5),
            (8, 8, 1.0),
            (0, 5, 0.0),
            (3, 12, 0.25)
        ]
        
        for completed, total, expected in test_cases:
            result = self.calculator.calculate_task_completion_rate(completed, total)
            assert abs(result - expected) < 0.001
    
    def test_calculate_milestone_progress(self):
        """Test milestone progress calculation."""
        milestones = [
            {"name": "Milestone 1", "completed": True, "weight": 0.3},
            {"name": "Milestone 2", "completed": False, "weight": 0.4},
            {"name": "Milestone 3", "completed": True, "weight": 0.3}
        ]
        
        result = self.calculator.calculate_milestone_progress(milestones)
        expected = 0.6  # 0.3 + 0.3 = 0.6
        assert abs(result - expected) < 0.001
    
    def test_calculate_milestone_progress_empty_list(self):
        """Test milestone progress calculation with empty list."""
        result = self.calculator.calculate_milestone_progress([])
        assert result == 0.0
    
    def test_calculate_milestone_progress_zero_weights(self):
        """Test milestone progress calculation with zero weights."""
        milestones = [
            {"name": "Milestone 1", "completed": True, "weight": 0.0},
            {"name": "Milestone 2", "completed": False, "weight": 0.0}
        ]
        
        result = self.calculator.calculate_milestone_progress(milestones)
        assert result == 0.0
    
    def test_calculate_time_based_progress(self):
        """Test time-based progress calculation."""
        start_date = datetime(2023, 1, 1)
        current_date = datetime(2023, 6, 15)
        end_date = datetime(2023, 12, 31)
        
        result = self.calculator.calculate_time_based_progress(start_date, current_date, end_date)
        expected = 0.5  # Approximately 50% of time elapsed
        assert abs(result - expected) < 0.05
    
    def test_calculate_time_based_progress_before_start(self):
        """Test time-based progress calculation when current date is before start."""
        start_date = datetime(2023, 6, 1)
        current_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        
        result = self.calculator.calculate_time_based_progress(start_date, current_date, end_date)
        assert result == 0.0
    
    def test_calculate_time_based_progress_after_end(self):
        """Test time-based progress calculation when current date is after end."""
        start_date = datetime(2023, 1, 1)
        current_date = datetime(2024, 1, 1)
        end_date = datetime(2023, 12, 31)
        
        result = self.calculator.calculate_time_based_progress(start_date, current_date, end_date)
        assert result == 1.0
    
    def test_calculate_weighted_progress(self):
        """Test weighted progress calculation."""
        tasks = [
            {"progress": 50, "weight": 0.3},
            {"progress": 75, "weight": 0.4},
            {"progress": 25, "weight": 0.3}
        ]
        
        result = self.calculator.calculate_weighted_progress(tasks)
        expected = (50 * 0.3 + 75 * 0.4 + 25 * 0.3)  # 15 + 30 + 7.5 = 52.5
        assert abs(result - 52.5) < 0.001
    
    def test_calculate_weighted_progress_zero_weights(self):
        """Test weighted progress calculation with zero weights."""
        tasks = [
            {"progress": 50, "weight": 0.0},
            {"progress": 75, "weight": 0.0}
        ]
        
        result = self.calculator.calculate_weighted_progress(tasks)
        assert result == 0.0
    
    def test_calculate_weighted_progress_empty_list(self):
        """Test weighted progress calculation with empty list."""
        result = self.calculator.calculate_weighted_progress([])
        assert result == 0.0
    
    def test_calculate_efficiency_score(self):
        """Test efficiency score calculation."""
        planned_hours = 100
        actual_hours = 80
        
        result = self.calculator.calculate_efficiency_score(planned_hours, actual_hours)
        expected = 1.25  # 100/80 = 1.25
        assert abs(result - expected) < 0.001
    
    def test_calculate_efficiency_score_zero_actual(self):
        """Test efficiency score calculation with zero actual hours."""
        with pytest.raises(ValueError, match="Actual hours cannot be zero"):
            self.calculator.calculate_efficiency_score(100, 0)
    
    def test_calculate_velocity(self):
        """Test velocity calculation."""
        completed_points = 50
        days_elapsed = 10
        
        result = self.calculator.calculate_velocity(completed_points, days_elapsed)
        expected = 5.0  # 50/10 = 5.0
        assert abs(result - expected) < 0.001
    
    def test_calculate_velocity_zero_days(self):
        """Test velocity calculation with zero days elapsed."""
        with pytest.raises(ValueError, match="Days elapsed cannot be zero"):
            self.calculator.calculate_velocity(50, 0)
    
    def test_calculate_burn_rate(self):
        """Test burn rate calculation."""
        remaining_work = 100
        remaining_days = 20
        
        result = self.calculator.calculate_burn_rate(remaining_work, remaining_days)
        expected = 5.0  # 100/20 = 5.0
        assert abs(result - expected) < 0.001
    
    def test_calculate_burn_rate_zero_days(self):
        """Test burn rate calculation with zero remaining days."""
        with pytest.raises(ValueError, match="Remaining days cannot be zero"):
            self.calculator.calculate_burn_rate(100, 0)
    
    def test_calculate_completion_forecast(self):
        """Test completion forecast calculation."""
        remaining_work = 100
        current_velocity = 5
        
        result = self.calculator.calculate_completion_forecast(remaining_work, current_velocity)
        expected = 20  # 100/5 = 20
        assert abs(result - expected) < 0.001
    
    def test_calculate_completion_forecast_zero_velocity(self):
        """Test completion forecast calculation with zero velocity."""
        with pytest.raises(ValueError, match="Current velocity cannot be zero"):
            self.calculator.calculate_completion_forecast(100, 0)
    
    def test_calculate_overall_project_progress(self):
        """Test overall project progress calculation."""
        project_data = {
            "tasks_completed": 75,
            "total_tasks": 100,
            "milestones_completed": 3,
            "total_milestones": 5,
            "budget_used": 50000,
            "total_budget": 100000,
            "time_elapsed": 0.6
        }
        
        result = self.calculator.calculate_overall_project_progress(project_data)
        assert 0 <= result <= 100
    
    def test_calculate_sprint_progress(self):
        """Test sprint progress calculation."""
        sprint_data = {
            "stories_completed": 8,
            "total_stories": 10,
            "story_points_completed": 40,
            "total_story_points": 50,
            "days_elapsed": 7,
            "total_days": 14
        }
        
        result = self.calculator.calculate_sprint_progress(sprint_data)
        assert 0 <= result <= 100
    
    def test_calculate_team_productivity(self):
        """Test team productivity calculation."""
        team_data = {
            "completed_tasks": 50,
            "total_hours_worked": 200,
            "team_size": 5,
            "working_days": 10
        }
        
        result = self.calculator.calculate_team_productivity(team_data)
        assert result >= 0
    
    def test_calculate_individual_productivity(self):
        """Test individual productivity calculation."""
        individual_data = {
            "completed_tasks": 10,
            "hours_worked": 40,
            "working_days": 5
        }
        
        result = self.calculator.calculate_individual_productivity(individual_data)
        assert result >= 0
