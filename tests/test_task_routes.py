import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from bson import ObjectId
from unittest.mock import patch, MagicMock
from main import app
from tasks.schemas.tasks_schema import TaskStatus
from fastapi import Depends, HTTPException
from auth.dependencies import get_current_user

# Create a test client
client = TestClient(app)

# Override the authentication dependency
async def override_get_current_user():
    return "test_user_id"

app.dependency_overrides[get_current_user] = override_get_current_user

TEST_USER_ID = str(ObjectId())
TEST_TASK_ID = str(ObjectId())
TEST_TASK = {
    "user_id": TEST_USER_ID,
    "title": "Test Task",
    "description": "Test Description",
    "status": TaskStatus.TO_DO,
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow(),
    "deleted_at": None
}

@pytest.mark.asyncio
async def test_list_tasks_success():
    with patch("tasks.services.tasks_service.list_tasks") as mock_list:
        task_response = {
            "user_id": TEST_USER_ID,
            "task_id": TEST_TASK_ID,
            "title": "Test Task",
            "description": "Test Description",
            "status": TaskStatus.TO_DO,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "deleted_at": None
        }
        mock_list.return_value = [task_response]
        response = client.get(f"/tasks/{TEST_USER_ID}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == task_response["title"]
        assert data[0]["description"] == task_response["description"]
        assert data[0]["status"] == task_response["status"]

@pytest.mark.asyncio
async def test_list_tasks_empty():
    with patch("tasks.services.tasks_service.list_tasks") as mock_list:
        mock_list.return_value = []
        response = client.get(f"/tasks/{TEST_USER_ID}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

@pytest.mark.asyncio
async def test_create_task_success():
    task_data = {
        "user_id": TEST_USER_ID,
        "title": "New Task",
        "description": "New Description"
    }
    with patch("tasks.services.tasks_service.create_task") as mock_create:
        mock_response = {
            "user_id": TEST_USER_ID,
            "task_id": str(ObjectId()),
            "title": task_data["title"],
            "description": task_data["description"],
            "status": TaskStatus.TO_DO,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "deleted_at": None
        }
        mock_create.return_value = mock_response
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == TaskStatus.TO_DO

@pytest.mark.asyncio
async def test_create_task_invalid_data():
    task_data = {
        "user_id": TEST_USER_ID,
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_delete_task_success():
    with patch("tasks.services.tasks_service.delete_task") as mock_delete:
        mock_delete.return_value = None
        response = client.delete(f"/tasks/{TEST_TASK_ID}")
        assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_task_not_found():
    with patch("tasks.services.tasks_service.delete_task") as mock_delete:
        mock_delete.side_effect = HTTPException(status_code=404, detail="Task not found")
        response = client.delete(f"/tasks/{TEST_TASK_ID}")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_task_status_success():
    update_data = {"status": TaskStatus.IN_PROGRESS}
    updated_task = {
        "user_id": TEST_USER_ID,
        "task_id": TEST_TASK_ID,
        "title": "Test Task",
        "description": "Test Description",
        "status": TaskStatus.IN_PROGRESS,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "deleted_at": None
    }
    
    with patch("tasks.services.tasks_service.update_task_status") as mock_update:
        mock_update.return_value = updated_task
        response = client.put(f"/tasks/{TEST_TASK_ID}/status", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == TaskStatus.IN_PROGRESS

@pytest.mark.asyncio
async def test_update_task_status_invalid_status():
    update_data = {"status": "INVALID_STATUS"}
    response = client.put(f"/tasks/{TEST_TASK_ID}/status", json=update_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_task_status_not_found():
    update_data = {"status": TaskStatus.IN_PROGRESS}
    with patch("tasks.services.tasks_service.update_task_status") as mock_update:
        mock_update.side_effect = HTTPException(status_code=404, detail="Task not found")
        response = client.put(f"/tasks/{TEST_TASK_ID}/status", json=update_data)
        assert response.status_code == 404 