"""
Test configuration for wiki services unit tests
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
