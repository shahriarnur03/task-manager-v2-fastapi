from fastapi import APIRouter

from src.api.routers.task_route import router as task_router

api_router = APIRouter()

api_router.include_router(task_router)