import os

# Load environment variables from a .env file if python-dotenv is installed.
try:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    # If dotenv isn't installed or load fails, silently continue using OS env.
    pass


def _get_positive_int_env(var_name: str, default_value: int) -> int:
    """
    Read a positive integer from environment; fall back to default on any error.
    Values less than 1 are clamped to the default to avoid invalid caps.
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


def _get_positive_int_from_candidates(candidates: list[str], default_value: int) -> int:
    for key in candidates:
        value = os.getenv(key)
        if value is None:
            continue
        try:
            parsed = int(value)
            if parsed > 0:
                return parsed
        except ValueError:
            continue
    return default_value


# Default caps if not provided via environment
# Preferred names
MAX_NUMBER_OF_PROJECT: int = _get_positive_int_from_candidates([
    "MAX_NUMBER_OF_PROJECT",
    "PROJECT_OF_NUMBER_MAX",  # backward compatibility
], 10)

MAX_NUMBER_OF_TASK: int = _get_positive_int_from_candidates([
    "MAX_NUMBER_OF_TASK",
    "TASK_OF_NUMBER_MAX",  # backward compatibility
], 50)

# Backward-compatible aliases (old names used elsewhere in code)
PROJECT_OF_NUMBER_MAX: int = MAX_NUMBER_OF_PROJECT
TASK_OF_NUMBER_MAX: int = MAX_NUMBER_OF_TASK
