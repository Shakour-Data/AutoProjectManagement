"""
Pytest configuration and fixtures for AutoProjectManagement tests.
"""
import pytest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch
import responses

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_project_data():
    """Provide sample project data for testing."""
    return {
        "project_name": "Test Project",
        "project_id": "test-123",
        "description": "A test project for unit testing",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "status": "active",
        "tasks": [
            {
                "task_id": "task-1",
                "title": "Setup project",
                "description": "Initial project setup",
                "priority": "high",
                "status": "completed",
                "estimated_hours": 8,
                "actual_hours": 6,
                "assigned_to": "user1"
            },
            {
                "task_id": "task-2",
                "title": "Implement feature",
                "description": "Main feature implementation",
                "priority": "medium",
                "status": "in_progress",
                "estimated_hours": 16,
                "actual_hours": 10,
                "assigned_to": "user2"
            }
        ],
        "resources": [
            {
                "resource_id": "user1",
                "name": "John Doe",
                "role": "developer",
                "availability": 0.8
            },
            {
                "resource_id": "user2",
                "name": "Jane Smith",
                "role": "developer",
                "availability": 0.6
            }
        ]
    }

@pytest.fixture
def mock_github_response():
    """Mock GitHub API responses."""
    return {
        "id": 123456789,
        "name": "test-repo",
        "full_name": "user/test-repo",
        "private": False,
        "owner": {
            "login": "testuser",
            "id": 12345
        },
        "html_url": "https://github.com/user/test-repo",
        "description": "Test repository",
        "fork": False,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
        "pushed_at": "2024-01-03T00:00:00Z"
    }

@pytest.fixture
def mock_config_data():
    """Mock configuration data."""
    return {
        "github": {
            "token": "ghp_test_token",
            "username": "testuser",
            "repository": "test-repo"
        },
        "project": {
            "name": "Test Project",
            "description": "Test project description"
        },
        "notifications": {
            "enabled": True,
            "email": "test@example.com"
        }
    }

@pytest.fixture
def mock_json_files(temp_dir):
    """Create mock JSON files for testing."""
    # Create sample JSON files
    commit_progress = {
        "commits": [
            {
                "hash": "abc123",
                "message": "Initial commit",
                "date": "2024-01-01",
                "files_changed": 5,
                "insertions": 100,
                "deletions": 20
            }
        ]
    }
    
    detailed_wbs = {
        "work_packages": [
            {
                "id": "WP-1",
                "name": "Project Setup",
                "deliverables": ["Project plan", "Team setup"],
                "estimated_hours": 40,
                "actual_hours": 35
            }
        ]
    }
    
    # Write files
    (temp_dir / "commit_progress.json").write_text(json.dumps(commit_progress, indent=2))
    (temp_dir / "detailed_wbs.json").write_text(json.dumps(detailed_wbs, indent=2))
    
    return temp_dir

@pytest.fixture
def mock_requests():
    """Mock requests for API testing."""
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.fixture
def clean_environment():
    """Clean environment for tests."""
    # Store original environment
    original_env = dict(os.environ)
    
    # Clean specific variables
    for key in list(os.environ.keys()):
        if key.startswith('AUTO_PROJECT_') or key.startswith('GITHUB_'):
            del os.environ[key]
    
    yield
    
    # Restore environment
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        "task_id": "TASK-001",
        "title": "Implement user authentication",
        "description": "Create login and registration system",
        "priority": "high",
        "status": "in_progress",
        "estimated_hours": 16,
        "actual_hours": 8,
        "assigned_to": "developer1",
        "due_date": "2024-02-15",
        "dependencies": [],
        "tags": ["backend", "security", "authentication"]
    }

@pytest.fixture
def sample_resource_data():
    """Sample resource data for testing."""
    return {
        "resource_id": "dev-001",
        "name": "Alice Johnson",
        "role": "senior_developer",
        "email": "alice@company.com",
        "availability": 0.8,
        "skills": ["Python", "Django", "PostgreSQL", "Docker"],
        "hourly_rate": 75.0,
        "max_hours_per_week": 40
    }

@pytest.fixture
def sample_risk_data():
    """Sample risk data for testing."""
    return {
        "risk_id": "RISK-001",
        "title": "Third-party API dependency",
        "description": "Project relies heavily on external APIs",
        "probability": "medium",
        "impact": "high",
        "status": "active",
        "mitigation": "Implement caching and fallback mechanisms",
        "owner": "tech_lead"
    }
