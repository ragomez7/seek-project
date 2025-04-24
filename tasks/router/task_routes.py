from fastapi import APIRouter, Depends
from tasks.schemas.tasks_schema import CreateTaskRequest, UpdateTaskStatusRequest, TaskResponse, TaskListResponse
from tasks.services import tasks_service
from typing import List
from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    "/{user_id}",
    summary="Get all tasks for a particular user",
    description="Retrieve a list of all tasks that have not been soft-deleted (i.e., `deleted_at` is `None`).",
    response_model=TaskListResponse
)
async def list_tasks(user_id: str):
    return tasks_service.list_tasks(user_id)


@router.post(
    "/",
    summary="Create a new task",
    description="Create a new task with a title and description. Status is set to TO_DO by default.",
    response_model=TaskResponse
)
async def create_task(task: CreateTaskRequest):
    return tasks_service.create_task(task)


@router.delete(
    "/{task_id}",
    summary="Delete a task (soft delete)",
    description="Marks a task as deleted by setting its `deleted_at` field to the current timestamp. Returns 204 No Content if successful.",
    status_code=204
)
async def delete_task(task_id: str):
    return tasks_service.delete_task(task_id)


@router.put(
    "/{task_id}/status",
    summary="Update task status",
    description="Update the status of a task by providing a valid status value (e.g., TO_DO, IN_PROGRESS, DONE).",
    response_model=TaskResponse
)
async def update_task_status(task_id: str, payload: UpdateTaskStatusRequest):
    return tasks_service.update_task_status(task_id, payload)
