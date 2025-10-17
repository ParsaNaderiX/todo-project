"""Service layer for the todo application."""
from typing import List

from app.ports import StoragePort
from app.core.models import Project, Task
from app.core.exceptions import (
    ProjectNotFoundError,
    TaskNotFoundError,
)


class TodoService:
    """Service layer implementing the todo application business logic."""

    def __init__(self, storage: StoragePort):
        """Initialize the service with a storage implementation.
        
        Args:
            storage: Implementation of the StoragePort interface
        """
        self.storage = storage

    def create_project(self, name: str, description: str) -> Project:
        """Create a new project.
        
        Args:
            name: Project name
            description: Project description
            
        Returns:
            The created project
            
        Raises:
            ValidationError: If project data is invalid
            DuplicateProjectError: If project name already exists
            ProjectLimitError: If maximum number of projects is reached
        """
        project = Project(name=name, description=description)
        self.storage.add_project(project)
        return project

    def list_projects(self) -> List[Project]:
        """Get all projects.
        
        Returns:
            List of all projects
        """
        return self.storage.list_projects()

    def edit_project(self, index: int, new_name: str, new_description: str) -> Project:
        """Update project details.
        
        Args:
            index: Project index
            new_name: New project name
            new_description: New project description
            
        Returns:
            The updated project
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            ValidationError: If new data is invalid
            DuplicateProjectError: If new name conflicts
        """
        project = self._get_project_or_raise(index)
        project.edit_project(new_name, new_description)
        return project

    def delete_project(self, index: int) -> None:
        """Delete a project.
        
        Args:
            index: Project index
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        self.storage.delete_project(index)

    def create_task(self, project_index: int, name: str, description: str, status: str, deadline: str) -> Task:
        """Create a new task in a project.
        
        Args:
            project_index: Index of the project
            name: Task name
            description: Task description
            status: Initial status ('todo', 'doing', 'done')
            deadline: Due date in YYYY-MM-DD format
            
        Returns:
            The created task
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            ValidationError: If task data is invalid
            DuplicateTaskError: If task name exists in project
            TaskLimitError: If project task limit reached
        """
        project = self._get_project_or_raise(project_index)
        task = Task(name, description, status, deadline, project=project)
        self.storage.add_task(project_index, task)
        return task

    def list_tasks(self, project_index: int) -> List[Task]:
        """Get all tasks in a project.
        
        Args:
            project_index: Index of the project
            
        Returns:
            List of tasks in the project
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        return self.storage.list_tasks(project_index)

    def edit_task(
        self,
        project_index: int,
        task_index: int,
        new_name: str,
        new_description: str,
        new_status: str,
        new_deadline: str
    ) -> Task:
        """Update task details.
        
        Args:
            project_index: Index of the project
            task_index: Index of the task
            new_name: New task name
            new_description: New task description
            new_status: New status ('todo', 'doing', 'done')
            new_deadline: New deadline in YYYY-MM-DD format
            
        Returns:
            The updated task
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            TaskNotFoundError: If task doesn't exist
            ValidationError: If new data is invalid
            DuplicateTaskError: If new name conflicts
        """
        task = self._get_task_or_raise(project_index, task_index)
        task.edit_task(new_name, new_description, new_status, new_deadline)
        return task

    def edit_task_status(self, project_index: int, task_index: int, new_status: str) -> Task:
        """Update just the task status.
        
        Args:
            project_index: Index of the project
            task_index: Index of the task
            new_status: New status ('todo', 'doing', 'done')
            
        Returns:
            The updated task
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            TaskNotFoundError: If task doesn't exist
            ValidationError: If new status is invalid
        """
        task = self._get_task_or_raise(project_index, task_index)
        task.edit_task_status(new_status)
        return task

    def delete_task(self, project_index: int, task_index: int) -> None:
        """Delete a task from a project.
        
        Args:
            project_index: Index of the project
            task_index: Index of the task
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            TaskNotFoundError: If task doesn't exist
        """
        self.storage.delete_task(project_index, task_index)

    def _get_project_or_raise(self, index: int) -> Project:
        """Get a project by index or raise an error.
        
        Args:
            index: Project index
            
        Returns:
            The project
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        project = self.storage.get_project(index)
        if project is None:
            raise ProjectNotFoundError(f"Project with index {index} not found")
        return project

    def _get_task_or_raise(self, project_index: int, task_index: int) -> Task:
        """Get a task by indices or raise an error.
        
        Args:
            project_index: Index of the project
            task_index: Index of the task
            
        Returns:
            The task
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            TaskNotFoundError: If task doesn't exist
        """
        task = self.storage.get_task(project_index, task_index)
        if task is None:
            raise TaskNotFoundError(
                f"Task with index {task_index} not found in project {project_index}"
            )
        return task


