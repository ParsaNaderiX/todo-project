"""Configuration settings for the todo application."""
import os

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass


def _get_positive_int_env(var_name: str, default_value: int) -> int:
    """Get a positive integer from environment variable.
    
    Args:
        var_name: Name of the environment variable
        default_value: Default value if var not found or invalid
        
    Returns:
        The positive integer value or default_value
    """
    raw_value = os.getenv(var_name)
    if raw_value is None:
        return default_value
    try:
        parsed = int(raw_value)
        if parsed < 1:
            return default_value
        return parsed
    except ValueError:
        return default_value


# Maximum number of projects allowed in the application
MAX_NUMBER_OF_PROJECT: int = _get_positive_int_env("MAX_NUMBER_OF_PROJECT", 10)

# Maximum number of tasks allowed per project
MAX_NUMBER_OF_TASK: int = _get_positive_int_env("MAX_NUMBER_OF_TASK", 50)


