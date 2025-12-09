"""Pydantic response schemas for Project and Task APIs.

These models are configured with `ConfigDict(from_attributes=True)` so they
can be constructed from SQLAlchemy ORM instances via `Model.model_validate(obj)`
or used with FastAPI's response_model which will honor attribute access.

Example usage:
    task_resp = TaskResponse.model_validate(sqlalchemy_task)
    project_resp = ProjectResponse.model_validate(sqlalchemy_project)

"""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    name: str
    description: Optional[str]
    status: str
    deadline: Optional[date]

    model_config = ConfigDict(from_attributes=True)


class ProjectResponse(BaseModel):
    name: str
    description: Optional[str]
    tasks: List[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ProjectSummary(BaseModel):
    name: str
    description: Optional[str]
    task_count: int

    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    projects: List[ProjectSummary]

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    detail: str
    error_type: str

    model_config = ConfigDict(from_attributes=True)
