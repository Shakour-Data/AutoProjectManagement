"""
Test suite for DashboardsReports service
"""
import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock, mock_open

from autoprojectmanagement.main_modules.dashboards_reports import (
    DashboardsReports
)


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
    
    def test_initialization(self, dashboards_service):
        """Test service initialization"""
        assert dashboards_service is not None
    
    def test_generate_dashboard_data(self, dashboards_service):
        """Test generating dashboard data"""
        data = {
            "projects": [
                {"name": "Project1", "progress": 75},
                {"name": "Project2", "progress": 50}
            ]
        }
        
        dashboard_data = dashboards_service.generate_dashboard_data(data)
        assert "projects" in dashboard_data
    
    def test_export_dashboard_report(self, dashboards_service, temp_dir):
        """Test exporting dashboard report"""
        report_file = os.path.join(temp_dir, 'dashboard_report.html')
        data = {"projects": [{"name": "Project1", "progress": 75}]}
        
        success = dashboards_service.export_dashboard_report(data, report_file)
        assert success is True
    
    def test_validate_dashboard_data(self, dashboards_service):
        """Test dashboard data validation"""
        valid_data = {
            "projects": [
                {"name": "Project1", "progress": 75}
            ]
        }
        assert dashboards_service.validate_dashboard_data(valid_data) is True
    
    def test_generate_progress_chart(self, dashboards_service):
        """Test generating progress chart"""
        chart_data = {
            "labels": ["Jan", "Feb", "Mar"],
            "data": [30, 50, 75]
        }
        
        chart = dashboards_service.generate_progress_chart(chart_data)
        assert chart is not None
