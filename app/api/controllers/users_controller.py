"""FastAPI controllers for project and task endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.controller_schemas.requests.users_request_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    TaskCreateRequest,
    TaskStatusUpdateRequest,
    TaskUpdateRequest,
)
from app.api.controller_schemas.responses.users_response_schema import (
    ErrorResponse,
    ProjectListResponse,
    ProjectResponse,
    ProjectSummary,
    TaskResponse,
)
from app.db.session import get_db
from app.exceptions import (
    DatabaseOperationError,
    DuplicateProjectError,
    DuplicateTaskError,
    ProjectLimitError,
    ProjectNotFoundError,
    TaskLimitError,
    TaskNotFoundError,
    ValidationError,
)
from app.repositories import ProjectRepository, TaskRepository
from app.services import TodoService

# Separate routers so main configuration can tag them independently
project_router = APIRouter()
task_router = APIRouter()


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    """Provide a TodoService with repository dependencies."""
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return TodoService(project_repo, task_repo)


def _error_response(exc: Exception, default_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> JSONResponse:
    """Translate service/repository exceptions into HTTP responses."""
    status_code = default_status
    if isinstance(exc, (ValidationError, ProjectLimitError, TaskLimitError)):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, (DuplicateProjectError, DuplicateTaskError)):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(exc, (ProjectNotFoundError, TaskNotFoundError)):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, DatabaseOperationError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    payload = ErrorResponse(detail=str(exc), error_type=exc.__class__.__name__)
    return JSONResponse(status_code=status_code, content=payload.model_dump())


@project_router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a project with a name and optional description.",
)
async def create_project(
    request: ProjectCreateRequest,
    service: TodoService = Depends(get_todo_service),
):
    try:
        project = service.create_project(request.name, request.description or "")
        return ProjectResponse.model_validate(project)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@project_router.get(
    "/projects",
    response_model=ProjectListResponse,
    summary="List projects",
    description="List all projects with optional pagination.",
)
async def list_projects(
    skip: int = 0,
    limit: Optional[int] = None,
    service: TodoService = Depends(get_todo_service),
):
    try:
        projects = service.list_projects()
        sliced = projects[skip:] if skip else projects
        if limit is not None:
            sliced = sliced[:limit]
        summaries: List[ProjectSummary] = []
        for proj in sliced:
            summaries.append(
                ProjectSummary(
                    name=proj.name,
                    description=proj.description,
                    task_count=len(getattr(proj, "tasks", []) or []),
                )
            )
        return ProjectListResponse(projects=summaries)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@project_router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project",
    description="Retrieve a single project by its ID.",
)
async def get_project(
    project_id: int,
    service: TodoService = Depends(get_todo_service),
):
    try:
        project = service.get_project(project_id)
        return ProjectResponse.model_validate(project)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@project_router.put(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
    description="Update project name and description.",
)
async def update_project(
    project_id: int,
    request: ProjectUpdateRequest,
    service: TodoService = Depends(get_todo_service),
):
    try:
        existing = service.get_project(project_id)
        new_name = request.new_name or existing.name
        new_description = request.new_description or existing.description or ""
        project = service.edit_project(project_id, new_name, new_description)
        return ProjectResponse.model_validate(project)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@project_router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Delete a project",
    description="Delete a project by ID.",
)
async def delete_project(
    project_id: int,
    service: TodoService = Depends(get_todo_service),
):
    try:
        service.delete_project(project_id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@task_router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Create a new task within a project.",
)
async def create_task(
    project_id: int,
    request: TaskCreateRequest,
    service: TodoService = Depends(get_todo_service),
):
    try:
        deadline_str = request.deadline.isoformat() if request.deadline else None
        task = service.create_task(
            project_id,
            request.name,
            request.description or "",
            request.status,
            deadline_str,
        )
        return TaskResponse.model_validate(task)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@task_router.get(
    "/projects/{project_id}/tasks",
    response_model=List[TaskResponse],
    summary="List tasks in a project",
    description="List all tasks belonging to a project.",
)
async def list_tasks(
    project_id: int,
    service: TodoService = Depends(get_todo_service),
):
    try:
        tasks = service.list_tasks(project_id)
        return [TaskResponse.model_validate(t) for t in tasks]
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@task_router.get(
    "/projects/{project_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a task",
    description="Retrieve a task within a project.",
)
async def get_task(
    project_id: int,
    task_id: int,
    service: TodoService = Depends(get_todo_service),
):
    try:
        task = service.get_task(project_id, task_id)
        return TaskResponse.model_validate(task)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@task_router.put(
    "/projects/{project_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update task fields (name, description, status, deadline).",
)
async def update_task(
    project_id: int,
    task_id: int,
    request: TaskUpdateRequest,
    service: TodoService = Depends(get_todo_service),
):
    try:
        existing = service.get_task(project_id, task_id)
        new_name = request.name or existing.name
        new_description = request.description or existing.description or ""
        new_status = request.status or existing.status
        deadline_str = request.deadline.isoformat() if request.deadline else (
            existing.deadline.isoformat() if existing.deadline else None
        )

        task = service.edit_task(
            project_id,
            task_id,
            new_name,
            new_description,
            new_status,
            deadline_str,
        )
        return TaskResponse.model_validate(task)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@task_router.patch(
    "/projects/{project_id}/tasks/{task_id}/status",
    response_model=TaskResponse,
    summary="Update task status",
    description="Update only the status field of a task.",
)
async def update_task_status(
    project_id: int,
    task_id: int,
    request: TaskStatusUpdateRequest,
    service: TodoService = Depends(get_todo_service),
):
    try:
        task = service.edit_task_status(project_id, task_id, request.status)
        return TaskResponse.model_validate(task)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)


@task_router.delete(
    "/projects/{project_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Delete a task",
    description="Delete a task from a project.",
)
async def delete_task(
    project_id: int,
    task_id: int,
    service: TodoService = Depends(get_todo_service),
):
    try:
        service.delete_task(project_id, task_id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    except Exception as exc:  # noqa: BLE001
        return _error_response(exc)
