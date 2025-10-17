"""In-memory storage implementation for the todo application."""
from typing import List, Optional

from app.config import MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK
from app.core.models import Project, Task
from app.core.exceptions import (
    ProjectNotFoundError,
    TaskNotFoundError,
    ProjectLimitError,
    TaskLimitError,
)
from app.core.validation import (
    validate_project_name,
    validate_project_description,
    validate_unique_project_name,
    validate_task_name,
    validate_task_description,
    validate_task_status,
    validate_task_deadline,
    validate_unique_task_name,
)


class InMemoryStorage:
    """Simple in-memory storage implementation."""

    def __init__(self):
        """Initialize empty storage."""
        self.projects: List[Project] = []

    def add_project(self, project: Project) -> None:
        """Add a new project to storage.
        
        Args:
            project: The project to add
            
        Raises:
            ValidationError: If project data is invalid
            DuplicateProjectError: If project name exists
            ProjectLimitError: If project limit reached
        """
        validate_project_name(project.name)
        validate_project_description(project.description)
        validate_unique_project_name(project.name, self.projects)
        
        if len(self.projects) >= MAX_NUMBER_OF_PROJECT:
            raise ProjectLimitError(
                f"Cannot add more projects. Maximum allowed is {MAX_NUMBER_OF_PROJECT}."
            )
        
        self.projects.append(project)

    def list_projects(self) -> List[Project]:
        """Get all projects.
        
        Returns:
            List of all projects
        """
        return list(self.projects)

    def get_project(self, index: int) -> Optional[Project]:
        """Get a project by index.
        
        Args:
            index: Project index
            
        Returns:
            The project if found, None otherwise
        """
        if 0 <= index < len(self.projects):
            return self.projects[index]
        return None

    def delete_project(self, index: int) -> None:
        """Delete a project.
        
        Args:
            index: Project index
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        project = self.get_project(index)
        if project is None:
            raise ProjectNotFoundError(f"Project with index {index} not found")
        
        project.tasks.clear()
        del self.projects[index]

    def add_task(self, project_index: int, task: Task) -> None:
        """Add a task to a project.
        
        Args:
            project_index: Project index
            task: The task to add
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            ValidationError: If task data is invalid
            DuplicateTaskError: If task name exists
            TaskLimitError: If task limit reached
        """
        project = self.get_project(project_index)
        if project is None:
            raise ProjectNotFoundError(f"Project with index {project_index} not found")
        
        validate_task_name(task.name)
        validate_task_description(task.description)
        task.status = validate_task_status(task.status)
        validate_task_deadline(task.deadline)
        validate_unique_task_name(task.name, project.tasks)
        
        if len(project.tasks) >= MAX_NUMBER_OF_TASK:
            raise TaskLimitError(
                f"Cannot add more tasks to this project. Maximum allowed is {MAX_NUMBER_OF_TASK}."
            )
        
        project.tasks.append(task)

    def list_tasks(self, project_index: int) -> List[Task]:
        """List all tasks in a project.
        
        Args:
            project_index: Project index
            
        Returns:
            List of tasks
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        project = self.get_project(project_index)
        if project is None:
            raise ProjectNotFoundError(f"Project with index {project_index} not found")
        
        return list(project.tasks)

    def get_task(self, project_index: int, task_index: int) -> Optional[Task]:
        """Get a task by indices.
        
        Args:
            project_index: Project index
            task_index: Task index
            
        Returns:
            The task if found, None otherwise
        """
        project = self.get_project(project_index)
        if project is None:
            return None
        
        if 0 <= task_index < len(project.tasks):
            return project.tasks[task_index]
        return None

    def delete_task(self, project_index: int, task_index: int) -> None:
        """Delete a task from a project.
        
        Args:
            project_index: Project index
            task_index: Task index
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            TaskNotFoundError: If task doesn't exist
        """
        project = self.get_project(project_index)
        task = self.get_task(project_index, task_index)
        
        if project is None:
            raise ProjectNotFoundError(f"Project with index {project_index} not found")
        if task is None:
            raise TaskNotFoundError(
                f"Task with index {task_index} not found in project {project_index}"
            )
        
        del project.tasks[task_index]


