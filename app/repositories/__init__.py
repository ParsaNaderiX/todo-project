"""Repository layer for database operations.

This module provides repository classes that implement the Repository Pattern,
handling all database operations for entities with proper error handling.
"""

from app.repositories.project_repository import ProjectRepository

__all__ = [
    "ProjectRepository",
]

