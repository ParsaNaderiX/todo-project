"""Exception hierarchy for the todo application.

This module provides a structured exception system following Phase 2 layered architecture:
- Base exceptions: Root exception classes
- Repository exceptions: Data access layer failures
- Service exceptions: Business logic failures
"""

from app.exceptions.base import TodoError
from app.exceptions.repository_exceptions import (
    RepositoryError,
    DatabaseConnectionError,
    DatabaseOperationError,
    RecordNotFoundError,
)
from app.exceptions.service_exceptions import (
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

__all__ = [
    # Base exceptions
    "TodoError",
    # Repository exceptions
    "RepositoryError",
    "DatabaseConnectionError",
    "DatabaseOperationError",
    "RecordNotFoundError",
    # Service exceptions
    "ValidationError",
    "ProjectError",
    "ProjectNotFoundError",
    "DuplicateProjectError",
    "ProjectLimitError",
    "TaskError",
    "TaskNotFoundError",
    "DuplicateTaskError",
    "TaskLimitError",
]

