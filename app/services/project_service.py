"""Project service wrapper that delegates to the unified TodoService."""

from typing import List

from app.models.project import Project
from app.repositories import ProjectRepository, TaskRepository
from app.services.todo_service import TodoService


class ProjectService:
    """Project-focused façade over the core TodoService."""

    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository) -> None:
        self._service = TodoService(project_repository, task_repository)

    def create_project(self, name: str, description: str) -> Project:
        """Create a new project with validation and business rules."""
        return self._service.create_project(name, description)

    def list_projects(self) -> List[Project]:
        """Return all projects."""
        return self._service.list_projects()

    def get_project(self, project_id: int) -> Project:
        """Fetch a project by ID or raise if missing."""
        return self._service.get_project(project_id)

    def edit_project(self, project_id: int, new_name: str, new_description: str) -> Project:
        """Update a project's name and description."""
        return self._service.edit_project(project_id, new_name, new_description)

    def delete_project(self, project_id: int) -> None:
        """Delete a project by ID."""
        self._service.delete_project(project_id)
