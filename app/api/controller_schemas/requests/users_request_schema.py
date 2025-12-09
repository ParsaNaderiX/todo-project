"""Pydantic request schemas for Project and Task APIs.

These models are used for request validation in controller endpoints and
include field validators and OpenAPI examples for Swagger UI.
"""
from __future__ import annotations

from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator


def _word_count(value: str) -> int:
    return len([w for w in value.strip().split() if w])


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., description="Project name (1-30 words)")
    description: Optional[str] = Field(None, description="Optional project description (max 150 words)")

    @field_validator("name")
    @classmethod
    def _validate_name(cls, v: str) -> str:
        count = _word_count(v)
        if count < 1 or count > 30:
            raise ValueError("Project name must be between 1 and 30 words")
        return v

    @field_validator("description")
    @classmethod
    def _validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if _word_count(v) > 150:
            raise ValueError("Description must be at most 150 words")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Marketing Website",
                "description": "Tasks related to launching the marketing website",
            }
        }
    }


class ProjectUpdateRequest(BaseModel):
    new_name: Optional[str] = Field(None, description="New project name (1-30 words)")
    new_description: Optional[str] = Field(None, description="New project description (max 150 words)")

    @field_validator("new_name")
    @classmethod
    def _validate_new_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        count = _word_count(v)
        if count < 1 or count > 30:
            raise ValueError("Project name must be between 1 and 30 words")
        return v

    @field_validator("new_description")
    @classmethod
    def _validate_new_description(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if _word_count(v) > 150:
            raise ValueError("Description must be at most 150 words")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "new_name": "Website Revamp",
                "new_description": "Updated description for the website revamp project",
            }
        }
    }


class TaskCreateRequest(BaseModel):
    name: str = Field(..., description="Task name (1-30 words)")
    description: Optional[str] = Field(None, description="Optional task description (max 150 words)")
    status: Literal["todo", "doing", "done"] = Field("todo", description="Task status")
    deadline: Optional[date] = Field(None, description="Optional deadline in YYYY-MM-DD format")

    @field_validator("name")
    @classmethod
    def _validate_name(cls, v: str) -> str:
        count = _word_count(v)
        if count < 1 or count > 30:
            raise ValueError("Task name must be between 1 and 30 words")
        return v

    @field_validator("description")
    @classmethod
    def _validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if _word_count(v) > 150:
            raise ValueError("Description must be at most 150 words")
        return v

    @field_validator("deadline")
    @classmethod
    def _validate_deadline(cls, v: Optional[date]) -> Optional[date]:
        if v is None:
            return v
        today = date.today()
        if v < today:
            raise ValueError("Deadline cannot be in the past")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Write landing page copy",
                "description": "Create initial copy for the landing page",
                "status": "todo",
                "deadline": str(date.today()),
            }
        }
    }


class TaskUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, description="New task name (1-30 words)")
    description: Optional[str] = Field(None, description="New task description (max 150 words)")
    status: Optional[Literal["todo", "doing", "done"]]
    deadline: Optional[date] = Field(None, description="Optional new deadline in YYYY-MM-DD format")

    @field_validator("name")
    @classmethod
    def _validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        count = _word_count(v)
        if count < 1 or count > 30:
            raise ValueError("Task name must be between 1 and 30 words")
        return v

    @field_validator("description")
    @classmethod
    def _validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if _word_count(v) > 150:
            raise ValueError("Description must be at most 150 words")
        return v

    @field_validator("deadline")
    @classmethod
    def _validate_deadline(cls, v: Optional[date]) -> Optional[date]:
        if v is None:
            return v
        today = date.today()
        if v < today:
            raise ValueError("Deadline cannot be in the past")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Update landing page copy",
                "description": "Refine copy and CTA",
                "status": "doing",
                "deadline": str(date.today()),
            }
        }
    }


class TaskStatusUpdateRequest(BaseModel):
    status: Literal["todo", "doing", "done"] = Field(..., description="New task status")

    model_config = {
        "json_schema_extra": {
            "example": {"status": "done"}
        }
    }
