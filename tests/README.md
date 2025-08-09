# AutoProjectManagement Test Suite

## Overview
This directory contains comprehensive tests for the AutoProjectManagement package, covering all aspects from unit tests to system integration tests.

## Test Structure
```
tests/
├── unit_tests/           # Unit tests for individual modules
├── integration_tests/    # Integration tests for module interactions
├── system_tests/         # End-to-end system tests
├── acceptance_tests/     # User acceptance tests
├── regression_tests/     # Regression tests
├── performance_tests/    # Performance and load tests
├── security_tests/       # Security vulnerability tests
├── documentation_tests/  # Documentation accuracy tests
├── shell_integration_tests/ # Shell and terminal tests
├── test_docs/           # Test documentation and plans
├── conftest.py          # Pytest configuration and fixtures
├── pytest.ini          # Pytest configuration
├── run_tests.py        # Test runner script
└── README.md           # This file
```

## Running Tests

### Quick Start
```bash
# Run all tests
python tests/run_tests.py

# Run specific test types
pytest tests/unit_tests/
pytest tests/integration_tests/
pytest tests/system_tests/

# Run with coverage
pytest --cov=autoprojectmanagement tests/

# Run with verbose output
pytest -v tests/
```

### Test Categories

#### 1. Unit Tests
- **Location**: `tests/unit_tests/`
- **Purpose**: Test individual functions and classes
- **Coverage**: All main modules and services
- **Command**: `pytest tests/unit_tests/`

#### 2. Integration Tests
- **Location**: `tests/integration_tests/`
- **Purpose**: Test module interactions
- **Coverage**: API integrations, data flow, module communication
- **Command**: `pytest tests/integration_tests/`

#### 3. System Tests
- **Location**: `tests/system_tests/`
- **Purpose**: End-to-end testing
- **Coverage**: Complete workflows, user scenarios
- **Command**: `pytest tests/system_tests/`

#### 4. Acceptance Tests
- **Location**: `tests/acceptance_tests/`
- **Purpose**: Business requirement validation
- **Coverage**: User stories, business rules
- **Command**: `pytest tests/acceptance_tests/`

#### 5. Performance Tests
- **Location**: `tests/performance_tests/`
- **Purpose**: Performance and load testing
- **Coverage**: Response times, resource usage
- **Command**: `pytest tests/performance_tests/`

#### 6. Security Tests
- **Location**: `tests/security_tests/`
- **Purpose**: Security vulnerability testing
- **Coverage**: Authentication, authorization, data protection
- **Command**: `pytest tests/security_tests/`

## Test Data
- **Location**: `tests/test_data/`
- **Contents**: Sample JSON files, mock responses, test configurations

## Coverage Reports
- **Location**: `tests/results/`
- **Format**: HTML, JSON, XML
- **View**: Open `tests/results/unit_coverage/index.html` in browser

## Development Workflow

### 1. Adding New Tests
1. Create test file in appropriate directory
2. Follow naming convention: `test_*.py`
3. Use provided fixtures from `conftest.py`
4. Add test markers as needed

### 2. Running Tests During Development
```bash
# Run specific test file
pytest tests/unit_tests/test_progress_calculator.py

# Run specific test function
pytest tests/unit_tests/test_progress_calculator.py::TestProgressCalculator::test_calculate_from_json

# Run with debugging
pytest --pdb tests/unit_tests/test_progress_calculator.py
```

### 3. Continuous Integration
The test suite is configured for CI/CD with:
- GitHub Actions workflow
- Coverage reporting
- Multiple Python versions
- Automated test execution

## Test Requirements
Install test dependencies:
```bash
pip install -r requirements-dev.txt
pip install pytest pytest-cov pytest-mock pytest-asyncio responses requests-mock
```

## Test Results
After running tests, check:
- Console output for test results
- Coverage reports in `tests/results/`
- Detailed logs for debugging

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure package is installed in development mode
2. **Missing dependencies**: Install test requirements
3. **Permission errors**: Make test files executable
4. **Path issues**: Run from project root directory

### Debug Mode
```bash
# Enable debug logging
pytest --log-cli-level=DEBUG tests/

# Run with coverage
pytest --cov=autoprojectmanagement --cov-report=html tests/
```

## Support
For test-related issues:
1. Check existing test files for examples
2. Review test documentation in `test_docs/`
3. Ensure all dependencies are installed
4. Run tests in clean environment
