"""Service layer exceptions for business logic failures.

These exceptions represent errors that occur at the business logic layer,
such as validation failures, business rule violations, and entity-specific errors.
"""

from app.exceptions.base import TodoError


class ValidationError(TodoError):
    """Raised when input validation fails.
    
    This exception should be raised when:
    - Input data does not meet format requirements
    - Required fields are missing
    - Data types are incorrect
    - Values are out of acceptable ranges
    
    Example:
        raise ValidationError("Project name must be between 1 and 30 words")
    """

    pass


class ProjectError(TodoError):
    """Base class for project-related errors.
    
    All project-specific exceptions inherit from this class, allowing
    catching all project-related errors with a single exception type.
    
    Example:
        try:
            # Project operation
        except ProjectError as e:
            # Handle any project-related error
    """

    pass


class ProjectNotFoundError(ProjectError):
    """Raised when a project cannot be found.
    
    This exception should be raised when:
    - A project with the specified name or ID does not exist
    - Attempting to access a project that has been deleted
    
    Example:
        raise ProjectNotFoundError(f"Project '{project_name}' not found")
    """

    pass


class DuplicateProjectError(ProjectError):
    """Raised when trying to create a project with a name that already exists.
    
    This exception should be raised when:
    - Attempting to create a project with a name that is already in use
    - Project name uniqueness constraint is violated
    
    Example:
        raise DuplicateProjectError(f"Project '{project_name}' already exists")
    """

    pass


class ProjectLimitError(ProjectError):
    """Raised when trying to create more projects than allowed.
    
    This exception should be raised when:
    - The maximum number of projects (MAX_NUMBER_OF_PROJECT) has been reached
    - Attempting to create a project would exceed the configured limit
    
    Example:
        raise ProjectLimitError(f"Cannot create more than {max_projects} projects")
    """

    pass


class TaskError(TodoError):
    """Base class for task-related errors.
    
    All task-specific exceptions inherit from this class, allowing
    catching all task-related errors with a single exception type.
    
    Example:
        try:
            # Task operation
        except TaskError as e:
            # Handle any task-related error
    """

    pass


class TaskNotFoundError(TaskError):
    """Raised when a task cannot be found.
    
    This exception should be raised when:
    - A task with the specified name or ID does not exist
    - Attempting to access a task that has been deleted
    - Task does not belong to the specified project
    
    Example:
        raise TaskNotFoundError(f"Task '{task_name}' not found in project '{project_name}'")
    """

    pass


class DuplicateTaskError(TaskError):
    """Raised when trying to create a task with a name that already exists in the project.
    
    This exception should be raised when:
    - Attempting to create a task with a name that already exists in the same project
    - Task name uniqueness constraint within a project is violated
    
    Example:
        raise DuplicateTaskError(f"Task '{task_name}' already exists in project '{project_name}'")
    """

    pass


class TaskLimitError(TaskError):
    """Raised when trying to create more tasks than allowed in a project.
    
    This exception should be raised when:
    - The maximum number of tasks per project (MAX_NUMBER_OF_TASK) has been reached
    - Attempting to create a task would exceed the configured limit for the project
    
    Example:
        raise TaskLimitError(f"Cannot create more than {max_tasks} tasks in project '{project_name}'")
    """

    pass

