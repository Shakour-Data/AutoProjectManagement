"""
Comprehensive unit tests for autoprojectmanagement/api/dashboard_endpoints.py
Generated according to AutoProjectManagement testing standards
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from autoprojectmanagement.api.dashboard_endpoints import router

# Create test client
client = TestClient(router)

class TestDashboardEndpoints:
    """Test class for dashboard endpoints"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.mock_project_service = Mock()
        self.mock_progress_report = Mock()
        self.mock_dashboard_reports = Mock()
        
        # Patch the dependencies
        self.project_service_patch = patch('autoprojectmanagement.api.dashboard_endpoints.project_service', self.mock_project_service)
        self.progress_report_patch = patch('autoprojectmanagement.api.dashboard_endpoints.progress_reporter', self.mock_progress_report)
        self.dashboard_report_patch = patch('autoprojectmanagement.api.dashboard_endpoints.dashboard_reporter', self.mock_dashboard_reports)
        
        self.project_service_patch.start()
        self.progress_report_patch.start()
        self.dashboard_report_patch.start()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        self.project_service_patch.stop()
        self.progress_report_patch.stop()
        self.dashboard_report_patch.stop()

    # Functionality Tests (5 tests)
    def test_get_dashboard_overview_success(self):
        """Test successful dashboard overview retrieval"""
        self.mock_project_service.get_status.return_value = {
            "total_tasks": 20,
            "completed_tasks": 15,
            "progress_percentage": 75.0
        }
        
        response = client.get("/dashboard/overview?project_id=test-project")
        
        assert response.status_code == 200
        assert response.json()["project_id"] == "test-project"
        assert response.json()["total_tasks"] == 20

    def test_get_dashboard_metrics_success(self):
        """Test successful dashboard metrics retrieval"""
        self.mock_progress_report.get_metrics_data.return_value = {
            "velocity": 25,
            "throughput": 18
        }
        
        response = client.get("/dashboard/metrics?project_id=test-project")
        
        assert response.status_code == 200
        assert "metrics" in response.json()

    def test_get_dashboard_alerts_success(self):
        """Test successful dashboard alerts retrieval"""
        self.mock_dashboard_reports.get_alerts.return_value = [
            {"id": "alert-001", "type": "risk", "severity": "warning", "message": "Risk detected"}
        ]
        
        response = client.get("/dashboard/alerts?project_id=test-project")
        
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_dashboard_health_success(self):
        """Test successful dashboard health retrieval"""
        self.mock_dashboard_reports.get_health_data.return_value = {
            "overall_health": 85,
            "components": {"code_quality": "healthy"}
        }
        
        response = client.get("/dashboard/health?project_id=test-project")
        
        assert response.status_code == 200
        assert response.json()["overall_health"] == 85

    def test_get_team_performance_success(self):
        """Test successful team performance retrieval"""
        self.mock_dashboard_reports.get_performance_data.return_value = {
            "team_velocity": 25
        }
        
        response = client.get("/dashboard/team-performance?project_id=test-project")
        
        assert response.status_code == 200
        assert response.json()["team_velocity"] == 25

    # Edge Case Tests (5 tests)
    def test_get_dashboard_overview_invalid_project(self):
        """Test dashboard overview retrieval with invalid project ID"""
        self.mock_project_service.get_status.return_value = None
        
        response = client.get("/dashboard/overview?project_id=invalid-project")
        
        assert response.status_code == 404

    def test_get_dashboard_metrics_invalid_project(self):
        """Test dashboard metrics retrieval with invalid project ID"""
        response = client.get("/dashboard/metrics?project_id=invalid-project")
        
        assert response.status_code == 404

    def test_get_dashboard_alerts_no_alerts(self):
        """Test dashboard alerts retrieval with no alerts"""
        self.mock_dashboard_reports.get_alerts.return_value = []
        
        response = client.get("/dashboard/alerts?project_id=test-project")
        
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_get_dashboard_health_invalid_project(self):
        """Test dashboard health retrieval with invalid project ID"""
        response = client.get("/dashboard/health?project_id=invalid-project")
        
        assert response.status_code == 404

    def test_get_team_performance_invalid_project(self):
        """Test team performance retrieval with invalid project ID"""
        response = client.get("/dashboard/team-performance?project_id=invalid-project")
        
        assert response.status_code == 404

    # Error Handling Tests (5 tests)
    def test_get_dashboard_overview_server_error(self):
        """Test dashboard overview retrieval with server error"""
        self.mock_project_service.get_status.side_effect = Exception("Database error")
        
        response = client.get("/dashboard/overview?project_id=test-project")
        
        assert response.status_code == 500

    def test_get_dashboard_metrics_server_error(self):
        """Test dashboard metrics retrieval with server error"""
        self.mock_progress_report.get_metrics_data.side_effect = Exception("Metrics service error")
        
        response = client.get("/dashboard/metrics?project_id=test-project")
        
        assert response.status_code == 500

    def test_get_dashboard_alerts_server_error(self):
        """Test dashboard alerts retrieval with server error"""
        self.mock_dashboard_reports.get_alerts.side_effect = Exception("Alerts service error")
        
        response = client.get("/dashboard/alerts?project_id=test-project")
        
        assert response.status_code == 500

    def test_get_dashboard_health_server_error(self):
        """Test dashboard health retrieval with server error"""
        self.mock_dashboard_reports.get_health_data.side_effect = Exception("Health service error")
        
        response = client.get("/dashboard/health?project_id=test-project")
        
        assert response.status_code == 500

    def test_get_team_performance_server_error(self):
        """Test team performance retrieval with server error"""
        self.mock_dashboard_reports.get_performance_data.side_effect = Exception("Performance service error")
        
        response = client.get("/dashboard/team-performance?project_id=test-project")
        
        assert response.status_code == 500

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
