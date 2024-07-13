from fastapi import APIRouter

from app.main.api.task import task_router

root_router = APIRouter()
root_router.include_router(task_router)
