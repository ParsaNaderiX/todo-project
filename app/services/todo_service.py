"""Service layer containing all business logic for projects and tasks.

This service orchestrates validation, business rules (limits, uniqueness),
and repository coordination. Controllers and CLI code should call this
service and work only with domain models (Project, Task), keeping
presentation layers free of business logic.
"""

from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional

from app.config import MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK
from app.core.validation import (
    validate_project_description,
    validate_project_name,
    validate_task_deadline,
    validate_task_description,
    validate_task_name,
    validate_task_status,
)
from app.exceptions import (
    DuplicateProjectError,
    DuplicateTaskError,
    ProjectLimitError,
    ProjectNotFoundError,
    TaskLimitError,
    TaskNotFoundError,
)
from app.models.project import Project
from app.models.task import Task
from app.repositories import ProjectRepository, TaskRepository


class TodoService:
    """Business logic for managing projects and tasks."""

    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository) -> None:
        self.project_repository = project_repository
        self.task_repository = task_repository

    # ------------------------
    # Project operations
    # ------------------------
    def create_project(self, name: str, description: str) -> Project:
        """Create a project after enforcing limits and uniqueness."""
        validate_project_name(name)
        validate_project_description(description)

        if self.project_repository.count() >= MAX_NUMBER_OF_PROJECT:
            raise ProjectLimitError(f"Cannot create more than {MAX_NUMBER_OF_PROJECT} projects.")

        if self.project_repository.exists_by_name(name):
            raise DuplicateProjectError(f"Project '{name}' already exists.")

        return self.project_repository.create(name=name, description=description)

    def list_projects(self) -> List[Project]:
        """Return all projects."""
        return self.project_repository.get_all()

    def get_project(self, project_id: int) -> Project:
        """Fetch a project or raise if missing."""
        project = self.project_repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        return project

    def edit_project(self, project_id: int, new_name: str, new_description: str) -> Project:
        """Update project details with validation and uniqueness checks."""
        validate_project_name(new_name)
        validate_project_description(new_description)
        self.get_project(project_id)

        if self.project_repository.exists_by_name(new_name, exclude_id=project_id):
            raise DuplicateProjectError(f"Project '{new_name}' already exists.")

        return self.project_repository.update(project_id, new_name, new_description)

    def delete_project(self, project_id: int) -> None:
        """Delete a project after verifying it exists."""
        self.get_project(project_id)
        self.project_repository.delete(project_id)

    # ------------------------
    # Task operations
    # ------------------------
    def create_task(
        self,
        project_id: int,
        name: str,
        description: str,
        status: str,
        deadline: Optional[str],
    ) -> Task:
        """Create a task within a project with full validation."""
        # Ensure project exists
        self.get_project(project_id)

        validate_task_name(name)
        validate_task_description(description)
        normalized_status = validate_task_status(status)
        parsed_deadline = self._parse_deadline(deadline)

        if self.task_repository.count_by_project(project_id) >= MAX_NUMBER_OF_TASK:
            raise TaskLimitError(f"Cannot create more than {MAX_NUMBER_OF_TASK} tasks in project {project_id}.")

        if self.task_repository.exists_by_name_in_project(project_id, name):
            raise DuplicateTaskError(f"Task '{name}' already exists in project {project_id}.")

        return self.task_repository.create(project_id, name, description, normalized_status, parsed_deadline)

    def list_tasks(self, project_id: int) -> List[Task]:
        """List all tasks for a project after verifying the project exists."""
        self.get_project(project_id)
        return self.task_repository.get_all_by_project(project_id)

    def list_all_tasks(self) -> List[Task]:
        """List all tasks across all projects."""
        return self.task_repository.get_all()

    def get_task(self, project_id: int, task_id: int) -> Task:
        """Fetch a task scoped to a project or raise if missing."""
        task = self.task_repository.get_by_id(project_id, task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")
        return task

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        new_name: str,
        new_description: str,
        new_status: str,
        new_deadline: Optional[str],
    ) -> Task:
        """Update full task details with validation and uniqueness checks."""
        self.get_task(project_id, task_id)

        validate_task_name(new_name)
        validate_task_description(new_description)
        normalized_status = validate_task_status(new_status)
        parsed_deadline = self._parse_deadline(new_deadline)

        if self.task_repository.exists_by_name_in_project(project_id, new_name, exclude_id=task_id):
            raise DuplicateTaskError(f"Task '{new_name}' already exists in project {project_id}.")

        return self.task_repository.update(task_id, new_name, new_description, normalized_status, parsed_deadline)

    def edit_task_status(self, project_id: int, task_id: int, new_status: str) -> Task:
        """Update only the task status."""
        self.get_task(project_id, task_id)
        normalized_status = validate_task_status(new_status)
        return self.task_repository.update_status(task_id, normalized_status)

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task after verifying ownership."""
        self.get_task(project_id, task_id)
        self.task_repository.delete(project_id, task_id)

    # ------------------------
    # Helpers
    # ------------------------
    def _parse_deadline(self, deadline: Optional[str]) -> Optional[date]:
        """Validate and parse a deadline string into a date."""
        validate_task_deadline(deadline)
        if deadline is None or str(deadline).strip() == "":
            return None
        return datetime.strptime(str(deadline).strip(), "%Y-%m-%d").date()
