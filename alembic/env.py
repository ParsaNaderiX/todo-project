"""Alembic environment configuration for database migrations.

This file configures Alembic to:
- Read DATABASE_URL from environment variables (.env file)
- Import all ORM models for autogenerate support
- Use SQLAlchemy 2.0 compatible syntax
"""

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool

from alembic import context

# Add project root to Python path to enable imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    env_path = project_root / ".env"
    load_dotenv(env_path)
except ImportError:
    # dotenv not available, rely on system environment variables
    pass
except Exception:
    # .env file might not exist, that's okay
    pass

# Import Base and all models so Alembic can detect schema changes
# This must be done after setting up the path and loading env vars
from app.db.base import Base  # noqa: E402

# Import all models to ensure they are registered with Base.metadata
# This is required for Alembic's autogenerate feature
from app.models import Project, Task  # noqa: E402, F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target_metadata to Base.metadata for autogenerate support
# This tells Alembic which metadata to compare against when generating migrations
target_metadata = Base.metadata

# Override sqlalchemy.url from environment variable if not set in alembic.ini
# This allows us to use DATABASE_URL from .env file instead of hardcoding
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
elif not config.get_main_option("sqlalchemy.url"):
    raise RuntimeError(
        "DATABASE_URL environment variable is required. "
        "Please set it in your .env file or environment."
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    if url is None:
        raise RuntimeError("Database URL not configured")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    Uses SQLAlchemy 2.0 compatible engine_from_config.

    """
    # Get database URL from config (set from environment variable above)
    configuration = config.get_section(config.config_ini_section, {})
    
    # Ensure sqlalchemy.url is set
    if "sqlalchemy.url" not in configuration:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            configuration["sqlalchemy.url"] = database_url
        else:
            raise RuntimeError(
                "DATABASE_URL environment variable is required. "
                "Please set it in your .env file or environment."
            )

    # Create engine using SQLAlchemy 2.0 compatible configuration
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
