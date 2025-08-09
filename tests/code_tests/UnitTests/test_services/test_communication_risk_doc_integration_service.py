"""
Test suite for CommunicationRiskDocIntegration service
"""
import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock, mock_open

from autoprojectmanagement.main_modules.communication_risk_doc_integration import (
    CommunicationRiskDocIntegration
)


class TestCommunicationRiskDocIntegration:
    """Test cases for CommunicationRiskDocIntegration class"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        import shutil
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def integration_service(self):
        """Create CommunicationRiskDocIntegration instance"""
        return CommunicationRiskDocIntegration()
    
    def test_initialization(self, integration_service):
        """Test service initialization"""
        assert integration_service is not None
    
    def test_load_risk_data_success(self, integration_service):
        """Test loading risk data from JSON files"""
        mock_data = {
            "risks": [
                {
                    "id": "risk1",
                    "description": "Test risk",
                    "probability": 0.5,
                    "impact": "high"
                }
            ]
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
            with patch('os.path.exists', return_value=True):
                result = integration_service.load_risk_data('test.json')
                assert result == mock_data
    
    def test_load_risk_data_file_not_found(self, integration_service):
        """Test handling missing risk data file"""
        with patch('os.path.exists', return_value=False):
            result = integration_service.load_risk_data('nonexistent.json')
            assert result == {}
    
    def test_validate_risk_data(self, integration_service):
        """Test risk data validation"""
        valid_data = {
            "risks": [
                {
                    "id": "risk1",
                    "description": "Test risk",
                    "probability": 0.5,
                    "impact": "high"
                }
            ]
        }
        assert integration_service.validate_risk_data(valid_data) is True
    
    def test_generate_risk_report(self, integration_service):
        """Test generating risk report"""
        report = integration_service.generate_risk_report({
            "risks": [
                {"id": "risk1", "description": "Test risk", "probability": 0.5}
            ]
        })
        assert "risks" in report
    
    def test_export_risk_data(self, integration_service, temp_dir):
        """Test exporting risk data"""
        export_file = os.path.join(temp_dir, 'risk_export.json')
        data = {"risks": [{"id": "risk1", "description": "Test risk"}]}
        
        success = integration_service.export_risk_data(data, export_file)
        assert success is True
        assert os.path.exists(export_file)
