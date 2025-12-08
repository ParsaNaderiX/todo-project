"""Repository layer exceptions for data access failures.

These exceptions represent errors that occur at the data access layer,
such as database connection issues, query failures, or record not found errors.
"""

from app.exceptions.base import TodoError


class RepositoryError(TodoError):
    """Base exception for all repository/data access layer errors.
    
    This exception should be raised when errors occur during data access operations
    that are not specific to a particular entity or operation type.
    
    Example:
        raise RepositoryError("Failed to execute database query")
    """

    pass


class DatabaseConnectionError(RepositoryError):
    """Raised when a database connection cannot be established.
    
    This exception should be raised when:
    - Database server is unreachable
    - Connection timeout occurs
    - Authentication fails
    - Network issues prevent connection
    
    Example:
        raise DatabaseConnectionError("Could not connect to PostgreSQL database")
    """

    pass


class DatabaseOperationError(RepositoryError):
    """Raised when a database operation fails.
    
    This exception should be raised when:
    - SQL query execution fails
    - Transaction rollback is required
    - Constraint violations occur (that aren't handled by specific exceptions)
    - Database integrity errors occur
    
    Example:
        raise DatabaseOperationError("Failed to insert record: constraint violation")
    """

    pass


class RecordNotFoundError(RepositoryError):
    """Raised when a requested record cannot be found in the database.
    
    This is a generic exception for when any entity record is not found.
    For entity-specific "not found" errors, use the service layer exceptions
    (e.g., ProjectNotFoundError, TaskNotFoundError) which provide more context.
    
    This exception is useful for generic repository operations where the entity
    type is not known or when a more specific exception is not available.
    
    Example:
        raise RecordNotFoundError(f"Record with id {record_id} not found")
    """

    pass

