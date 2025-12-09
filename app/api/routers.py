"""API router registrations."""

from fastapi import APIRouter

from app.api.controllers import users_controller

# Main API router with shared prefix
api_router = APIRouter(prefix="/api/v1")

# Include project and task routers with distinct tags
api_router.include_router(users_controller.project_router, tags=["Projects"])
api_router.include_router(users_controller.task_router, tags=["Tasks"])

__all__ = ["api_router"]
