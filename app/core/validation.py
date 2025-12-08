"""Validation utilities for the todo application."""
from datetime import datetime, date
from typing import List, Optional

from app.core.exceptions import ValidationError, DuplicateProjectError, DuplicateTaskError
from app.models import Project, Task


def validate_project_name(name: str) -> None:
    """Validate a project name.
    
    Args:
        name: The project name to validate
        
    Raises:
        ValidationError: If name is invalid
    """
    if not name or str(name).strip() == "":
        raise ValidationError("Project name is required.")
    
    name_word_count = len(str(name).strip().split())
    if name_word_count > 30:
        raise ValidationError("Project name must be <= 30 words.")


def validate_project_description(description: str) -> None:
    """Validate a project description.
    
    Args:
        description: The description to validate
        
    Raises:
        ValidationError: If description is invalid
    """
    desc_word_count = len(str(description).strip().split())
    if desc_word_count > 150:
        raise ValidationError("Project description must be <= 150 words.")


def validate_unique_project_name(name: str, existing_projects: List[Project]) -> None:
    """Ensure project name is unique.
    
    Args:
        name: The project name to check
        existing_projects: List of existing projects
        
    Raises:
        DuplicateProjectError: If name already exists
    """
    if any(p.name == name for p in existing_projects):
        raise DuplicateProjectError("Project name must be unique.")


def validate_task_name(name: str) -> None:
    """Validate a task name.
    
    Args:
        name: The task name to validate
        
    Raises:
        ValidationError: If name is invalid
    """
    if not name or str(name).strip() == "":
        raise ValidationError("Task name is required.")
    
    name_word_count = len(str(name).strip().split())
    if name_word_count > 30:
        raise ValidationError("Task name must be <= 30 words.")


def validate_task_description(description: str) -> None:
    """Validate a task description.
    
    Args:
        description: The description to validate
        
    Raises:
        ValidationError: If description is invalid
    """
    desc_word_count = len(str(description).strip().split())
    if desc_word_count > 150:
        raise ValidationError("Task description must be <= 150 words.")


def validate_task_status(status: str) -> str:
    """Validate and normalize task status.
    
    Args:
        status: The status to validate
        
    Returns:
        Normalized status string
        
    Raises:
        ValidationError: If status is invalid
    """
    allowed_status = {"todo", "doing", "done"}
    if status is None or str(status).strip() == "":
        return "todo"
    
    normalized = str(status).strip().lower()
    if normalized not in allowed_status:
        raise ValidationError("Task status must be one of: todo, doing, done.")
    return normalized


def validate_task_deadline(deadline: Optional[str]) -> None:
    """Validate a task deadline.
    
    Args:
        deadline: The deadline to validate (YYYY-MM-DD) or None
        
    Raises:
        ValidationError: If deadline is invalid
    """
    if deadline is not None and str(deadline).strip():
        try:
            parsed = datetime.strptime(str(deadline).strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Task deadline must be in YYYY-MM-DD format.")
        if parsed < date.today():
            raise ValidationError("Task deadline cannot be in the past.")


def validate_unique_task_name(name: str, existing_tasks: List[Task]) -> None:
    """Ensure task name is unique within its project.
    
    Args:
        name: The task name to check
        existing_tasks: List of existing tasks in the project
        
    Raises:
        DuplicateTaskError: If name already exists in project
    """
    if any(t.name == name for t in existing_tasks):
        raise DuplicateTaskError("Task name must be unique within its project.")