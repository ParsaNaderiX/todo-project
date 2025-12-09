"""Task service wrapper that delegates to the unified TodoService."""

from typing import List, Optional

from app.models.task import Task
from app.repositories import ProjectRepository, TaskRepository
from app.services.todo_service import TodoService


class TaskService:
    """Task-focused façade over the core TodoService."""

    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository) -> None:
        self._service = TodoService(project_repository, task_repository)

    def create_task(
        self,
        project_id: int,
        name: str,
        description: str,
        status: str,
        deadline: Optional[str],
    ) -> Task:
        """Create a new task within a project."""
        return self._service.create_task(project_id, name, description, status, deadline)

    def list_tasks(self, project_id: int) -> List[Task]:
        """Return all tasks for a project."""
        return self._service.list_tasks(project_id)

    def list_all_tasks(self) -> List[Task]:
        """Return all tasks across all projects."""
        return self._service.list_all_tasks()

    def get_task(self, project_id: int, task_id: int) -> Task:
        """Fetch a task scoped to a project."""
        return self._service.get_task(project_id, task_id)

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        new_name: str,
        new_description: str,
        new_status: str,
        new_deadline: Optional[str],
    ) -> Task:
        """Edit full task details."""
        return self._service.edit_task(project_id, task_id, new_name, new_description, new_status, new_deadline)

    def edit_task_status(self, project_id: int, task_id: int, new_status: str) -> Task:
        """Update only the status for a task."""
        return self._service.edit_task_status(project_id, task_id, new_status)

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task from a project."""
        self._service.delete_task(project_id, task_id)
