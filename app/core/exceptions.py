"""Custom exceptions for the todo application."""

class TodoError(Exception):
    """Base exception for all todo application errors."""


class ValidationError(TodoError):
    """Raised when input validation fails."""


class ProjectError(TodoError):
    """Base class for project-related errors."""


class TaskError(TodoError):
    """Base class for task-related errors."""


class ProjectNotFoundError(ProjectError):
    """Raised when a project cannot be found."""


class TaskNotFoundError(TaskError):
    """Raised when a task cannot be found."""


class DuplicateProjectError(ProjectError):
    """Raised when trying to create a project with a name that already exists."""


class DuplicateTaskError(TaskError):
    """Raised when trying to create a task with a name that already exists in the project."""


class ProjectLimitError(ProjectError):
    """Raised when trying to create more projects than allowed."""


class TaskLimitError(TaskError):
    """Raised when trying to create more tasks than allowed in a project."""