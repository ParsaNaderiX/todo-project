"""API router registrations."""

from fastapi import APIRouter

from app.api.controllers import users_controller

router = APIRouter()
router.include_router(users_controller.router)

__all__ = ["router"]
