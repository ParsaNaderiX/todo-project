"""Service layer for task-related operations using repositories.

This module provides a thin service that orchestrates calls to the
`TaskRepository`. All validation and database concerns live in the
repository; the service only delegates and translates repository `None`
responses into service-level `TaskNotFoundError` where appropriate.
"""

from typing import List, Optional

from app.repositories import TaskRepository
from app.models.task import Task
from app.exceptions import TaskNotFoundError


class TaskService:
    """Service for task operations backed by `TaskRepository`.

    The service is intentionally thin — it delegates to the repository for
    validation and persistence. It translates repository `None` results into
    `TaskNotFoundError` when callers expect a task to exist.
    """

    def __init__(self, task_repository: TaskRepository) -> None:
        """Initialize the service with a `TaskRepository`.

        Args:
            task_repository: Repository handling task DB operations.
        """
        self.task_repository = task_repository

    def create_task(
        self,
        project_id: int,
        name: str,
        description: str,
        status: str,
        deadline: Optional[str],
    ) -> Task:
        """Create a new task in a project.

        Delegates to `TaskRepository.create()` and returns the created
        `Task` instance. Repository exceptions are allowed to bubble up.
        """
        return self.task_repository.create(project_id, name, description, status, deadline)

    def list_tasks(self, project_id: int) -> List[Task]:
        """Return all tasks for a specific project.

        Delegates to `TaskRepository.get_all_by_project()`.
        """
        return self.task_repository.get_all_by_project(project_id)

    def list_all_tasks(self) -> List[Task]:
        """Return all tasks across all projects, eager-loading projects.

        Delegates to `TaskRepository.get_all()`.
        """
        return self.task_repository.get_all()

    def get_task(self, project_id: int, task_id: int) -> Task:
        """Fetch a task scoped to a specific project.

        Raises `TaskNotFoundError` if the task does not exist or does not
        belong to the given project.
        """
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
        """Update an existing task.

        Verifies the task exists and belongs to the project before delegating
        to `TaskRepository.update()` which performs validation and persistence.
        """
        existing = self.task_repository.get_by_id(project_id, task_id)
        if existing is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")
        # repository.update only requires task_id and new values
        return self.task_repository.update(task_id, new_name, new_description, new_status, new_deadline)

    def edit_task_status(self, project_id: int, task_id: int, new_status: str) -> Task:
        """Update only the status of a task.

        Verifies the task belongs to the project, then delegates to
        `TaskRepository.update_status()`.
        """
        existing = self.task_repository.get_by_id(project_id, task_id)
        if existing is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")
        return self.task_repository.update_status(task_id, new_status)

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task in a project.

        Delegates to `TaskRepository.delete()` which verifies ownership and
        performs the deletion.
        """
        self.task_repository.delete(project_id, task_id)
