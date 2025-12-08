"""Task ORM model."""

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.project import Project


class Task(Base):
    """ORM model representing a task within a project.
    
    Attributes:
        id: Primary key identifier
        name: Task name (unique within project)
        description: Task description
        status: Task status (default: 'todo')
        deadline: Task deadline date
        closed_at: Timestamp when task was closed (NEW FIELD for Phase 2)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        project_id: Foreign key to associated project
        project: Relationship to associated project
    """
    
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="todo")
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Relationship: many-to-one with Project
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="tasks",
        lazy="select"
    )
    
    # Unique constraint: task names must be unique within a project
    __table_args__ = (
        UniqueConstraint("project_id", "name", name="uq_task_project_name"),
    )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status}', project_id={self.project_id})>"

