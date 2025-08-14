#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: test_wiki_services_runner
File: test_wiki_services_runner.py
Path: tests/code_tests/01_UnitTests/test_services/test_wiki_services_runner.py

Description:
    Test Wiki Services Runner module

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2025-08-14
    Python Version: 3.8+
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-01
    Last Modified: 2025-08-14
    Modified By: AutoProjectManagement Team

Dependencies:
    - Python 3.8+
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team

Usage:
    This module is part of the AutoProjectManagement package.
    Import and use as needed within the package ecosystem.

Example:
    >>> from tests.code_tests.01_UnitTests.test_services.test_wiki_services_runner import {main_class}
    >>> instance = {main_class}()
    >>> instance.run()

Notes:
    - This file follows the AutoProjectManagement coding standards
    - All changes should be documented in the changelog below
    - Ensure compatibility with Python 3.8+

Changelog:
    1.0.0 (2024-01-01): Initial release
    1.0.1 (2025-08-14): {change_description}

TODO:
    - [ ] Add comprehensive error handling
    - [ ] Implement logging throughout
    - [ ] Add unit tests
    - [ ] Update documentation

================================================================================
"""


import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def run_wiki_tests():
    """Run all wiki services tests"""
    test_files = [
        "test_wiki_git_operations.py",
        "test_wiki_page_mapper.py", 
        "test_wiki_sync_service.py"
    ]
    
    test_dir = Path(__file__).parent
    
    results = []
    for test_file in test_files:
        test_path = test_dir / test_file
        if test_path.exists():
            print(f"Running {test_file}...")
            result = pytest.main([str(test_path), "-v"])
            results.append((test_file, result))
    
    return results

def run_all_wiki_tests_with_coverage():
    """Run all wiki tests with coverage report"""
    test_dir = Path(__file__).parent
    
    # Run tests with coverage
    args = [
        str(test_dir),
        "-v",
        "--cov=autoprojectmanagement.services.wiki_git_operations",
        "--cov=autoprojectmanagement.services.wiki_page_mapper", 
        "--cov=autoprojectmanagement.services.wiki_sync_service",
        "--cov-report=html",
        "--cov-report=term-missing"
    ]
    
    return pytest.main(args)

if __name__ == "__main__":
    print("Wiki Services Test Runner")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--coverage":
        result = run_all_wiki_tests_with_coverage()
    else:
        results = run_wiki_tests()
        
        print("\n" + "=" * 50)
        print("Test Results Summary:")
        for test_file, result in results:
            status = "PASSED" if result == 0 else "FAILED"
            print(f"{test_file}: {status}")
    
    print("\nTo run with coverage: python test_wiki_services_runner.py --coverage")
