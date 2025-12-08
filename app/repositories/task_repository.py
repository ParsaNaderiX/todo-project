"""Repository for Task entity database operations.

Implements the Repository Pattern for Task entity using SQLAlchemy 2.0 style
queries (`select` / `session.execute` / `session.scalar`) and provides
validation, error handling and convenient data access methods used by services
and CLI code.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.config import MAX_NUMBER_OF_TASK
from app.core.validation import (
    validate_task_deadline,
    validate_task_description,
    validate_task_name,
    validate_task_status,
)
from app.exceptions import (
    DatabaseOperationError,
    DuplicateTaskError,
    ProjectNotFoundError,
    TaskLimitError,
    TaskNotFoundError,
    ValidationError,
)
from app.models.project import Project
from app.models.task import Task


class TaskRepository:
    """Repository for Task entity database operations.

    This class encapsulates all DB access related to tasks. It validates input
    using centralized validators, enforces business rules (task limits,
    uniqueness), and maps SQLAlchemy exceptions to application exceptions.

    Attributes:
        db: SQLAlchemy `Session` instance injected by caller.
    """

    def __init__(self, db: Session) -> None:
        """Initialize repository with a DB session (dependency injection).

        Args:
            db: SQLAlchemy `Session`.
        """
        self.db = db

    def create(
        self,
        project_id: int,
        name: str,
        description: str,
        status: str,
        deadline: Optional[str],
    ) -> Task:
        """Create and persist a new Task in the given project.

        Steps:
        - Verify project exists.
        - Validate task fields using validators in `app.core.validation`.
        - Enforce task count limit per project (raises `TaskLimitError`).
        - Ensure task name is unique within project (raises `DuplicateTaskError`).
        - Insert, commit and return the created `Task` model.

        Args:
            project_id: ID of the owning project.
            name: Task name.
            description: Task description.
            status: Task status string (will be normalized by validator).
            deadline: Optional deadline string in `YYYY-MM-DD` format.

        Returns:
            The created `Task` ORM instance.

        Raises:
            ValidationError: If validation fails.
            ProjectNotFoundError: If the project does not exist.
            TaskLimitError: If project has reached `MAX_NUMBER_OF_TASK`.
            DuplicateTaskError: If a task with the same name already exists in project.
            DatabaseOperationError: For unexpected DB errors.
        """
        # Verify project exists
        try:
            proj_stmt = select(Project).where(Project.id == project_id)
            project = self.db.scalar(proj_stmt)
        except Exception as e:
            raise DatabaseOperationError(f"Failed to verify project existence: {e}") from e

        if project is None:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

        # Validate inputs
        validate_task_name(name)
        validate_task_description(description)
        normalized_status = validate_task_status(status)
        validate_task_deadline(deadline)

        # Enforce task limit
        try:
            count_stmt = select(func.count(Task.id)).where(Task.project_id == project_id)
            task_count = self.db.scalar(count_stmt) or 0
        except Exception as e:
            raise DatabaseOperationError(f"Failed to count tasks for project: {e}") from e

        if task_count >= MAX_NUMBER_OF_TASK:
            raise TaskLimitError(f"Cannot create more than {MAX_NUMBER_OF_TASK} tasks in project {project_id}.")

        # Uniqueness check
        if self.exists_by_name_in_project(project_id, name):
            raise DuplicateTaskError(f"Task '{name}' already exists in project {project_id}.")

        # Parse deadline into date if provided
        parsed_deadline: Optional[date] = None
        if deadline is not None and str(deadline).strip():
            parsed_deadline = datetime.strptime(str(deadline).strip(), "%Y-%m-%d").date()

        task = Task(
            project_id=project_id,
            name=name,
            description=description,
            status=normalized_status,
            deadline=parsed_deadline,
        )

        try:
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except IntegrityError as e:
            self.db.rollback()
            # Detect unique constraint violation
            if "unique" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise DuplicateTaskError(f"Task '{name}' already exists in project {project_id}.") from e
            raise DatabaseOperationError(f"Failed to create task: {e}") from e
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationError(f"Failed to create task: {e}") from e

    def get_by_id(self, project_id: int, task_id: int) -> Optional[Task]:
        """Fetch a task by ID scoped to a specific project.

        Returns `None` when no such task exists or it does not belong to the project.
        """
        try:
            stmt = select(Task).where(Task.id == task_id, Task.project_id == project_id)
            return self.db.scalar(stmt)
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch task by id: {e}") from e

    def get_all_by_project(self, project_id: int) -> List[Task]:
        """Return all tasks for a specific project ordered by `created_at` desc.

        Raises `ProjectNotFoundError` if the project does not exist.
        """
        # ensure project exists
        try:
            proj_stmt = select(Project).where(Project.id == project_id)
            project = self.db.scalar(proj_stmt)
        except Exception as e:
            raise DatabaseOperationError(f"Failed to verify project existence: {e}") from e

        if project is None:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

        try:
            stmt = select(Task).where(Task.project_id == project_id).order_by(Task.created_at.desc())
            result = self.db.scalars(stmt)
            return list(result.all())
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch tasks for project {project_id}: {e}") from e

    def get_all(self) -> List[Task]:
        """Return all tasks across all projects, with project relationship eagerly loaded.

        Useful for "View all tasks" feature.
        """
        try:
            stmt = select(Task).options(selectinload(Task.project)).order_by(Task.created_at.desc())
            result = self.db.scalars(stmt)
            return list(result.all())
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch all tasks: {e}") from e

    def update(
        self,
        task_id: int,
        name: str,
        description: str,
        status: str,
        deadline: Optional[str],
    ) -> Task:
        """Update an existing task by ID.

        Validates inputs and enforces uniqueness within the owning project
        (excluding the current task). Raises `TaskNotFoundError` if the task
        doesn't exist.
        """
        # Fetch task
        try:
            stmt = select(Task).where(Task.id == task_id)
            task = self.db.scalar(stmt)
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch task for update: {e}") from e

        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")

        # Validate inputs
        validate_task_name(name)
        validate_task_description(description)
        normalized_status = validate_task_status(status)
        validate_task_deadline(deadline)

        # Uniqueness check within project (exclude current task)
        if self.exists_by_name_in_project(task.project_id, name, exclude_id=task_id):
            raise DuplicateTaskError(f"Task '{name}' already exists in project {task.project_id}.")

        # Parse deadline
        parsed_deadline: Optional[date] = None
        if deadline is not None and str(deadline).strip():
            parsed_deadline = datetime.strptime(str(deadline).strip(), "%Y-%m-%d").date()

        # Apply updates
        task.name = name
        task.description = description
        task.status = normalized_status
        task.deadline = parsed_deadline

        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except IntegrityError as e:
            self.db.rollback()
            if "unique" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise DuplicateTaskError(f"Task '{name}' already exists in project {task.project_id}.") from e
            raise DatabaseOperationError(f"Failed to update task: {e}") from e
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationError(f"Failed to update task: {e}") from e

    def update_status(self, task_id: int, status: str) -> Task:
        """Update only the `status` field of a task.

        Validates status using the central validator. Raises `TaskNotFoundError`
        when the task does not exist.
        """
        try:
            stmt = select(Task).where(Task.id == task_id)
            task = self.db.scalar(stmt)
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch task for status update: {e}") from e

        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")

        normalized_status = validate_task_status(status)
        task.status = normalized_status

        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationError(f"Failed to update task status: {e}") from e

    def delete(self, project_id: int, task_id: int) -> None:
        """Delete a task by ID, verifying it belongs to the specified project.

        Raises `TaskNotFoundError` if the task does not exist or does not belong
        to the project.
        """
        try:
            stmt = select(Task).where(Task.id == task_id, Task.project_id == project_id)
            task = self.db.scalar(stmt)
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch task for deletion: {e}") from e

        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")

        try:
            self.db.delete(task)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationError(f"Failed to delete task: {e}") from e

    def exists_by_name_in_project(self, project_id: int, name: str, exclude_id: Optional[int] = None) -> bool:
        """Return True if a task with `name` exists in `project_id`.

        If `exclude_id` is provided it will be excluded from the check (useful
        when updating a task).
        """
        try:
            stmt = select(Task).where(Task.project_id == project_id, Task.name == name)
            if exclude_id is not None:
                stmt = stmt.where(Task.id != exclude_id)
            existing = self.db.scalar(stmt)
            return existing is not None
        except Exception as e:
            raise DatabaseOperationError(f"Failed to check task name existence: {e}") from e

    def get_overdue_tasks(self) -> List[Task]:
        """Return all tasks where deadline < today and status != 'done'.

        Tasks without a deadline are ignored. Results are ordered by nearest
        deadline first.
        """
        today = date.today()
        try:
            stmt = (
                select(Task)
                .where(Task.deadline.isnot(None))
                .where(Task.deadline < today)
                .where(Task.status != "done")
                .order_by(Task.deadline.asc())
            )
            result = self.db.scalars(stmt)
            return list(result.all())
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch overdue tasks: {e}") from e
