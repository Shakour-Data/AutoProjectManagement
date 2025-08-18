"""
Unit tests for input_handler module.

Tests input validation, sanitization, and error handling functionality.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from project_management.modules.main_modules.input_handler import InputHandler


class TestInputHandler:
    """Test cases for InputHandler class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = InputHandler()
    
    def test_validate_string_input_valid(self):
        """Test string input validation with valid inputs."""
        valid_inputs = ["hello", "test123", "valid_input", "UPPERCASE", "lowercase"]
        for input_str in valid_inputs:
            result = self.handler.validate_string_input(input_str)
            assert result == input_str
    
    def test_validate_string_input_empty(self):
        """Test string input validation with empty string."""
        with pytest.raises(ValueError, match="Input cannot be empty"):
            self.handler.validate_string_input("")
    
    def test_validate_string_input_none(self):
        """Test string input validation with None."""
        with pytest.raises(ValueError, match="Input cannot be None"):
            self.handler.validate_string_input(None)
    
    def test_validate_integer_input_valid(self):
        """Test integer input validation with valid inputs."""
        valid_inputs = [1, 100, 0, -1, 999999]
        for input_int in valid_inputs:
            result = self.handler.validate_integer_input(str(input_int))
            assert result == input_int
    
    def test_validate_integer_input_invalid(self):
        """Test integer input validation with invalid inputs."""
        invalid_inputs = ["abc", "12.5", "", "1a2b", "not_a_number"]
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError, match="Invalid integer input"):
                self.handler.validate_integer_input(invalid_input)
    
    def test_validate_float_input_valid(self):
        """Test float input validation with valid inputs."""
        valid_inputs = [1.5, 100.0, 0.0, -1.25, 999.999]
        for input_float in valid_inputs:
            result = self.handler.validate_float_input(str(input_float))
            assert abs(result - input_float) < 0.001
    
    def test_validate_float_input_invalid(self):
        """Test float input validation with invalid inputs."""
        invalid_inputs = ["abc", "", "1a2b", "not_a_float"]
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError, match="Invalid float input"):
                self.handler.validate_float_input(invalid_input)
    
    def test_sanitize_input_removes_special_chars(self):
        """Test input sanitization removes special characters."""
        dirty_input = "Hello@World!#$%^&*()_+"
        expected = "HelloWorld"
        result = self.handler.sanitize_input(dirty_input)
        assert result == expected
    
    def test_sanitize_input_preserves_alphanumeric(self):
        """Test input sanitization preserves alphanumeric characters."""
        clean_input = "ValidInput123"
        result = self.handler.sanitize_input(clean_input)
        assert result == clean_input
    
    def test_validate_range_valid(self):
        """Test range validation with valid inputs."""
        result = self.handler.validate_range(50, 0, 100)
        assert result == 50
    
    def test_validate_range_below_min(self):
        """Test range validation with input below minimum."""
        with pytest.raises(ValueError, match="Input must be between 0 and 100"):
            self.handler.validate_range(-1, 0, 100)
    
    def test_validate_range_above_max(self):
        """Test range validation with input above maximum."""
        with pytest.raises(ValueError, match="Input must be between 0 and 100"):
            self.handler.validate_range(101, 0, 100)
    
    def test_validate_email_valid(self):
        """Test email validation with valid emails."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "email+tag@example.org"
        ]
        for email in valid_emails:
            result = self.handler.validate_email(email)
            assert result == email
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid emails."""
        invalid_emails = [
            "invalid.email",
            "@example.com",
            "test@",
            "test..email@example.com"
        ]
        for email in invalid_emails:
            with pytest.raises(ValueError, match="Invalid email format"):
                self.handler.validate_email(email)
    
    def test_validate_date_format_valid(self):
        """Test date format validation with valid dates."""
        valid_dates = ["2023-12-25", "2024-01-01", "2023-06-15"]
        for date_str in valid_dates:
            result = self.handler.validate_date_format(date_str)
            assert result == date_str
    
    def test_validate_date_format_invalid(self):
        """Test date format validation with invalid dates."""
        invalid_dates = ["25-12-2023", "2023/12/25", "12-25-2023", "invalid"]
        for date_str in invalid_dates:
            with pytest.raises(ValueError, match="Invalid date format"):
                self.handler.validate_date_format(date_str)
    
    def test_validate_list_input_valid(self):
        """Test list input validation with valid lists."""
        valid_lists = [[1, 2, 3], ["a", "b", "c"], [1.5, 2.5, 3.5]]
        for input_list in valid_lists:
            result = self.handler.validate_list_input(input_list)
            assert result == input_list
    
    def test_validate_list_input_empty(self):
        """Test list input validation with empty list."""
        with pytest.raises(ValueError, match="List cannot be empty"):
            self.handler.validate_list_input([])
    
    def test_validate_list_input_none(self):
        """Test list input validation with None."""
        with pytest.raises(ValueError, match="List cannot be None"):
            self.handler.validate_list_input(None)
    
    def test_validate_dict_input_valid(self):
        """Test dictionary input validation with valid dictionaries."""
        valid_dicts = [
            {"key1": "value1", "key2": "value2"},
            {"id": 1, "name": "test"},
            {"config": {"setting": True}}
        ]
        for input_dict in valid_dicts:
            result = self.handler.validate_dict_input(input_dict)
            assert result == input_dict
    
    def test_validate_dict_input_empty(self):
        """Test dictionary input validation with empty dictionary."""
        with pytest.raises(ValueError, match="Dictionary cannot be empty"):
            self.handler.validate_dict_input({})
    
    def test_validate_dict_input_none(self):
        """Test dictionary input validation with None."""
        with pytest.raises(ValueError, match="Dictionary cannot be None"):
            self.handler.validate_dict_input(None)
    
    def test_validate_boolean_input_valid(self):
        """Test boolean input validation with valid inputs."""
        valid_booleans = [True, False, "true", "false", "True", "False", "1", "0"]
        expected = [True, False, True, False, True, False, True, False]
        for input_bool, expected_result in zip(valid_booleans, expected):
            result = self.handler.validate_boolean_input(str(input_bool))
            assert result == expected_result
    
    def test_validate_boolean_input_invalid(self):
        """Test boolean input validation with invalid inputs."""
        invalid_booleans = ["yes", "no", "maybe", "invalid", ""]
        for invalid_input in invalid_booleans:
            with pytest.raises(ValueError, match="Invalid boolean input"):
                self.handler.validate_boolean_input(invalid_input)
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URLs."""
        valid_urls = [
            "https://www.example.com",
            "http://example.com/path",
            "https://subdomain.example.com:8080/path?query=value"
        ]
        for url in valid_urls:
            result = self.handler.validate_url(url)
            assert result == url
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "www.example.com",
            "ftp://example.com",
            "invalid://example.com"
        ]
        for url in invalid_urls:
            with pytest.raises(ValueError, match="Invalid URL format"):
                self.handler.validate_url(url)
