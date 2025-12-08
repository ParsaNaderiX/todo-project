"""Configuration settings for the todo application."""
import os
from typing import Optional

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


def _get_required_env(var_name: str) -> str:
    """Retrieve required environment variable or raise a clear error."""
    value = os.getenv(var_name)
    if value is None or value.strip() == "":
        # For development and import-time safety, provide a sensible default
        # for the database URL so modules can be imported without requiring
        # environment setup. Production deployments should set
        # `DATABASE_URL` explicitly.
        if var_name == "DATABASE_URL":
            return "sqlite:///./dev.db"
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value


# Database configuration
DATABASE_URL: str = _get_required_env("DATABASE_URL")
DB_HOST: Optional[str] = os.getenv("DB_HOST")
DB_PORT: Optional[str] = os.getenv("DB_PORT")
DB_NAME: Optional[str] = os.getenv("DB_NAME")
DB_USER: Optional[str] = os.getenv("DB_USER")
DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD")


