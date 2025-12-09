# Todo Project - Phase 1: CLI Application

> **DEPRECATION NOTICE**: The CLI is deprecated. Please use the REST API exposed at `/api/v1`. See "Running the API" below.

A modular To-Do application built with clean architecture principles. This semester-long Software Engineering project demonstrates professional software development practices in Python.

## Overview

This is Phase 1 of a comprehensive To-Do application being developed throughout the semester as part of a Software Engineering course. The project will evolve from a command-line interface to a full-stack web application while maintaining clean architecture principles.

### Project Phases

All development phases will be tracked in this repository:

- **Phase 1 (Current)**: CLI Application with In-Memory Storage
- **Phase 2**: Database Integration
- **Phase 3**: REST API
- **Phase 4**: Web Interface

## Running the API

- Start the server: `python run_api.py`
- Base URL: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

Projects:
- `POST /api/v1/projects` — Create project (201)
- `GET /api/v1/projects` — List projects (supports `skip`, `limit`)
- `GET /api/v1/projects/{project_id}` — Get project (200/404)
- `PUT /api/v1/projects/{project_id}` — Update project (200/404)
- `DELETE /api/v1/projects/{project_id}` — Delete project (204/404)

Tasks:
- `POST /api/v1/projects/{project_id}/tasks` — Create task (201)
- `GET /api/v1/projects/{project_id}/tasks` — List tasks
- `GET /api/v1/projects/{project_id}/tasks/{task_id}` — Get task
- `PUT /api/v1/projects/{project_id}/tasks/{task_id}` — Update task
- `PATCH /api/v1/projects/{project_id}/tasks/{task_id}/status` — Update status only
- `DELETE /api/v1/projects/{project_id}/tasks/{task_id}` — Delete task

### API Usage Examples

Create a project (curl):
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Marketing Website", "description": "Launch tasks"}'
```

Create a task in a project (curl):
```bash
curl -X POST http://localhost:8000/api/v1/projects/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"name": "Write landing copy", "status": "todo", "deadline": "2025-12-31"}'
```

Fetch tasks (Python requests):
```python
import requests

resp = requests.get("http://localhost:8000/api/v1/projects/1/tasks")
resp.raise_for_status()
print(resp.json())
```

## Current Features

### Project Management
- Create projects with names and descriptions
- Edit existing project details
- Delete projects (with cascade deletion of tasks)
- View all projects with task counts
- Unique project name validation
- Configurable project limits (default: 10)

### Task Management
- Add tasks to projects with full details
- Edit task information (name, description, status, deadline)
- Quick status updates (TODO, DOING, DONE)
- Delete individual tasks
- View all tasks across all projects
- Deadline validation (YYYY-MM-DD format)
- Unique task names within projects

### Validation & Error Handling
- Comprehensive input validation
- Word count limits (30 words for names, 150 for descriptions)
- Date validation with past date prevention
- Status validation (todo, doing, done)
- User-friendly error messages
- Graceful error handling with recovery
- Confirmation prompts for destructive actions

### Technical Highlights
- Clean architecture with separation of concerns
- Port/Adapter pattern for storage abstraction
- Type hints throughout the codebase
- Custom exception hierarchy
- Environment-based configuration
- Modular package structure
- Extensible design for future phases

## Architecture

This project follows Clean Architecture principles with a clear separation between layers:

```
┌─────────────────────────────────────────┐
│         CLI Layer (Presentation)        │
│    - User interaction & display         │
│    - Input handling & validation UI     │
│    - Error display & confirmations      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Service Layer (Business Logic)    │
│    - Core business operations           │
│    - Validation orchestration           │
│    - Exception handling                 │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Storage Port (Abstract Interface)  │
│    - Defines storage contract           │
│    - Technology-agnostic                │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼──────────┐
│   In-Memory    │   │    Database       │
│    Storage     │   │    Storage        │
│   (Phase 1)    │   │   (Phase 2)       │
└────────────────┘   └───────────────────┘
```

### Architecture Benefits

1. **Dependency Inversion**: High-level modules (service layer) don't depend on low-level modules (storage)
2. **Testability**: Each layer can be tested independently
3. **Maintainability**: Changes in one layer don't cascade to others
4. **Extensibility**: New storage implementations can be added without touching business logic
5. **Future-Proof**: Ready for database, API, and web UI without major refactoring

## Installation

### Prerequisites

- Python 3.14+
- pip or Poetry for dependency management
- Git for version control

### Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/ParsaNaderiX/todo-project.git
   cd todo-project
   ```

2. Set up virtual environment
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using Poetry
   poetry install
   poetry shell
   ```

3. Install dependencies
   ```bash
   # With pip
   pip install python-dotenv
   
   # With Poetry
   poetry add python-dotenv
   ```

4. Configure environment (optional)
   ```bash
   cp .example.env .env
   # Edit .env to customize limits
   ```

### Configuration Options

Create a `.env` file to customize application settings:

```env
# Maximum number of projects allowed
MAX_NUMBER_OF_PROJECT=10

# Maximum number of tasks per project
MAX_NUMBER_OF_TASK=50
```

## Usage

### Starting the Application

```bash
python -m app.cli
```

### Available Commands

When you start the application, you'll see this menu:

```
Welcome to the To-Do List Application!
Please select an option:
1. Add a new project
2. Add a new task
3. Edit a project
4. Edit a task
5. Edit task status
6. Delete a project
7. Delete a task
8. View all projects
9. View all tasks
10. Exit
```

### Validation Examples

The application enforces strict validation:

```
Project name is required.
Project name must be <= 30 words.
Project name must be unique.
Task status must be one of: todo, doing, done.
Task deadline must be in YYYY-MM-DD format.
Task deadline cannot be in the past.
```

## Project Structure

```
todo-project/
├── app/
│   ├── __init__.py
│   │
│   ├── cli/                      # Command-Line Interface Layer
│   │   ├── __init__.py
│   │   ├── __main__.py          # Main entry point with menu loop
│   │   ├── menus.py             # User interaction & display functions
│   │   └── utils.py             # Error handling & helper functions
│   │
│   ├── core/                     # Domain Layer (Business Models)
│   │   ├── __init__.py
│   │   ├── models.py            # Project & Task domain models
│   │   ├── exceptions.py        # Custom exception hierarchy
│   │   └── validation.py        # Validation logic & rules
│   │
│   ├── services/                 # Business Logic Layer
│   │   ├── __init__.py
│   │   └── todo_service.py      # Core business operations
│   │
│   ├── ports.py                  # Abstract Storage Interface
│   │
│   ├── storage/                  # Storage Implementations
│   │   ├── __init__.py
│   │   └── in_memory.py         # In-memory storage (Phase 1)
│   │
│   └── config/                   # Configuration Management
│       ├── __init__.py
│       └── settings.py          # Environment variables & defaults
│
├── .env                          # Environment configuration (not in repo)
├── .example.env                 # Environment template
├── .gitignore                   # Git ignore rules
├── pyproject.toml               # Project metadata & dependencies
└── README.md                    # This file
```

### Layer Responsibilities

| Layer | Responsibility | Example |
|-------|---------------|---------|
| CLI | User interaction, display | Show menus, get input, display results |
| Service | Business logic, validation | Create project, enforce limits, check uniqueness |
| Core | Domain models, validation rules | Project/Task classes, validation functions |
| Port | Abstract interface | StoragePort protocol definition |
| Storage | Data persistence | In-memory list operations |
| Config | Application settings | Load environment variables |

## Design Principles

### 1. Port/Adapter Pattern (Hexagonal Architecture)

Isolate business logic from infrastructure concerns.

```python
# Abstract interface (Port)
class StoragePort(Protocol):
    def add_project(self, project: Project) -> None: ...

# Current implementation (Adapter)
class InMemoryStorage:
    def add_project(self, project: Project) -> None:
        self.projects.append(project)

# Future implementation (Adapter)
class DatabaseStorage:
    def add_project(self, project: Project) -> None:
        db.session.add(project)
        db.session.commit()
```

The service layer code remains unchanged when swapping storage implementations.

### 2. Separation of Concerns

Each module has a single, well-defined responsibility:

- **Models**: Define data structure and relationships
- **Validation**: Enforce business rules
- **Service**: Orchestrate operations
- **Storage**: Persist data
- **CLI**: Handle user interaction

### 3. Validation Strategy

Validation happens in the storage layer during operations to ensure data integrity:

```python
def add_project(self, project: Project) -> None:
    validate_project_name(project.name)
    validate_project_description(project.description)
    validate_unique_project_name(project.name, self.projects)
    # ... then add
```

Note: In future refactorings, validation may move to service layer for even better separation.

### 4. Error Handling

Custom exception hierarchy provides clear error semantics:

```
TodoError (base)
├── ValidationError
├── ProjectError
│   ├── ProjectNotFoundError
│   ├── DuplicateProjectError
│   └── ProjectLimitError
└── TaskError
    ├── TaskNotFoundError
    ├── DuplicateTaskError
    └── TaskLimitError
```

The CLI layer catches these exceptions and displays user-friendly messages.

### 5. Type Safety

Comprehensive type hints throughout the codebase:

```python
def create_project(self, name: str, description: str) -> Project:
    """Create a new project with validation."""

def list_projects(self) -> List[Project]:
    """Retrieve all projects."""
```

Benefits: IDE autocomplete, early error detection, self-documenting code.

## Development Notes

### Key Improvements Made

Starting from a basic CLI application, the codebase was improved by:

- Restructuring into clean architecture layers
- Adding comprehensive error handling with user-friendly messages
- Implementing confirmation prompts for destructive actions
- Creating reusable utility functions for error handling
- Adding docstrings throughout the codebase
- Improving input validation and feedback
- Setting up Poetry for dependency management

### Challenges Addressed

1. Understanding when to use protocols versus inheritance
2. Deciding where validation logic should live
3. Making errors helpful without cluttering the CLI
4. Designing for future phases without over-engineering

---

## Phase 2 - Part 2: Scheduled Tasks

This part adds scheduled maintenance to the application so routine tasks
are handled automatically without manual intervention.

### What's New
- Automatic closure of overdue tasks
- Configurable scheduling using the `schedule` library
- Dry-run mode for safe testing (shows what would be closed)
- Status monitoring command to inspect overdue tasks
- Comprehensive logging for audit and troubleshooting

### New Commands

Auto-close overdue tasks (manual execution):
```bash
poetry run python -m app.commands.autoclose_overdue
poetry run python -m app.commands.autoclose_overdue --dry-run  # Test mode
```

Check overdue task status:
```bash
poetry run python -m app.commands.status
```

Run scheduler (continuous background process):
```bash
poetry run python -m app.commands.scheduler
```

### Configuration

Environment variables (add to your `.env` for local development):
```env
# How often to check for overdue tasks (in minutes)
SCHEDULER_INTERVAL_MINUTES=15
```

By default the scheduler runs every 15 minutes; adjust `SCHEDULER_INTERVAL_MINUTES`
to increase or decrease the frequency.

### How It Works
- A task is considered "overdue" when: `deadline < today` AND `status != 'done'`.
- When an overdue task is closed automatically the system:
    - sets `status` → `done`
    - sets `closed_at` → current timestamp
- The scheduler runs at the configured interval (default 15 minutes) and
    invokes the auto-close routine. Each run is logged to `logs/scheduler.log`.

### Running in Production

Development
- Run the scheduler directly while developing:
```bash
poetry run python -m app.commands.scheduler
```

Production
- Recommended: run the scheduler under a process manager (systemd, supervisor,
    or container orchestration) so it restarts on failure and logs are captured.
- Alternative: run via a cron job that executes the auto-close command at fixed
    intervals.

Example `systemd` service unit (save as `/etc/systemd/system/todo-scheduler.service`):
```ini
[Unit]
Description=Todo Project Scheduler
After=network.target

[Service]
Type=simple
User=todo_user
WorkingDirectory=/path/to/todo-project
ExecStart=/usr/bin/env poetry run python -m app.commands.scheduler
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

After creating the unit file:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now todo-scheduler.service
```

### Testing

Quick testing workflow:
```bash
# 1. Create test tasks with past deadlines using the CLI
poetry run python -m app.cli

# 2. Check overdue status (status command)
poetry run python -m app.commands.status

# 3. Test dry-run (safe, does not commit changes)
poetry run python -m app.commands.autoclose_overdue --dry-run

# 4. Actually close them
poetry run python -m app.commands.autoclose_overdue

# 5. Verify in database
docker exec -it todo-postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT name, status, closed_at FROM tasks;"
```

### Troubleshooting
- Scheduler not running → Check `logs/scheduler.log` and your process manager
    (systemd, supervisor) for failures.
- Tasks not closing → Verify task deadlines are valid `YYYY-MM-DD` dates and
    that the database connection (`DATABASE_URL`) is correct.
- Database connection errors → Ensure the DB is running and `DATABASE_URL`
    matches the running DB credentials.

---

## Version History

- **v0.3.0 (Current)** - Phase 3: FastAPI REST API, versioned routing, global error handling
- **v0.2.0** - Phase 2: Database integration, repository pattern, Alembic migrations
- **v0.1.0** - Phase 1: CLI application with in-memory storage
  - Full CRUD operations for projects and tasks
  - Comprehensive validation and error handling
  - Clean architecture implementation
  - User-friendly CLI with confirmations

---

## Phase 2: Database Integration

This phase moves the application from an in-memory prototype to a durable,
database-backed system using PostgreSQL. The goal is to provide reliable data
persistence, improved scalability, and a clearer separation between business
logic and infrastructure.

### What's New in Phase 2
- Migration from in-memory to PostgreSQL database
- Implementation of Repository Pattern
- Use of SQLAlchemy ORM for data modeling
- Database migrations with Alembic
- Docker containerization for PostgreSQL
- Data persistence across application restarts

### New Dependencies
- `SQLAlchemy` 2.0+
- `Alembic`
- `psycopg2-binary`
- `Docker` & `Docker Compose` (for running PostgreSQL locally)

### Setup Instructions for Phase 2

Prerequisites
- Docker Desktop (or another Docker runtime)
- Poetry (or an alternative Python dependency manager)

Start PostgreSQL with Docker Compose
```bash
docker-compose up -d
```

Environment configuration
- Copy the environment template and update the database URL and credentials:
```bash
cp .example.env .env
# Edit .env to set DATABASE_URL (or ensure docker-compose sets matching vars)
```

Database initialization
```bash
poetry run alembic upgrade head
```

> Note: Ensure `DATABASE_URL` points to the running PostgreSQL instance. The
> project provides a `docker-compose.yml` to start a local DB for development.

### Updated Architecture Diagram

The layered architecture is now explicit about the repository and database layers:

```
CLI Layer → Service Layer → Repository Layer → Database Layer
```

- CLI Layer: Handles user interaction, input, and presentation (unchanged).
- Service Layer: Orchestrates business logic and validation; calls repositories.
- Repository Layer: Encapsulates data access (SQLAlchemy + ORM mappings).
- Database Layer: PostgreSQL instance managed via Docker / Docker Compose.

Each layer has a single responsibility: the service layer calls repositories
instead of directly manipulating storage, which improves testability and
separation of concerns.

### Phase 3 Architecture (with API)

```
API (FastAPI controllers)
        │
        ▼
Service Layer (business rules, validation)
        │
        ▼
Repository Layer (SQLAlchemy)
        │
        ▼
Database
```

The API layer is a thin adapter that depends on the service layer via dependency injection.

## Phase 4: Postman API Testing

### Overview
Complete Postman collection and environment to exercise the FastAPI application end-to-end.

### Setup Instructions
1. Import `postman_collection.json` (ToDoList_API_Phase4).
2. Import `postman_environment.json` (ToDoList_Environment).
3. Select the "Local Development" environment.
4. Ensure the FastAPI server is running at `http://127.0.0.1:8000`.

### Endpoints Tested
**Projects**
- GET /api/v1/projects
- GET /api/v1/projects/{id}
- POST /api/v1/projects
- PUT /api/v1/projects/{id}
- DELETE /api/v1/projects/{id}

**Tasks**
- GET /api/v1/projects/{project_id}/tasks
- GET /api/v1/projects/{project_id}/tasks/{task_id}
- POST /api/v1/projects/{project_id}/tasks
- PUT /api/v1/projects/{project_id}/tasks/{task_id}
- PATCH /api/v1/projects/{project_id}/tasks/{task_id}/status
- DELETE /api/v1/projects/{project_id}/tasks/{task_id}

### Testing Notes
- All endpoints return appropriate HTTP status codes.
- Request/response bodies follow RESTful conventions.
- Validation errors surface as structured error responses.

### Database Operations
- Run migrations:
```bash
poetry run alembic upgrade head
```
- Rollback (downgrade one migration):
```bash
poetry run alembic downgrade -1
```
- Access PostgreSQL directly (example using Docker Compose):
```bash
docker-compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
```
- View database tables (inside `psql`):
```sql
\dt
```

### Migration from Phase 1
- The storage implementation migrated from an in-memory adapter to a
    repository-backed PostgreSQL implementation. Business logic now talks to
    repositories instead of directly manipulating in-memory lists.
- Data now persists across application restarts and is managed via Alembic
    migrations.
- The old `InMemoryStorage` implementation has been removed (or deprecated)
    in favor of repository classes using SQLAlchemy sessions.

---
