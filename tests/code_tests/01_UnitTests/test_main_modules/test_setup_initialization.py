#!/usr/bin/env python3
"""
Unit tests for SetupAutomation class in setup_automation.py
Tests the initialization and basic functionality of the SetupAutomation component.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from io import StringIO

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from project_management.modules.main_modules.setup_automation import SetupAutomation


class TestSetupInitialization(unittest.TestCase):
    """Test cases for SetupAutomation initialization and basic functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.setup_automation = SetupAutomation()

    def tearDown(self):
        """Clean up after each test method."""
        del self.setup_automation

    def test_initialization(self):
        """Test that SetupAutomation initializes correctly."""
        self.assertIsInstance(self.setup_automation, SetupAutomation)
        self.assertIsNone(self.setup_automation.__dict__.get('_SetupAutomation__initialized'))

    def test_get_standard_response_valid_question(self):
        """Test get_standard_response with valid questions."""
        # Test git flow question
        response = self.setup_automation.get_standard_response("What is the git flow used in this project?")
        self.assertEqual(response, "main")
        
        # Test naming conventions question
        response = self.setup_automation.get_standard_response("What naming conventions should be followed?")
        self.assertEqual(response, "Use lowercase with hyphens for branches and snake_case for files.")

    def test_get_standard_response_invalid_question(self):
        """Test get_standard_response with invalid/non-existent questions."""
        response = self.setup_automation.get_standard_response("Invalid question")
        self.assertEqual(response, "No standard response available.")

    def test_get_standard_response_non_string_input(self):
        """Test get_standard_response with non-string input."""
        # Test with None
        response = self.setup_automation.get_standard_response(None)
        self.assertEqual(response, "No standard response available.")
        
        # Test with integer
        response = self.setup_automation.get_standard_response(123)
        self.assertEqual(response, "No standard response available.")
        
        # Test with empty string
        response = self.setup_automation.get_standard_response("")
        self.assertEqual(response, "No standard response available.")

    def test_get_standard_response_empty_string(self):
        """Test get_standard_response with empty string."""
        response = self.setup_automation.get_standard_response("")
        self.assertEqual(response, "No standard response available.")

    def test_get_standard_response_case_sensitivity(self):
        """Test get_standard_response case sensitivity."""
        # Test with different case - should not match
        response = self.setup_automation.get_standard_response("what is the git flow used in this project?")
        self.assertEqual(response, "No standard response available.")

    def test_run_method(self):
        """Test the run method executes without errors."""
        # Capture stdout to verify print statement
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            self.setup_automation.run()
            output = captured_output.getvalue()
            self.assertIn("SetupAutomation mock run method called.", output)

    @patch('builtins.print')
    def test_run_method_prints_correctly(self, mock_print):
        """Test that run method prints the correct message."""
        self.setup_automation.run()
        mock_print.assert_called_once_with("SetupAutomation mock run method called.")

    def test_standard_responses_dictionary_structure(self):
        """Test that standard responses dictionary has expected structure."""
        # Access the internal dictionary for testing
        expected_keys = [
            "What is the git flow used in this project?",
            "What naming conventions should be followed?"
        ]
        
        # Test each expected key exists
        for key in expected_keys:
            response = self.setup_automation.get_standard_response(key)
            self.assertNotEqual(response, "No standard response available.")

    def test_standard_responses_values_are_strings(self):
        """Test that all standard responses return string values."""
        test_questions = [
            "What is the git flow used in this project?",
            "What naming conventions should be followed?",
            "Non-existent question"
        ]
        
        for question in test_questions:
            response = self.setup_automation.get_standard_response(question)
            self.assertIsInstance(response, str)

    def test_multiple_instances_independent(self):
        """Test that multiple instances of SetupAutomation are independent."""
        setup1 = SetupAutomation()
        setup2 = SetupAutomation()
        
        # Both should have same initial state
        self.assertEqual(
            setup1.get_standard_response("What is the git flow used in this project?"),
            setup2.get_standard_response("What is the git flow used in this project?")
        )

    def test_standard_responses_consistency(self):
        """Test that standard responses are consistent across multiple calls."""
        question = "What is the git flow used in this project?"
        response1 = self.setup_automation.get_standard_response(question)
        response2 = self.setup_automation.get_standard_response(question)
        response3 = self.setup_automation.get_standard_response(question)
        
        self.assertEqual(response1, response2)
        self.assertEqual(response2, response3)


if __name__ == '__main__':
    # Run the tests
    unittest.main()
