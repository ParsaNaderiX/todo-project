"""Service layer for project-related operations using repositories.

This module provides a thin service that orchestrates calls to the
`ProjectRepository`. All validation and database concerns live in the
repository; the service only delegates and translates repository `None`
responses into service-level `ProjectNotFoundError` where appropriate.
"""

from typing import List

from app.repositories import ProjectRepository
from app.models.project import Project
from app.exceptions import ProjectNotFoundError


class ProjectService:
    """Service for project operations backed by `ProjectRepository`.

    The service is intentionally thin — it delegates to the repository for
    validation and persistence. It translates repository `None` results into
    `ProjectNotFoundError` where a not-found semantic is expected by callers.
    """

    def __init__(self, project_repository: ProjectRepository) -> None:
        """Initialize the service with a `ProjectRepository`.

        Args:
            project_repository: Repository handling project DB operations.
        """
        self.project_repository = project_repository

    def create_project(self, name: str, description: str) -> Project:
        """Create a new project.

        Delegates to `ProjectRepository.create()` and returns the created
        `Project` instance. Repository exceptions are allowed to bubble up.
        """
        return self.project_repository.create(name=name, description=description)

    def list_projects(self) -> List[Project]:
        """Return all projects.

        Delegates to `ProjectRepository.get_all()`.
        """
        return self.project_repository.get_all()

    def get_project(self, project_id: int) -> Project:
        """Fetch a project by ID.

        Raises `ProjectNotFoundError` if no project exists with the given ID.
        """
        project = self.project_repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        return project

    def edit_project(self, project_id: int, new_name: str, new_description: str) -> Project:
        """Update a project's name and description.

        Delegates to `ProjectRepository.update()` which performs validation
        and uniqueness checks.
        """
        return self.project_repository.update(project_id, new_name, new_description)

    def delete_project(self, project_id: int) -> None:
        """Delete a project by ID.

        Delegates to `ProjectRepository.delete()`.
        """
        self.project_repository.delete(project_id)
