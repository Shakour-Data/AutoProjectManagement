"""
Comprehensive tests for autoprojectmanagement/main_modules/quality_management.py
Implemented according to project testing standards with 20 tests in 4 categories
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'src'))

from autoprojectmanagement.main_modules.quality_commit_management import quality_management


class TestBaseManagement:
    """Test class for BaseManagement functionality"""
    
    def test_basemanagement_initialization_valid(self):
        """Test BaseManagement initialization with valid parameters"""
        input_paths = {'test': 'test.json'}
        output_path = 'output.json'
        
        manager = quality_management.BaseManagement(input_paths, output_path)
        
        assert manager.input_paths == input_paths
        assert manager.output_path == output_path
        assert manager.inputs == {}
        assert manager.output == {}
    
    def test_basemanagement_initialization_invalid(self):
        """Test BaseManagement initialization with invalid parameters"""
        with pytest.raises(ValueError, match="input_paths cannot be empty"):
            quality_management.BaseManagement({}, 'output.json')
        
        with pytest.raises(ValueError, match="output_path cannot be empty"):
            quality_management.BaseManagement({'test': 'test.json'}, '')
    
    def test_load_json_existing_file(self):
        """Test load_json with existing valid JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            test_data = {'key': 'value', 'number': 42}
            json.dump(test_data, tmp)
            tmp_path = tmp.name
        
        try:
            manager = quality_management.BaseManagement({'test': tmp_path}, 'output.json')
            result = manager.load_json(tmp_path)
            
            assert result == test_data
        finally:
            os.unlink(tmp_path)
    
    def test_load_json_nonexistent_file(self):
        """Test load_json with non-existent file"""
        manager = quality_management.BaseManagement({'test': 'nonexistent.json'}, 'output.json')
        result = manager.load_json('nonexistent.json')
        
        assert result is None
    
    def test_load_json_invalid_json(self):
        """Test load_json with invalid JSON content"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp.write('invalid json content')
            tmp_path = tmp.name
        
        try:
            manager = quality_management.BaseManagement({'test': tmp_path}, 'output.json')
            
            with pytest.raises(json.JSONDecodeError):
                manager.load_json(tmp_path)
        finally:
            os.unlink(tmp_path)
    
    def test_save_json_valid(self):
        """Test save_json with valid data"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, 'output.json')
            test_data = {'key': 'value', 'nested': {'data': [1, 2, 3]}}
            
            manager = quality_management.BaseManagement({'test': 'input.json'}, output_path)
            manager.save_json(test_data, output_path)
            
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data == test_data
    
    def test_load_inputs_success(self):
        """Test load_inputs with valid input files"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp1:
            data1 = {'data1': 'value1'}
            json.dump(data1, tmp1)
            tmp1_path = tmp1.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp2:
            data2 = {'data2': 'value2'}
            json.dump(data2, tmp2)
            tmp2_path = tmp2.name
        
        try:
            input_paths = {'input1': tmp1_path, 'input2': tmp2_path}
            manager = quality_management.BaseManagement(input_paths, 'output.json')
            manager.load_inputs()
            
            assert manager.inputs['input1'] == data1
            assert manager.inputs['input2'] == data2
        finally:
            os.unlink(tmp1_path)
            os.unlink(tmp2_path)
    
    def test_validate_inputs_success(self):
        """Test validate_inputs with all inputs loaded"""
        manager = quality_management.BaseManagement(
            {'input1': 'file1.json', 'input2': 'file2.json'}, 
            'output.json'
        )
        manager.inputs = {'input1': {}, 'input2': {}}
        
        assert manager.validate_inputs() is True
    
    def test_validate_inputs_failure(self):
        """Test validate_inputs with missing inputs"""
        manager = quality_management.BaseManagement(
            {'input1': 'file1.json', 'input2': 'file2.json'}, 
            'output.json'
        )
        manager.inputs = {'input1': {}}  # Missing input2
        
        assert manager.validate_inputs() is False


class TestQualityManagement:
    """Test class for QualityManagement functionality"""
    
    def test_qualitymanagement_initialization_default(self):
        """Test QualityManagement initialization with default paths"""
        manager = quality_management.QualityManagement()
        
        expected_inputs = {
            'detailed_wbs': 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json',
            'quality_standards': 'JSonDataBase/Inputs/UserInputs/quality_standards.json'
        }
        
        assert manager.input_paths == expected_inputs
        assert manager.output_path == 'JSonDataBase/OutPuts/quality_management.json'
    
    def test_qualitymanagement_initialization_custom(self):
        """Test QualityManagement initialization with custom paths"""
        custom_wbs = 'custom_wbs.json'
        custom_standards = 'custom_standards.json'
        custom_output = 'custom_output.json'
        
        manager = quality_management.QualityManagement(
            custom_wbs, custom_standards, custom_output
        )
        
        expected_inputs = {
            'detailed_wbs': custom_wbs,
            'quality_standards': custom_standards
        }
        
        assert manager.input_paths == expected_inputs
        assert manager.output_path == custom_output
    
    def test_calculate_quality_score_comprehensive(self):
        """Test calculate_quality_score with comprehensive metrics"""
        task = {
            'code_coverage': 85,
            'documentation_coverage': 90,
            'pep8_compliance': 95
        }
        
        standards = {
            'code_coverage': {'target': 80, 'weight': 1.0},
            'documentation_coverage': {'target': 85, 'weight': 0.8},
            'pep8_compliance': {'target': 90, 'weight': 0.7}
        }
        
        manager = quality_management.QualityManagement()
        result = manager.calculate_quality_score(task, standards)
        
        assert 'score' in result
        assert 'level' in result
        assert 'metrics' in result
        assert 'recommendations' in result
        
        # Verify score calculation
        expected_score = (
            (min(85/80*100, 100) * 1.0 + 
             min(90/85*100, 100) * 0.8 + 
             min(95/90*100, 100) * 0.7) / 
            (100 * 1.0 + 100 * 0.8 + 100 * 0.7) * 100
        )
        
        assert abs(result['score'] - expected_score) < 0.1
    
    def test_calculate_quality_score_edge_cases(self):
        """Test calculate_quality_score with edge case values"""
        manager = quality_management.QualityManagement()
        
        # Test with 0% values
        task_zero = {'code_coverage': 0, 'documentation_coverage': 0, 'pep8_compliance': 0}
        standards = {
            'code_coverage': {'target': 80, 'weight': 1.0},
            'documentation_coverage': {'target': 85, 'weight': 1.0},
            'pep8_compliance': {'target': 90, 'weight': 1.0}
        }
        
        result_zero = manager.calculate_quality_score(task_zero, standards)
        assert result_zero['score'] == 0.0
        assert result_zero['level'] == 'POOR'
        
        # Test with 100% values
        task_perfect = {'code_coverage': 100, 'documentation_coverage': 100, 'pep8_compliance': 100}
        result_perfect = manager.calculate_quality_score(task_perfect, standards)
        assert result_perfect['score'] == 100.0
        assert result_perfect['level'] == 'HIGH'
    
    def test_generate_recommendations_various_levels(self):
        """Test _generate_recommendations with various quality levels"""
        manager = quality_management.QualityManagement()
        
        # Test with poor quality metrics
        poor_metrics = {
            'code_coverage': {'actual': 40, 'target': 80, 'score': 50, 'weight': 1.0},
            'documentation_coverage': {'actual': 30, 'target': 85, 'score': 35, 'weight': 1.0}
        }
        
        recommendations_poor = manager._generate_recommendations(poor_metrics, 'POOR')
        assert len(recommendations_poor) > 0  # Expect recommendations for poor quality
        
        # Test with high quality metrics
        high_metrics = {
            'code_coverage': {'actual': 90, 'target': 80, 'score': 100, 'weight': 1.0},
            'documentation_coverage': {'actual': 85, 'target': 85, 'score': 100, 'weight': 1.0}
        }
        
        recommendations_high = manager._generate_recommendations(high_metrics, 'HIGH')
        assert len(recommendations_high) == 0  # No recommendations expected for high quality
    
    def test_analyze_with_valid_data(self):
        """Test analyze method with valid WBS and quality standards"""
        manager = quality_management.QualityManagement()
        manager.inputs = {
            'detailed_wbs': {
                "project_name": "Test Project",
                "tasks": {
                    "task_001": {
                        "code_coverage": 85,
                        "documentation_coverage": 90,
                        "pep8_compliance": 95
                    }
                }
            },
            'quality_standards': {
                'code_coverage': {'target': 80, 'weight': 1.0},
                'documentation_coverage': {'target': 85, 'weight': 0.8},
                'pep8_compliance': {'target': 90, 'weight': 0.7}
            }
        }
        
        manager.analyze()
        
        assert 'summary' in manager.output
        assert 'task_quality' in manager.output
        assert 'recommendations' in manager.output
    
    def test_analyze_with_empty_wbs(self):
        """Test analyze method with empty WBS data"""
        manager = quality_management.QualityManagement()
        manager.inputs = {
            'detailed_wbs': {},
            'quality_standards': {}
        }
        
        manager.analyze()
        
        assert 'error' in manager.output
        assert manager.output['error'] == 'No WBS data available'
    
    def test_analyze_with_missing_quality_standards(self):
        """Test analyze method with missing quality standards"""
        manager = quality_management.QualityManagement()
        manager.inputs = {
            'detailed_wbs': {
                "project_name": "Test Project",
                "tasks": {
                    "task_001": {
                        "code_coverage": 85,
                        "documentation_coverage": 90,
                        "pep8_compliance": 95
                    }
                }
            },
            'quality_standards': {}
        }
        
        manager.analyze()
        
        assert 'quality_standards' in manager.output
        assert manager.output['quality_standards'] is not None  # Should use defaults
    
    def test_run_integration(self):
        """Test the complete run method integration"""
        manager = quality_management.QualityManagement()
        manager.inputs = {
            'detailed_wbs': {
                "project_name": "Test Project",
                "tasks": {
                    "task_001": {
                        "code_coverage": 85,
                        "documentation_coverage": 90,
                        "pep8_compliance": 95
                    }
                }
            },
            'quality_standards': {
                'code_coverage': {'target': 80, 'weight': 1.0},
                'documentation_coverage': {'target': 85, 'weight': 0.8},
                'pep8_compliance': {'target': 90, 'weight': 0.7}
            }
        }
        
        manager.run()
        
        assert 'summary' in manager.output
        assert 'task_quality' in manager.output
        assert 'recommendations' in manager.output
        
