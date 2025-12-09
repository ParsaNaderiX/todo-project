# Todo Project - Complete Implementation

A modular To-Do application demonstrating clean architecture principles through progressive development phases. This Software Engineering course project evolved from a command-line interface to a full-stack application with database persistence, REST API, and scheduled maintenance.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development Phases](#development-phases)
- [Design Decisions](#design-decisions)
- [Database](#database)
- [Maintenance](#maintenance)

## Overview

This project implements a complete To-Do application following clean architecture principles and industry best practices. The application manages projects and tasks with full CRUD operations, validation, and scheduled maintenance capabilities.

### Technology Stack

- **Language**: Python 3.14+
- **Web Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Containerization**: Docker / Docker Compose
- **Scheduling**: Python Schedule library

### Project Status

All four development phases are complete:

- Phase 1: CLI Application (Deprecated)
- Phase 2: Database Integration
- Phase 3: REST API
- Phase 4: API Testing & Documentation

## Features

### Project Management
- Create projects with unique names and descriptions
- Update project details
- Delete projects (cascade deletes all tasks)
- List all projects with task counts
- Word count validation (30 words for names, 150 for descriptions)
- Configurable project limits (default: 10)

### Task Management
- Create tasks with name, description, status, and deadline
- Update task details or status independently
- Delete tasks
- List tasks by project or across all projects
- Status tracking (todo, doing, done)
- Deadline validation (YYYY-MM-DD format, no past dates)
- Unique task names within projects
- Configurable task limits per project (default: 50)

### Automated Maintenance
- Automatic closure of overdue tasks
- Configurable scheduling (default: every 15 minutes)
- Dry-run mode for testing
- Status monitoring command
- Comprehensive logging

### API Features
- RESTful endpoints with versioning (/api/v1)
- Automatic OpenAPI documentation (Swagger/ReDoc)
- Structured error responses with error codes
- Request/response validation with Pydantic
- CORS support for development

## Architecture

The application follows Clean Architecture with clear layer separation:
```
┌─────────────────────────────────────────────────┐
│              API Layer (FastAPI)                │
│    Controllers, Request/Response Schemas        │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│           Service Layer (Business Logic)        │
│    Validation, Business Rules, Coordination     │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         Repository Layer (Data Access)          │
│    SQLAlchemy ORM, Query Logic, Transactions    │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│          Database Layer (PostgreSQL)            │
│         Persistent Storage, Constraints         │
└─────────────────────────────────────────────────┘
```

### Architecture Benefits

1. **Dependency Inversion**: High-level modules independent of low-level details
2. **Testability**: Each layer can be tested in isolation
3. **Maintainability**: Changes localized to specific layers
4. **Extensibility**: New features added without modifying existing code
5. **Database Agnostic**: Repository pattern allows database changes without touching business logic

## Installation

### Prerequisites

- Python 3.14+
- Docker Desktop (for PostgreSQL)
- Poetry (recommended) or pip

### Setup Instructions

1. Clone the repository
```bash
   git clone https://github.com/ParsaNaderiX/todo-project.git
   cd todo-project
```

2. Set up virtual environment
```bash
   poetry install
   poetry shell
```

3. Configure environment variables
```bash
   cp .example.env .env
   # Edit .env with your database credentials
```

4. Start PostgreSQL
```bash
   docker-compose up -d
```

5. Run database migrations
```bash
   poetry run alembic upgrade head
```

### Environment Configuration

Required variables in `.env`:
```env
# Database connection
DATABASE_URL=postgresql://parsanaderi:password@localhost:5432/todo_db

# PostgreSQL credentials (for docker-compose)
POSTGRES_DB=todo_db
POSTGRES_USER=parsanaderi
POSTGRES_PASSWORD=your_secure_password

# Application limits
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50

# Scheduler configuration
SCHEDULER_INTERVAL_MINUTES=15
```

## Usage

### Running the API

Start the FastAPI server:
```bash
python run_api.py
```

Server will be available at:
- API Base: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### CLI (Deprecated)

The CLI is deprecated but still functional:
```bash
python -m app.cli
```

Warning: CLI will display deprecation notice directing users to the API.

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Project Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/projects` | Create project | 201, 400, 409 |
| GET | `/projects` | List projects | 200 |
| GET | `/projects/{id}` | Get project | 200, 404 |
| PUT | `/projects/{id}` | Update project | 200, 404, 409 |
| DELETE | `/projects/{id}` | Delete project | 204, 404 |

### Task Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/projects/{project_id}/tasks` | Create task | 201, 400, 404, 409 |
| GET | `/projects/{project_id}/tasks` | List tasks | 200, 404 |
| GET | `/projects/{project_id}/tasks/{task_id}` | Get task | 200, 404 |
| PUT | `/projects/{project_id}/tasks/{task_id}` | Update task | 200, 404, 409 |
| PATCH | `/projects/{project_id}/tasks/{task_id}/status` | Update status | 200, 404 |
| DELETE | `/projects/{project_id}/tasks/{task_id}` | Delete task | 204, 404 |

### Example Requests

Create a project:
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Website Redesign", "description": "Q4 website overhaul project"}'
```

Create a task:
```bash
curl -X POST http://localhost:8000/api/v1/projects/1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Design mockups",
    "description": "Create initial design mockups",
    "status": "todo",
    "deadline": "2025-12-31"
  }'
```

List projects with pagination:
```bash
curl "http://localhost:8000/api/v1/projects?skip=0&limit=10"
```

### Error Responses

All errors return structured JSON:
```json
{
  "detail": "Project with ID 999 not found.",
  "error_type": "ProjectNotFoundError"
}
```

Common error codes:
- `400`: Validation error, limit exceeded
- `404`: Resource not found
- `409`: Duplicate resource (name conflict)
- `500`: Internal server error

## Project Structure
```
todo-project/
├── app/
│   ├── api/                      # API Layer
│   │   ├── controllers/         # Endpoint handlers
│   │   ├── controller_schemas/  # Request/Response models
│   │   │   ├── requests/
│   │   │   └── responses/
│   │   └── routers.py          # Route registration
│   │
│   ├── services/                # Business Logic Layer
│   │   ├── todo_service.py     # Core business operations
│   │   ├── project_service.py  # Project-focused facade
│   │   └── task_service.py     # Task-focused facade
│   │
│   ├── repositories/            # Data Access Layer
│   │   ├── project_repository.py
│   │   └── task_repository.py
│   │
│   ├── models/                  # ORM Models
│   │   ├── project.py
│   │   └── task.py
│   │
│   ├── db/                      # Database Configuration
│   │   ├── base.py             # Declarative base
│   │   └── session.py          # Session management
│   │
│   ├── exceptions/              # Exception Hierarchy
│   │   ├── base.py
│   │   ├── repository_exceptions.py
│   │   └── service_exceptions.py
│   │
│   ├── core/                    # Domain Layer (Legacy)
│   │   ├── models.py           # Domain models (deprecated)
│   │   └── validation.py       # Validation functions
│   │
│   ├── cli/                     # CLI Interface (Deprecated)
│   │   ├── __main__.py
│   │   ├── menus.py
│   │   └── utils.py
│   │
│   ├── commands/                # Maintenance Scripts
│   │   ├── autoclose_overdue.py
│   │   ├── scheduler.py
│   │   └── status.py
│   │
│   ├── config/                  # Configuration
│   │   └── settings.py
│   │
│   └── main.py                  # FastAPI application
│
├── alembic/                     # Database Migrations
│   ├── versions/
│   └── env.py
│
├── postman/                     # API Testing
│   ├── postman_collection.json
│   └── postman_environment.json
│
├── docker-compose.yml           # PostgreSQL container
├── alembic.ini                  # Alembic configuration
├── pyproject.toml               # Python dependencies
└── README.md                    # This file
```

## Development Phases

### Phase 1: CLI Application (Complete)

**Goal**: Establish core architecture with working CLI interface.

**Implementation**:
- Command-line interface with menu-driven navigation
- In-memory storage implementation
- Service layer with business logic
- Validation framework
- Custom exception hierarchy

**Key Learnings**:
- Clean architecture principles
- Separation of concerns
- Port/Adapter pattern

### Phase 2: Database Integration (Complete)

**Goal**: Replace in-memory storage with persistent database.

**Implementation**:
- PostgreSQL database with Docker
- SQLAlchemy ORM models
- Repository pattern for data access
- Alembic migrations
- Database session management

**Key Changes**:
- Added `ProjectRepository` and `TaskRepository`
- Implemented ORM models (`Project`, `Task`)
- Created migration system
- Updated service layer to use repositories

**Key Learnings**:
- Repository pattern
- ORM relationships and constraints
- Database transaction management
- Migration strategies

### Phase 3: REST API (Complete)

**Goal**: Expose functionality via REST API.

**Implementation**:
- FastAPI framework
- Versioned API endpoints (/api/v1)
- Pydantic request/response schemas
- OpenAPI documentation
- Global exception handlers
- CORS configuration

**Key Changes**:
- Created API controllers
- Added Pydantic validation schemas
- Implemented dependency injection
- Added error response standardization

**Key Learnings**:
- RESTful API design
- Request/response validation
- API documentation
- Dependency injection patterns

### Phase 4: Testing & Maintenance (Complete)

**Goal**: Add automated testing capabilities and scheduled maintenance.

**Implementation**:
- Postman collection for API testing
- Automated overdue task closure
- Scheduler for periodic maintenance
- Status monitoring commands
- Comprehensive logging

**Key Changes**:
- Added `autoclose_overdue` command
- Implemented scheduler using Python Schedule
- Created Postman test suite
- Added `closed_at` field to tasks

**Key Learnings**:
- API testing strategies
- Scheduled job patterns
- Operational tooling
- Logging best practices

## Design Decisions

### 1. Repository Pattern Over Direct ORM Access

**Decision**: Use repository classes to encapsulate all database operations.

**Rationale**:
- Provides abstraction over data access
- Makes testing easier (repositories can be mocked)
- Isolates database changes from business logic
- Centralizes query logic and error handling

**Implementation**:
```python
class ProjectRepository:
    def create(self, name: str, description: str) -> Project:
        # Database-specific implementation
        pass
```

### 2. Facade Pattern for Service Layer

**Decision**: Provide `ProjectService` and `TaskService` facades over `TodoService`.

**Rationale**:
- Cleaner API for consumers
- Separates concerns (project vs task operations)
- Backwards compatibility with CLI
- Easier to understand for new developers

**Implementation**:
```python
class ProjectService:
    def __init__(self, project_repo, task_repo):
        self._service = TodoService(project_repo, task_repo)
    
    def create_project(self, name, description):
        return self._service.create_project(name, description)
```

### 3. Pydantic for API Validation

**Decision**: Use Pydantic models for request/response validation.

**Rationale**:
- Automatic validation and serialization
- Type safety
- Generates OpenAPI schema automatically
- Better error messages for API consumers

### 4. Integer IDs Over UUIDs

**Decision**: Use auto-incrementing integers for primary keys.

**Rationale**:
- Simpler for academic project
- Better query performance for small datasets
- Easier to work with in CLI/testing
- UUIDs can be added later if needed for distributed systems

### 5. Cascade Delete for Tasks

**Decision**: When a project is deleted, automatically delete all its tasks.

**Rationale**:
- Maintains data integrity
- Simpler than orphaned task handling
- Matches user expectation (project contains tasks)
- Configured at database level via foreign key

### 6. Status as String Instead of Enum

**Decision**: Store task status as string ("todo", "doing", "done") rather than enum.

**Rationale**:
- Simpler database schema
- Easier to extend with new statuses
- Validation handled at application level
- More flexible for future requirements

### 7. Deprecation of CLI

**Decision**: Mark CLI as deprecated after API implementation.

**Rationale**:
- API provides better integration capabilities
- Focuses development effort on modern interface
- Maintains CLI for backwards compatibility
- Encourages migration to API

## Database

### Schema

**Projects Table**:
```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Tasks Table**:
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'todo',
    deadline DATE,
    closed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, name)
);
```

### Migrations

Create new migration:
```bash
poetry run alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
poetry run alembic upgrade head
```

Rollback migration:
```bash
poetry run alembic downgrade -1
```

View migration history:
```bash
poetry run alembic history
```

### Database Management

Access PostgreSQL CLI:
```bash
docker-compose exec postgres psql -U parsanaderi -d todo_db
```

Common SQL commands:
```sql
-- List tables
\dt

-- Describe table structure
\d projects
\d tasks

-- View data
SELECT * FROM projects;
SELECT * FROM tasks WHERE status = 'todo';

-- Check overdue tasks
SELECT name, deadline, status FROM tasks 
WHERE deadline < CURRENT_DATE AND status != 'done';
```

## Maintenance

### Automatic Task Closure

Tasks with deadlines in the past are automatically closed by the scheduler.

Manual execution:
```bash
# Run immediately
poetry run python -m app.commands.autoclose_overdue

# Test without making changes
poetry run python -m app.commands.autoclose_overdue --dry-run
```

Check overdue status:
```bash
poetry run python -m app.commands.status
```

### Running the Scheduler

Development:
```bash
poetry run python -m app.commands.scheduler
```

Production (systemd service):
```ini
[Unit]
Description=Todo Scheduler
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

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now todo-scheduler
```

### Logging

Logs are written to `logs/scheduler.log` with timestamps:
```
[2025-12-09T10:00:00+00:00] Starting task scheduler...
[2025-12-09T10:00:00+00:00] Running scheduled job: autoclose_overdue_tasks
[2025-12-09T10:00:01+00:00] Closed task: Update documentation (Project: Website)
[2025-12-09T10:00:01+00:00] Job completed successfully
```

## Testing

### API Testing with Postman

1. Import collection and environment:
   - `postman/postman_collection.json`
   - `postman/postman_environment.json`

2. Set environment variable `base` to `http://localhost:8000`

3. Run requests in order:
   - Create Project
   - List Projects
   - Create Task
   - Update Task Status
   - Delete Task
   - Delete Project

### Manual Testing Workflow
```bash
# 1. Start services
docker-compose up -d
poetry run alembic upgrade head
python run_api.py

# 2. Create test data
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test project"}'

# 3. Verify data
curl http://localhost:8000/api/v1/projects

# 4. Cleanup
docker-compose down -v
```

## Troubleshooting

### Database Connection Errors
```bash
# Check if PostgreSQL is running
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Migration Issues
```bash
# Check current migration version
poetry run alembic current

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
poetry run alembic upgrade head
```

### API Not Starting
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i:8000)
```

## Version History

- **v0.3.0** - Phase 3: REST API with FastAPI
  - Added versioned API endpoints
  - Implemented Pydantic schemas
  - Global exception handling
  - OpenAPI documentation

- **v0.2.0** - Phase 2: Database Integration
  - PostgreSQL with Docker
  - Repository pattern
  - Alembic migrations
  - ORM models

- **v0.1.0** - Phase 1: CLI Application
  - Command-line interface
  - In-memory storage
  - Service layer
  - Clean architecture foundation

Last Updated: December 2025  
Current Version: v0.3.0  
Status: Complete