#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: conftest
File: conftest.py
Path: tests/code_tests/01_UnitTests/test_services/conftest.py

Description:
    Conftest module

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
    >>> from tests.code_tests.01_UnitTests.test_services.conftest import {main_class}
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
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def mock_docs_structure():
    """Create a mock documentation structure for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        docs_root = Path(temp_dir) / "Docs"
        docs_root.mkdir()
        
        # Create nested structure
        system_design = docs_root / "SystemDesign"
        system_design.mkdir()
        
        guides = docs_root / "Guides"
        guides.mkdir()
        
        # Create markdown files
        (docs_root / "README.md").write_text("# Project Documentation")
        (system_design / "architecture.md").write_text("# Architecture")
        (system_design / "api-reference.md").write_text("# API Reference")
        (guides / "getting-started.md").write_text("# Getting Started")
        
        yield docs_root


@pytest.fixture
def mock_wiki_repo():
    """Create a mock wiki repository structure"""
    with tempfile.TemporaryDirectory() as temp_dir:
        wiki_dir = Path(temp_dir) / "wiki"
        wiki_dir.mkdir()
        
        # Create wiki files
        (wiki_dir / "Home.md").write_text("# Wiki Home")
        (wiki_dir / "README.md").write_text("# README")
        
        yield wiki_dir


@pytest.fixture
def mock_github_token():
    """Mock GitHub token for testing"""
    return "mock_github_token_12345"


@pytest.fixture
def mock_repo_config():
    """Mock repository configuration"""
    return {
        "owner": "test_user",
        "name": "test_repo",
        "token": "mock_token"
    }
