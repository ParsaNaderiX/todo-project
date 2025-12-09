"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import api_router
from app.api.controller_schemas.responses.users_response_schema import ErrorResponse
from app.db.session import engine
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

app = FastAPI(
    title="ToDoList API",
    version="3.0.0",
    description="RESTful API for ToDoList project management",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Development CORS (allow all)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    # Eagerly verify DB connectivity on startup
    conn = None
    try:
        conn = engine.connect()
    finally:
        if conn is not None:
            conn.close()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    # Dispose engine connections
    engine.dispose()


@app.exception_handler(ValidationError)
async def handle_validation_error(request: Request, exc: ValidationError) -> JSONResponse:  # noqa: ARG001
    payload = ErrorResponse(detail=str(exc), error_type=exc.__class__.__name__)
    return JSONResponse(status_code=400, content=payload.model_dump())


@app.exception_handler(ProjectNotFoundError)
@app.exception_handler(TaskNotFoundError)
async def handle_not_found(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    payload = ErrorResponse(detail=str(exc), error_type=exc.__class__.__name__)
    return JSONResponse(status_code=404, content=payload.model_dump())


@app.exception_handler(DuplicateProjectError)
@app.exception_handler(DuplicateTaskError)
async def handle_conflict(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    payload = ErrorResponse(detail=str(exc), error_type=exc.__class__.__name__)
    return JSONResponse(status_code=409, content=payload.model_dump())


@app.exception_handler(ProjectLimitError)
@app.exception_handler(TaskLimitError)
async def handle_limit(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    payload = ErrorResponse(detail=str(exc), error_type=exc.__class__.__name__)
    return JSONResponse(status_code=400, content=payload.model_dump())


@app.exception_handler(DatabaseOperationError)
async def handle_db_error(request: Request, exc: DatabaseOperationError) -> JSONResponse:  # noqa: ARG001
    payload = ErrorResponse(detail=str(exc), error_type=exc.__class__.__name__)
    return JSONResponse(status_code=500, content=payload.model_dump())


@app.get("/", summary="API Info")
async def root() -> dict:
    return {
        "name": "ToDoList API",
        "version": "3.0.0",
        "description": "RESTful API for ToDoList project management",
        "deprecated": "CLI is deprecated; use API endpoints under /api/v1",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# Register versioned API router
app.include_router(api_router)


__all__ = ["app"]
