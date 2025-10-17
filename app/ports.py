"""Port definitions for the todo application."""
from typing import Protocol, List, Optional

from app.core.models import Project, Task


class StoragePort(Protocol):
    """Interface for storage implementations."""
    
    def add_project(self, project: Project) -> None:
        """Add a new project to storage.
        
        Args:
            project: The project to add
            
        Raises:
            ValidationError: If project data is invalid
            DuplicateProjectError: If project name already exists
            ProjectLimitError: If maximum number of projects is reached
        """
        ...

    def list_projects(self) -> List[Project]:
        """Retrieve all projects.
        
        Returns:
            List of all projects
        """
        ...

    def get_project(self, index: int) -> Optional[Project]:
        """Get a project by its index.
        
        Args:
            index: The project index
            
        Returns:
            The project if found, None otherwise
        """
        ...

    def delete_project(self, index: int) -> None:
        """Delete a project by its index.
        
        Args:
            index: The project index
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        ...

    def add_task(self, project_index: int, task: Task) -> None:
        """Add a task to a project.
        
        Args:
            project_index: Index of the project
            task: The task to add
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            ValidationError: If task data is invalid
            DuplicateTaskError: If task name already exists in project
            TaskLimitError: If maximum number of tasks is reached
        """
        ...

    def list_tasks(self, project_index: int) -> List[Task]:
        """List all tasks in a project.
        
        Args:
            project_index: Index of the project
            
        Returns:
            List of tasks in the project
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        ...

    def get_task(self, project_index: int, task_index: int) -> Optional[Task]:
        """Get a task by its indices.
        
        Args:
            project_index: Index of the project
            task_index: Index of the task
            
        Returns:
            The task if found, None otherwise
        """
        ...

    def delete_task(self, project_index: int, task_index: int) -> None:
        """Delete a task from a project.
        
        Args:
            project_index: Index of the project
            task_index: Index of the task
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            TaskNotFoundError: If task doesn't exist
        """
        ...


