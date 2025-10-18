"""Utility functions for CLI error handling and display."""
from typing import Optional, TypeVar, Callable, Any

from app.core.exceptions import (
    TodoError,
    ValidationError,
    ProjectError,
    TaskError,
    ProjectNotFoundError,
    TaskNotFoundError,
    ProjectLimitError,
    TaskLimitError,
)


T = TypeVar("T")


def handle_application_error(func: Callable[..., T], *args: Any, **kwargs: Any) -> Optional[T]:
    """Execute a function and handle any application errors gracefully.
    
    Args:
        func: The function to execute
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
        
    Returns:
        The function result if successful, None if an error occurred
        
    Example:
        result = handle_application_error(service.create_project, name, description)
        if result is not None:
            print(f"Created project: {result.name}")
    """
    try:
        return func(*args, **kwargs)
    except ValidationError as e:
        print(f"Validation error: {str(e)}")
    except ProjectLimitError as e:
        print(f"Project limit reached: {str(e)}")
    except TaskLimitError as e:
        print(f"Task limit reached: {str(e)}")
    except ProjectNotFoundError as e:
        print(f"Project not found: {str(e)}")
    except TaskNotFoundError as e:
        print(f"Task not found: {str(e)}")
    except ProjectError as e:
        print(f"Project error: {str(e)}")
    except TaskError as e:
        print(f"Task error: {str(e)}")
    except TodoError as e:
        print(f"Application error: {str(e)}")
    except ValueError as e:
        print(f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    return None


def display_error(message: str) -> None:
    """Display an error message to the user.
    
    Args:
        message: The error message to display
    """
    print(f"Error: {message}")


def confirm_action(prompt: str) -> bool:
    """Ask user to confirm an action.
    
    Args:
        prompt: The confirmation prompt to show
        
    Returns:
        True if user confirms, False otherwise
    """
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")