# tasks/services/tasks_service.py

from bson import ObjectId
from pymongo import errors
from datetime import datetime
from fastapi import HTTPException

from db import client
from tasks.schemas.tasks_schema import CreateTaskRequest, UpdateTaskStatusRequest
from schemas.task import TaskStatus


def list_tasks(user_id: str):
    print('user_id', user_id)
    cursor = client.tasksdb.tasks.find({
        "deleted_at": None,
        "user_id": ObjectId(user_id)
    })

    return [
        {
            "task_id": str(doc["_id"]),
            "title": doc["title"],
            "description": doc["description"],
            "status": doc["status"],
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
            "deleted_at": doc.get("deleted_at"),
            "user_id": str(doc["user_id"]),
        }
        for doc in cursor
    ]


def create_task(task: CreateTaskRequest):
    try:
        task_data = task.dict()
        now = datetime.utcnow()
        task_data.update({
            "created_at": now,
            "updated_at": now,
            "deleted_at": None,
            "status": TaskStatus.TO_DO,
            "user_id": ObjectId(task_data["user_id"])
        })

        result = client.tasksdb.tasks.insert_one(task_data)

        return {
            "user_id": str(task_data["user_id"]),
            "task_id": str(result.inserted_id),
            "title": task_data["title"],
            "description": task_data["description"],
            "created_at": task_data["created_at"],
            "status": task_data["status"],
        }
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_task(task_id: str):
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    now = datetime.utcnow()
    result = client.tasksdb.tasks.update_one(
        {"_id": oid, "deleted_at": None},
        {"$set": {"deleted_at": now, "updated_at": now}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail="Task not found or already deleted")


def update_task_status(task_id: str, payload: UpdateTaskStatusRequest):
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    result = client.tasksdb.tasks.update_one(
        {"_id": oid},
        {"$set": {"status": payload.status.value, "updated_at": datetime.utcnow()}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    task = client.tasksdb.tasks.find_one({"_id": oid})
    task["task_id"] = str(task["_id"])
    return {
        "task_id": task["task_id"],
        "title": task["title"],
        "description": task["description"],
        "status": task["status"],
        "created_at": task["created_at"],
        "updated_at": task["updated_at"],
    }
