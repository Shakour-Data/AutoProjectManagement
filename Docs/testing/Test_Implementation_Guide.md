# Test Implementation Guide

## Overview
This guide provides detailed instructions for implementing comprehensive unit tests for all modules in the AutoProjectManagement system. Each module requires 20+ tests covering functionality, edge cases, error handling, and integration.

## Test Structure Template

### Basic Test File Structure
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Unit Tests for {Module Name}
================================================================================
Module: test_{module_name}
File: test_{module_name}.py
Path: tests/code_tests/01_UnitTests/{category}/test_{module_name}.py

Description:
    Comprehensive unit tests for the {Module Name} module.
    Includes 20+ tests covering functionality, edge cases, error handling, and integration.

Test Categories:
    1. Functionality Tests (5 tests)
    2. Edge Case Tests (5 tests) 
    3. Error Handling Tests (5 tests)
    4. Integration Tests (5 tests)

Author: AutoProjectManagement Team
Version: 1.0.0
================================================================================
"""

import pytest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock

# Add project root to path for imports
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from autoprojectmanagement.{module_path} import {ClassNames}


class Test{MainClass}:
    """Test class for {MainClass} functionality"""
    
    @pytest.fixture
    def test_instance(self):
        """Create test instance with mocked dependencies"""
        return {MainClass}()
    
    # Functionality Tests (5 tests)
    
    def test_basic_functionality_1(self, test_instance):
        """Test basic functionality scenario 1"""
        # Arrange
        # Act
        # Assert
        pass
    
    def test_basic_functionality_2(self, test_instance):
        """Test basic functionality scenario 2"""
        pass
    
    def test_basic_functionality_3(self, test_instance):
        """Test basic functionality scenario 3"""
        pass
    
    def test_basic_functionality_4(self, test_instance):
        """Test basic functionality scenario 4"""
        pass
    
    def test_basic_functionality_5(self, test_instance):
        """Test basic functionality scenario 5"""
        pass
    
    # Edge Case Tests (5 tests)
    
    def test_edge_case_1(self, test_instance):
        """Test edge case scenario 1"""
        pass
    
    def test_edge_case_2(self, test_instance):
        """Test edge case scenario 2"""
        pass
    
    def test_edge_case_3(self, test_instance):
        """Test edge case scenario 3"""
        pass
    
    def test_edge_case_4(self, test_instance):
        """Test edge case scenario 4"""
        pass
    
    def test_edge_case_5(self, test_instance):
        """Test edge case scenario 5"""
        pass
    
    # Error Handling Tests (5 tests)
    
    def test_error_handling_1(self, test_instance):
        """Test error handling scenario 1"""
        pass
    
    def test_error_handling_2(self, test_instance):
        """Test error handling scenario 2"""
        pass
    
    def test_error_handling_3(self, test_instance):
        """Test error handling scenario 3"""
        pass
    
    def test_error_handling_4(self, test_instance):
        """Test error handling scenario 4"""
        pass
    
    def test_error_handling_5(self, test_instance):
        """Test error handling scenario 5"""
        pass
    
    # Integration Tests (5 tests)
    
    def test_integration_1(self, test_instance):
        """Test integration scenario 1"""
        pass
    
    def test_integration_2(self, test_instance):
        """Test integration scenario 2"""
        pass
    
    def test_integration_3(self, test_instance):
        """Test integration scenario 3"""
        pass
    
    def test_integration_4(self, test_instance):
        """Test integration scenario 4"""
        pass
    
    def test_integration_5(self, test_instance):
        """Test integration scenario 5"""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## Test Category Examples

### Functionality Tests (5 examples)
```python
def test_core_business_logic(self, test_instance):
    """Test the core business logic of the module"""
    # Arrange
    input_data = {"key": "value"}
    expected_output = {"processed": "value"}
    
    # Act
    result = test_instance.process_data(input_data)
    
    # Assert
    assert result == expected_output

def test_data_validation(self, test_instance):
    """Test data validation functionality"""
    # Arrange
    valid_data = {"name": "test", "value": 42}
    invalid_data = {"name": "", "value": -1}
    
    # Act & Assert
    assert test_instance.validate_data(valid_data) is True
    assert test_instance.validate_data(invalid_data) is False

def test_state_management(self, test_instance):
    """Test state management functionality"""
    # Arrange
    initial_state = test_instance.get_state()
    
    # Act
    test_instance.update_state("new_state")
    
    # Assert
    assert test_instance.get_state() == "new_state"
    assert test_instance.get_state() != initial_state

def test_configuration_handling(self, test_instance):
    """Test configuration handling"""
    # Arrange
    config = {"setting1": "value1", "setting2": "value2"}
    
    # Act
    test_instance.configure(config)
    
    # Assert
    assert test_instance.get_config() == config

def test_performance_characteristics(self, test_instance):
    """Test basic performance characteristics"""
    # Arrange
    import time
    start_time = time.time()
    
    # Act
    for _ in range(1000):
        test_instance.lightweight_operation()
    
    # Assert
    execution_time = time.time() - start_time
    assert execution_time < 1.0  # Should complete in under 1 second
```

### Edge Case Tests (5 examples)
```python
def test_boundary_values(self, test_instance):
    """Test boundary value conditions"""
    # Test minimum boundary
    assert test_instance.handle_value(0) is not None
    # Test maximum boundary  
    assert test_instance.handle_value(100) is not None
    # Test just beyond boundaries
    with pytest.raises(ValueError):
        test_instance.handle_value(-1)
    with pytest.raises(ValueError):
        test_instance.handle_value(101)

def test_empty_inputs(self, test_instance):
    """Test handling of empty inputs"""
    # Empty string
    assert test_instance.process_input("") is not None
    # Empty list
    assert test_instance.process_input([]) is not None
    # Empty dict
    assert test_instance.process_input({}) is not None
    # None value
    with pytest.raises(ValueError):
        test_instance.process_input(None)

def test_large_datasets(self, test_instance):
    """Test handling of large datasets"""
    # Arrange
    large_data = [{"id": i, "value": f"test_{i}"} for i in range(10000)]
    
    # Act
    result = test_instance.process_batch(large_data)
    
    # Assert
    assert len(result) == len(large_data)
    assert all(item["processed"] for item in result)

def test_concurrent_access(self, test_instance):
    """Test concurrent access scenarios"""
    import threading
    
    results = []
    def worker():
        results.append(test_instance.get_resource())
    
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    assert len(results) == 10
    assert len(set(results)) == 10  # All should be unique

def test_special_characters(self, test_instance):
    """Test handling of special characters"""
    special_cases = [
        "test@example.com",
        "test_with_underscore",
        "test-with-dash", 
        "test with spaces",
        "test_with_unicode_中文",
        "test_with_emoji_😊"
    ]
    
    for case in special_cases:
        result = test_instance.handle_string(case)
        assert result is not None
        assert isinstance(result, str)
```

### Error Handling Tests (5 examples)
```python
def test_invalid_input_handling(self, test_instance):
    """Test handling of invalid inputs"""
    invalid_inputs = [
        None,
        "",
        [],
        {},
        "invalid",
        12345
    ]
    
    for invalid_input in invalid_inputs:
        with pytest.raises((ValueError, TypeError)):
            test_instance.process(invalid_input)

def test_external_dependency_failure(self, test_instance):
    """Test handling of external dependency failures"""
    with patch('external.dependency') as mock_dep:
        mock_dep.side_effect = ConnectionError("Connection failed")
        
        with pytest.raises(ConnectionError):
            test_instance.use_external_dependency()

def test_resource_cleanup_on_error(self, test_instance):
    """Test that resources are cleaned up properly on error"""
    initial_resources = test_instance.get_resource_count()
    
    with pytest.raises(RuntimeError):
        test_instance.operation_that_fails()
    
    # Resources should be cleaned up even after failure
    assert test_instance.get_resource_count() == initial_resources

def test_graceful_degradation(self, test_instance):
    """Test graceful degradation when features are unavailable"""
    with patch('optional.feature', None):  # Feature not available
        result = test_instance.fallback_operation()
        
        assert result is not None
        assert "fallback" in result

def test_error_logging(self, test_instance, caplog):
    """Test that errors are properly logged"""
    with pytest.raises(ValueError):
        test_instance.operation_that_fails()
    
    assert "ERROR" in caplog.text
    assert "operation_that_fails" in caplog.text
```

### Integration Tests (5 examples)
```python
def test_integration_with_database(self, test_instance):
    """Test integration with database layer"""
    with patch('database.connection') as mock_db:
        mock_db.query.return_value = [{"id": 1, "name": "test"}]
        
        result = test_instance.get_from_database(1)
        
        assert result == {"id": 1, "name": "test"}
        mock_db.query.assert_called_once_with("SELECT * FROM table WHERE id = 1")

def test_integration_with_api(self, test_instance):
    """Test integration with external API"""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = test_instance.call_external_api()
        
        assert result == {"data": "test"}
        mock_get.assert_called_once_with("https://api.example.com/data")

def test_integration_with_config_system(self, test_instance):
    """Test integration with configuration system"""
    with patch('config.load') as mock_config:
        mock_config.return_value = {"setting": "value"}
        
        test_instance.initialize()
        config = test_instance.get_config()
        
        assert config == {"setting": "value"}
        mock_config.assert_called_once()

def test_integration_with_logging_system(self, test_instance, caplog):
    """Test integration with logging system"""
    test_instance.log_operation("test message")
    
    assert "test message" in caplog.text
    assert "INFO" in caplog.text

def test_integration_with_cache_system(self, test_instance):
    """Test integration with caching system"""
    with patch('cache.set') as mock_cache_set, \
         patch('cache.get') as mock_cache_get:
        
        mock_cache_get.return_value = None  # Cache miss first time
        mock_cache_set.return_value = True
        
        # First call - should set cache
        result1 = test_instance.get_cached_data("key")
        
        # Second call - should get from cache
        mock_cache_get.return_value = "cached_value"
        result2 = test_instance.get_cached_data("key")
        
        assert result1 == result2
        mock_cache_set.assert_called_once()
        assert mock_cache_get.call_count == 2
```

## Mocking Strategies

### Basic Mocking
```python
@patch('module.Class.method')
def test_with_mock(self, mock_method):
    mock_method.return_value = "mocked_result"
    # test code
```

### Async Mocking
```python
@patch('module.AsyncClass.method', new_callable=AsyncMock)
def test_async_method(self, mock_method):
    mock_method.return_value = "async_result"
    # test code
```

### Complex Mocking
```python
def test_complex_scenario(self):
    with patch('module.Class1.method1') as mock1, \
         patch('module.Class2.method2') as mock2, \
         patch('module.Class3.method3', new_callable=AsyncMock) as mock3:
        
        mock1.return_value = "result1"
        mock2.return_value = "result2" 
        mock3.return_value = "async_result"
        
        # test code
```

## Fixture Patterns

### Basic Fixture
```python
@pytest.fixture
def test_data():
    return {"key": "value", "number": 42}
```

### Factory Fixture
```python
@pytest.fixture
def user_factory():
    def create_user(name="test", age=25):
        return User(name=name, age=age)
    return create_user
```

### Temporary Resources
```python
@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"test content")
        yield f.name
    os.unlink(f.name)
```

## Best Practices

### Test Naming
- Use descriptive test names
- Follow pattern: `test_<what>_<scenario>_<expected>`
- Include docstrings explaining the test scenario

### Test Organization
- Group related tests in classes
- Use fixtures for setup/teardown
- Keep tests independent and isolated

### Assertion Patterns
- Use specific assertions (`assert x == y`)
- Avoid generic `assert True`
- Use context managers for expected exceptions

### Performance Considerations
- Keep tests fast (
