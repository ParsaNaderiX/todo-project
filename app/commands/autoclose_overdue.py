"""Script to automatically close overdue tasks.

Usage:
    python -m app.commands.autoclose_overdue

This command will mark tasks whose deadline is before today and are not
already marked as `done` as `done`, set their `closed_at` timestamp, and
persist the changes.
"""
from datetime import datetime
from typing import List

from app.db.session import get_db
from app.repositories import TaskRepository
from app.exceptions import DatabaseOperationError


def autoclose_overdue_tasks() -> None:
    """Close overdue tasks by setting status to 'done' and recording closed_at.

    Behavior:
    - Obtains a DB session via `get_db()`.
    - Uses `TaskRepository.get_overdue_tasks()` to find overdue tasks.
    - Marks each task as done, sets `closed_at` to now (UTC), and commits.
    - Prints a summary of actions taken.
    """
    db = next(get_db())
    closed_count = 0
    try:
        repo = TaskRepository(db)

        try:
            overdue: List = repo.get_overdue_tasks()
        except Exception as e:
            print(f"Error fetching overdue tasks: {e}")
            return

        if not overdue:
            print("No overdue tasks found")
            return

        for task in overdue:
            try:
                # Update in-memory ORM object
                task.status = "done"
                task.closed_at = datetime.utcnow()

                # Persist changes
                db.add(task)
                db.commit()
                db.refresh(task)

                proj_name = getattr(task, "project", None)
                proj_display = proj_name.name if proj_name and getattr(proj_name, "name", None) else str(task.project_id)
                print(f"Closed task: {task.name} (Project: {proj_display})")
                closed_count += 1
            except DatabaseOperationError as db_err:
                # Repository-level DB errors
                print(f"Database error closing task id={getattr(task, 'id', '<unknown>')}: {db_err}")
                try:
                    db.rollback()
                except Exception:
                    pass
            except Exception as err:
                print(f"Unexpected error closing task id={getattr(task, 'id', '<unknown>')}: {err}")
                try:
                    db.rollback()
                except Exception:
                    pass

        print(f"Closed {closed_count} overdue tasks")

    except Exception as e:
        print(f"Unexpected error in autoclose_overdue_tasks: {e}")
    finally:
        try:
            db.close()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        autoclose_overdue_tasks()
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Fatal error running autoclose command: {e}")
