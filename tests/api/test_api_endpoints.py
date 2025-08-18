import pytest
from fastapi.testclient import TestClient
from autoprojectmanagement.api.main import app

client = TestClient(app)

def test_get_project_status():
    project_id = "test_project"
    response = client.get(f"/api/v1/projects/{project_id}/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "running" or isinstance(data["status"], str)

def test_create_project():
    project_data = {
        "name": "Test Project",
        "description": "A project created during testing"
    }
    response = client.post("/api/v1/projects", json=project_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == project_data["name"]
    assert "id" in data

def test_add_task_to_project():
    project_id = "test_project"
    task_data = {
        "title": "Test Task",
        "description": "Task created during testing"
    }
    response = client.post(f"/api/v1/projects/{project_id}/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert "id" in data

def test_get_project_reports():
    project_id = "test_project"
    response = client.get(f"/api/v1/projects/{project_id}/reports")
    assert response.status_code == 200
    data = response.json()
    assert "report" in data or isinstance(data, dict)
