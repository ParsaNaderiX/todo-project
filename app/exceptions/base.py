"""Base exception classes for the todo application."""


class TodoError(Exception):
    """Base exception for all todo application errors.
    
    All custom exceptions in the todo application should inherit from this class.
    This allows for catching all application-specific errors with a single exception type.
    
    Example:
        try:
            # Some operation
        except TodoError as e:
            # Handle any todo application error
    """

    pass

