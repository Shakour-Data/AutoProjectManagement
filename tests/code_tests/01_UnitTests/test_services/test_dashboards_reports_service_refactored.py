"""
Test suite for DashboardsReports service
"""
import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock, mock_open

from autoprojectmanagement.main_modules.dashboards_reports import DashboardsReports


class TestDashboardsReports:
    """Test cases for DashboardsReports class"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        import shutil
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def dashboards_service(self):
        """Create DashboardsReports instance"""
        return DashboardsReports()
    
    @pytest.fixture
    def sample_project_data(self):
        """Sample project data for testing"""
        return {
            "projects": [
                {"name": "Project1", "progress": 75, "status": "in_progress"},
                {"name": "Project2", "progress": 50, "status": "in_progress"},
                {"name": "Project3", "progress": 100, "status": "completed"}
            ],
            "metrics": {
                "total_projects": 3,
                "completed_projects": 1,
                "average_progress": 75.0
            }
        }
    
    def test_initialization(self, dashboards_service):
        """Test service initialization"""
        assert dashboards_service is not None
        assert hasattr(dashboards_service, 'generate_dashboard_data')
        assert hasattr(dashboards_service, 'export_dashboard_report')
        assert hasattr(dashboards_service, 'validate_dashboard_data')
    
    def test_generate_dashboard_data(self, dashboards_service, sample_project_data):
        """Test generating dashboard data"""
        dashboard_data = dashboards_service.generate_dashboard_data(sample_project_data)
        
        assert "projects" in dashboard_data
        assert "metrics" in dashboard_data
        assert len(dashboard_data["projects"]) == 3
        assert dashboard_data["metrics"]["total_projects"] == 3
    
    def test_generate_dashboard_data_empty(self, dashboards_service):
        """Test generating dashboard data with empty input"""
        empty_data = {"projects": []}
        dashboard_data = dashboards_service.generate_dashboard_data(empty_data)
        
        assert "projects" in dashboard_data
        assert len(dashboard_data["projects"]) == 0
    
    def test_export_dashboard_report(self, dashboards_service, sample_project_data, temp_dir):
        """Test exporting dashboard report"""
        report_file = os.path.join(temp_dir, 'dashboard_report.html')
        
        success = dashboards_service.export_dashboard_report(sample_project_data, report_file)
        
        assert success is True
        assert os.path.exists(report_file)
        
        # Check if file has content
        with open(report_file, 'r') as f:
            content = f.read()
            assert len(content) > 0
    
    def test_export_dashboard_report_invalid_path(self, dashboards_service, sample_project_data):
        """Test exporting to invalid path"""
        invalid_path = "/invalid/path/report.html"
        
        success = dashboards_service.export_dashboard_report(sample_project_data, invalid_path)
        assert success is False
    
    def test_validate_dashboard_data(self, dashboards_service, sample_project_data):
        """Test dashboard data validation"""
        assert dashboards_service.validate_dashboard_data(sample_project_data) is True
    
    def test_validate_dashboard_data_invalid(self, dashboards_service):
        """Test validation with invalid data"""
        invalid_data = {"invalid_key": "value"}
        assert dashboards_service.validate_dashboard_data(invalid_data) is False
    
    def test_validate_dashboard_data_missing_projects(self, dashboards_service):
        """Test validation with missing projects key"""
        invalid_data = {"metrics": {"total": 0}}
        assert dashboards_service.validate_dashboard_data(invalid_data) is False
    
    def test_generate_progress_chart(self, dashboards_service):
        """Test generating progress chart"""
        chart_data = {
            "labels": ["Jan", "Feb", "Mar", "Apr"],
            "data": [30, 50, 75, 90],
            "colors": ["#FF0000", "#FFFF00", "#00FF00", "#0000FF"]
        }
        
        chart = dashboards_service.generate_progress_chart(chart_data)
        assert chart is not None
        assert "labels" in str(chart)
        assert "data" in str(chart)
    
    def test_generate_progress_chart_empty_data(self, dashboards_service):
        """Test generating progress chart with empty data"""
        chart_data = {
            "labels": [],
            "data": []
        }
        
        chart = dashboards_service.generate_progress_chart(chart_data)
        assert chart is not None
    
    def test_generate_dashboard_data_with_metrics(self, dashboards_service):
        """Test dashboard data generation with comprehensive metrics"""
        data = {
            "projects": [
                {"name": "Project1", "progress": 75, "status": "in_progress", "priority": "high"},
                {"name": "Project2", "progress": 50, "status": "in_progress", "priority": "medium"},
                {"name": "Project3", "progress": 100, "status": "completed", "priority": "low"}
            ],
            "tasks": [
                {"id": 1, "status": "completed", "priority": "urgent"},
                {"id": 2, "status": "in_progress", "priority": "high"}
            ],
            "resources": [
                {"name": "Developer1", "utilization": 85},
                {"name": "Developer2", "utilization": 60}
            ]
        }
        
        dashboard_data = dashboards_service.generate_dashboard_data(data)
        
        assert "projects" in dashboard_data
        assert "tasks" in dashboard_data
        assert "resources" in dashboard_data
        assert len(dashboard_data["projects"]) == 3
    
    def test_export_dashboard_report_with_charts(self, dashboards_service, sample_project_data, temp_dir):
        """Test exporting dashboard report with charts"""
        report_file = os.path.join(temp_dir, 'dashboard_with_charts.html')
        
        # Add chart data to sample data
        sample_project_data["charts"] = {
            "progress_chart": {
                "labels": ["Week1", "Week2", "Week3"],
                "data": [20, 50, 75]
            }
        }
        
        success = dashboards_service.export_dashboard_report(sample_project_data, report_file)
        
        assert success is True
        assert os.path.exists(report_file)
    
    def test_validate_dashboard_data_with_unicode(self, dashboards_service):
        """Test validation with unicode characters"""
        unicode_data = {
            "projects": [
                {"name": "پروژه فارسی", "progress": 75, "status": "در حال انجام"},
                {"name": "Project English", "progress": 100, "status": "completed"}
            ]
        }
        
        assert dashboards_service.validate_dashboard_data(unicode_data) is True
    
    def test_generate_dashboard_data_performance(self, dashboards_service):
        """Test performance with large dataset"""
        large_data = {
            "projects": [
                {"name": f"Project{i}", "progress": i % 100, "status": "in_progress"}
                for i in range(1000)
            ]
        }
        
        dashboard_data = dashboards_service.generate_dashboard_data(large_data)
        
        assert len(dashboard_data["projects"]) == 1000
        assert dashboard_data["projects"][0]["name"] == "Project0"
        assert dashboard_data["projects"][999]["name"] == "Project999"
    
    def test_export_dashboard_report_performance(self, dashboards_service, temp_dir):
        """Test export performance with large dataset"""
        large_data = {
            "projects": [
                {"name": f"Project{i}", "progress": i % 100, "status": "in_progress"}
                for i in range(100)
            ]
        }
        
        report_file = os.path.join(temp_dir, 'large_dashboard.html')
        
        success = dashboards_service.export_dashboard_report(large_data, report_file)
        
        assert success is True
        assert os.path.exists(report_file)
        assert os.path.getsize(report_file) > 0
