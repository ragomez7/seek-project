import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from bson import ObjectId
from unittest.mock import patch, MagicMock
from main import app
from fastapi import HTTPException

client = TestClient(app)

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"
TEST_USER_ID = "68097dc72fe0617b55153166"
TEST_TOKEN = "test_token"

MOCK_USER = {
    "_id": ObjectId(TEST_USER_ID),
    "email": TEST_EMAIL,
    "hashed_password": "hashed_password",
    "created_at": datetime.utcnow()
}

@pytest.mark.asyncio
async def test_register_user_email_exists():
    with patch("auth.router.auth_routes.client.tasksdb.users.find_one") as mock_find_one:
        mock_find_one.return_value = MOCK_USER
        
        response = client.post("/auth/register", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_register_user_invalid_email():
    response = client.post("/auth/register", json={
        "email": "invalid-email",
        "password": TEST_PASSWORD
    })
    
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_login_user_invalid_credentials():
    with patch("auth.router.auth_routes.client.tasksdb.users.find_one") as mock_find_one, \
         patch("auth.router.auth_routes.verify_password") as mock_verify_password:
        
        mock_find_one.return_value = MOCK_USER
        mock_verify_password.return_value = False
        
        response = client.post("/auth/login", json={
            "email": TEST_EMAIL,
            "password": "wrong_password"
        })
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_login_user_invalid_email():
    response = client.post("/auth/login", json={
        "email": "invalid-email",
        "password": TEST_PASSWORD
    })
    
    assert response.status_code == 422 