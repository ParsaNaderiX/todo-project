import os

try:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    pass


def _get_positive_int_env(var_name: str, default_value: int) -> int:
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


MAX_NUMBER_OF_PROJECT: int = _get_positive_int_from_candidates([
    "MAX_NUMBER_OF_PROJECT",
    "PROJECT_OF_NUMBER_MAX",
], 10)

MAX_NUMBER_OF_TASK: int = _get_positive_int_from_candidates([
    "MAX_NUMBER_OF_TASK",
    "TASK_OF_NUMBER_MAX",
], 50)

PROJECT_OF_NUMBER_MAX: int = MAX_NUMBER_OF_PROJECT
TASK_OF_NUMBER_MAX: int = MAX_NUMBER_OF_TASK


