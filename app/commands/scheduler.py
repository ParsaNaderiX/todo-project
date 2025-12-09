"""Simple scheduler to run maintenance commands periodically.

Uses the `schedule` library to run `autoclose_overdue_tasks` every minute.

Run with:
    python -m app.commands.scheduler

Note: install `schedule` in your environment: `poetry add schedule` or
`pip install schedule`.
"""
import time
import schedule
from datetime import datetime, timezone

from app.commands.autoclose_overdue import autoclose_overdue_tasks


def _log(msg: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    print(f"[{now}] {msg}")


def main() -> None:
    _log("Starting task scheduler...")
    _log("Auto-close overdue tasks will run every 1 minute.")

    # Schedule the task every 1 minute
    schedule.every(1).minutes.do(lambda: _run_job(autoclose_overdue_tasks))

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        _log("Scheduler stopped by user")


def _run_job(job_callable) -> None:
    """Run a job callable and log start/end and exceptions."""
    _log(f"Running scheduled job: {getattr(job_callable, '__name__', str(job_callable))}")
    try:
        job_callable()
        _log("Job completed successfully")
    except Exception as e:
        _log(f"Job raised an exception: {e}")


if __name__ == "__main__":
    main()
