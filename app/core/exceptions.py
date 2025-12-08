"""Custom exceptions for the todo application.

DEPRECATED: This module is maintained for backwards compatibility.
New code should import from app.exceptions instead.

This module re-exports all exceptions from app.exceptions to maintain
backwards compatibility with existing code that imports from app.core.exceptions.
"""

# Import all exceptions from the new location
from app.exceptions import (
    # Base exceptions
    TodoError,
    # Repository exceptions
    RepositoryError,
    DatabaseConnectionError,
    DatabaseOperationError,
    RecordNotFoundError,
    # Service exceptions
    ValidationError,
    ProjectError,
    ProjectNotFoundError,
    DuplicateProjectError,
    ProjectLimitError,
    TaskError,
    TaskNotFoundError,
    DuplicateTaskError,
    TaskLimitError,
)

# Re-export for backwards compatibility
__all__ = [
    "TodoError",
    "ValidationError",
    "ProjectError",
    "ProjectNotFoundError",
    "DuplicateProjectError",
    "ProjectLimitError",
    "TaskError",
    "TaskNotFoundError",
    "DuplicateTaskError",
    "TaskLimitError",
    # New repository exceptions (also available for backwards compatibility)
    "RepositoryError",
    "DatabaseConnectionError",
    "DatabaseOperationError",
    "RecordNotFoundError",
]
