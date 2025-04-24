from pydantic import BaseModel, Field, RootModel
from datetime import datetime
from enum import Enum
from typing import Optional, List


class TaskStatus(str, Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class CreateTaskRequest(BaseModel):
    user_id: str = Field(..., example="134234232")
    title: str = Field(..., example="Buy groceries")
    description: str = Field(..., example="Milk, eggs, and bread")


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus = Field(..., example="IN_PROGRESS")


class TaskResponse(BaseModel):
    user_id: str = Field(..., example="661f98f1a2b345f1f4e2d0d1")
    task_id: str = Field(..., example="661f98f1a2b345f1f4e2d0d1")
    title: str = Field(..., example="Buy groceries")
    description: str = Field(..., example="Milk, eggs, and bread")
    status: TaskStatus = Field(..., example="TO_DO")
    created_at: Optional[datetime] = Field(None, example="2024-04-23T14:00:00Z")
    updated_at: Optional[datetime] = Field(None, example="2024-04-23T14:10:00Z")
    deleted_at: Optional[datetime] = Field(None, example="2024-04-23T15:00:00Z")


class TaskListResponse(RootModel[List[TaskResponse]]):
    pass

