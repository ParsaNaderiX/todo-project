"""Repository for Project entity database operations.

This module implements the Repository Pattern for Project entity,
handling all database operations with proper error handling and validation.
"""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import MAX_NUMBER_OF_PROJECT
from app.core.validation import (
    validate_project_description,
    validate_project_name,
)
from app.exceptions.repository_exceptions import DatabaseOperationError
from app.exceptions.service_exceptions import (
    DuplicateProjectError,
    ProjectLimitError,
    ProjectNotFoundError,
)
from app.models.project import Project


class ProjectRepository:
    """Repository for Project entity database operations.
    
    This class handles all database operations for the Project entity,
    including CRUD operations, validation, and error handling.
    
    Attributes:
        db: SQLAlchemy database session
    """
    
    def __init__(self, db: Session) -> None:
        """Initialize the repository with a database session.
        
        Args:
            db: SQLAlchemy Session instance (dependency injection)
        """
        self.db = db
    
    def create(self, name: str, description: str) -> Project:
        """Create and save a new project.
        
        This method:
        - Validates the project name and description
        - Checks if project limit has been reached
        - Checks for duplicate project names
        - Creates and saves the project to the database
        - Handles database constraint violations
        
        Args:
            name: Project name
            description: Project description
            
        Returns:
            The created Project ORM model instance
            
        Raises:
            ValidationError: If name or description validation fails
            ProjectLimitError: If maximum number of projects has been reached
            DuplicateProjectError: If a project with the same name already exists
            DatabaseOperationError: If database operation fails
        """
        # Validate input
        validate_project_name(name)
        validate_project_description(description)
        
        # Check project limit
        count_stmt = select(func.count(Project.id))
        project_count = self.db.scalar(count_stmt) or 0
        
        if project_count >= MAX_NUMBER_OF_PROJECT:
            raise ProjectLimitError(
                f"Cannot create more than {MAX_NUMBER_OF_PROJECT} projects."
            )
        
        # Check for duplicate name
        if self.exists_by_name(name):
            raise DuplicateProjectError(f"Project '{name}' already exists.")
        
        # Create new project
        project = Project(name=name, description=description)
        
        try:
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            return project
        except IntegrityError as e:
            self.db.rollback()
            # Check if it's a unique constraint violation
            if "unique" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise DuplicateProjectError(f"Project '{name}' already exists.") from e
            raise DatabaseOperationError(f"Failed to create project: {e}") from e
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationError(f"Failed to create project: {e}") from e
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Fetch project by ID.
        
        Args:
            project_id: The ID of the project to fetch
            
        Returns:
            Project instance if found, None otherwise
        """
        try:
            stmt = select(Project).where(Project.id == project_id)
            return self.db.scalar(stmt)
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch project by ID: {e}") from e
    
    def get_all(self) -> List[Project]:
        """Return all projects ordered by creation date (newest first).
        
        Returns:
            List of all Project instances, ordered by created_at descending
            
        Raises:
            DatabaseOperationError: If database operation fails
        """
        try:
            stmt = select(Project).order_by(Project.created_at.desc())
            result = self.db.scalars(stmt)
            return list(result.all())
        except Exception as e:
            raise DatabaseOperationError(f"Failed to fetch all projects: {e}") from e
    
    def update(self, project_id: int, name: str, description: str) -> Project:
        """Update an existing project.
        
        This method:
        - Validates the new project data
        - Checks for duplicate names (excluding current project)
        - Updates the project in the database
        - Handles database constraint violations
        
        Args:
            project_id: The ID of the project to update
            name: New project name
            description: New project description
            
        Returns:
            The updated Project ORM model instance
            
        Raises:
            ValidationError: If name or description validation fails
            ProjectNotFoundError: If project with given ID does not exist
            DuplicateProjectError: If a project with the same name already exists
            DatabaseOperationError: If database operation fails
        """
        # Validate input
        validate_project_name(name)
        validate_project_description(description)
        
        # Fetch project
        project = self.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        
        # Check for duplicate name (excluding current project)
        if self.exists_by_name(name, exclude_id=project_id):
            raise DuplicateProjectError(f"Project '{name}' already exists.")
        
        # Update project
        project.name = name
        project.description = description
        
        try:
            self.db.commit()
            self.db.refresh(project)
            return project
        except IntegrityError as e:
            self.db.rollback()
            # Check if it's a unique constraint violation
            if "unique" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise DuplicateProjectError(f"Project '{name}' already exists.") from e
            raise DatabaseOperationError(f"Failed to update project: {e}") from e
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationError(f"Failed to update project: {e}") from e
    
    def delete(self, project_id: int) -> None:
        """Delete a project by ID.
        
        Tasks associated with the project will be cascade deleted
        (configured in the ORM model relationship).
        
        Args:
            project_id: The ID of the project to delete
            
        Raises:
            ProjectNotFoundError: If project with given ID does not exist
            DatabaseOperationError: If database operation fails
        """
        # Fetch project
        project = self.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        
        try:
            self.db.delete(project)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseOperationError(f"Failed to delete project: {e}") from e
    
    def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a project with the given name already exists.
        
        Args:
            name: The project name to check
            exclude_id: Optional project ID to exclude from the check
                       (useful when updating a project)
        
        Returns:
            True if a project with the name exists, False otherwise
            
        Raises:
            DatabaseOperationError: If database operation fails
        """
        try:
            stmt = select(Project).where(Project.name == name)
            if exclude_id is not None:
                stmt = stmt.where(Project.id != exclude_id)
            
            result = self.db.scalar(stmt)
            return result is not None
        except Exception as e:
            raise DatabaseOperationError(f"Failed to check project name existence: {e}") from e

