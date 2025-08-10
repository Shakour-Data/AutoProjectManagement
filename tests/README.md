# AutoProjectManagement Test Suite

## Overview
This directory contains comprehensive tests for the AutoProjectManagement package, covering all aspects from unit tests to system integration tests, including the new automated test generation workflow.

## Test Structure
```
tests/
├── code_tests/           # Automated and manual code tests
│   ├── 01_UnitTests/    # Unit tests for individual modules (auto-generated supported)
│   ├── 02_IntegrationTests/    # Integration tests for module interactions
│   ├── 03_SystemTests/         # End-to-end system tests
│   ├── 04_PerformanceTests/    # Performance and load tests
│   ├── 05_SecurityTests/       # Security vulnerability tests
│   ├── 06_RegressionTests/     # Regression tests
│   ├── 07_AcceptanceTests/     # User acceptance tests
│   ├── 09_ShellIntegrationTerminalTests/ # Shell and terminal tests
│   └── 10_DocumentationUsabilityTests/  # Documentation accuracy tests
├── api/                  # API endpoint tests
├── automation/           # Automated test generator and related scripts
├── test_docs/            # Test documentation and plans
├── conftest.py           # Pytest configuration and fixtures
├── pytest.ini            # Pytest configuration
├── run_tests.py          # Test runner script
└── README.md             # This file
```

## Running Tests

### Quick Start
```bash
# Run all tests
python tests/run_tests.py

# Run specific test types
pytest tests/code_tests/01_UnitTests/
pytest tests/code_tests/02_IntegrationTests/
pytest tests/code_tests/03_SystemTests/

# Run with coverage
pytest --cov=autoprojectmanagement tests/

# Run with verbose output
pytest -v tests/
```

### Test Categories

#### 1. Unit Tests
- **Location**: `tests/code_tests/01_UnitTests/`
- **Purpose**: Test individual functions and classes, including auto-generated tests
- **Coverage**: All main modules and services
- **Command**: `pytest tests/code_tests/01_UnitTests/`

#### 2. Integration Tests
- **Location**: `tests/code_tests/02_IntegrationTests/`
- **Purpose**: Test module interactions
- **Coverage**: API integrations, data flow, module communication
- **Command**: `pytest tests/code_tests/02_IntegrationTests/`

#### 3. System Tests
- **Location**: `tests/code_tests/03_SystemTests/`
- **Purpose**: End-to-end testing
- **Coverage**: Complete workflows, user scenarios
- **Command**: `pytest tests/code_tests/03_SystemTests/`

#### 4. Performance Tests
- **Location**: `tests/code_tests/04_PerformanceTests/`
- **Purpose**: Performance and load testing
- **Coverage**: Response times, resource usage
- **Command**: `pytest tests/code_tests/04_PerformanceTests/`

#### 5. Security Tests
- **Location**: `tests/code_tests/05_SecurityTests/`
- **Purpose**: Security vulnerability testing
- **Coverage**: Authentication, authorization, data protection
- **Command**: `pytest tests/code_tests/05_SecurityTests/`

#### 6. Regression Tests
- **Location**: `tests/code_tests/06_RegressionTests/`
- **Purpose**: Regression testing to prevent bugs
- **Command**: `pytest tests/code_tests/06_RegressionTests/`

#### 7. Acceptance Tests
- **Location**: `tests/code_tests/07_AcceptanceTests/`
- **Purpose**: User acceptance and business validation
- **Command**: `pytest tests/code_tests/07_AcceptanceTests/`

#### 8. Shell Integration Tests
- **Location**: `tests/code_tests/09_ShellIntegrationTerminalTests/`
- **Purpose**: Shell and terminal integration tests
- **Command**: `pytest tests/code_tests/09_ShellIntegrationTerminalTests/`

#### 9. Documentation Usability Tests
- **Location**: `tests/code_tests/10_DocumentationUsabilityTests/`
- **Purpose**: Documentation accuracy and usability tests
- **Command**: `pytest tests/code_tests/10_DocumentationUsabilityTests/`

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
pytest tests/code_tests/01_UnitTests/test_progress_calculator.py

# Run specific test function
pytest tests/code_tests/01_UnitTests/test_progress_calculator.py::TestProgressCalculator::test_calculate_from_json

# Run with debugging
pytest --pdb tests/code_tests/01_UnitTests/test_progress_calculator.py
```

### 3. Continuous Integration
The test suite is configured for CI/CD with:
- GitHub Actions workflow including automated test generation
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
