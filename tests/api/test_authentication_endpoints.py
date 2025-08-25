import pytest
from fastapi.testclient import TestClient
from autoprojectmanagement.api.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "SecurePass123!",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 201
    assert response.json()["success"] is True

def test_login_user():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_request_password_reset():
    response = client.post("/auth/request-password-reset", json={
        "email": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_reset_password():
    response = client.post("/auth/reset-password", json={
        "token": "dummy_token",
        "new_password": "NewSecurePass123!"
    })
    assert response.status_code == 400  # This should fail as the token is dummy

def test_verify_email():
    response = client.post("/auth/verify-email", json={
        "token": "dummy_verification_token"
    })
    assert response.status_code == 400  # This should fail as the token is dummy
