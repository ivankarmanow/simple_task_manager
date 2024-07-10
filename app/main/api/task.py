from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, APIRouter, Body, status, HTTPException

from app.models import Task, TaskInput, TaskStatus
from app.protocols import Stub
from app.services import TaskService
from .responses import TaskList, DefaultResponse, TaskId, TaskCreated

task_router = APIRouter(prefix="/task")


@task_router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    summary="Get list of all root tasks"
)
async def list_tasks(
        service: Annotated[TaskService, Depends(Stub(TaskService))]
) -> TaskList:
    return TaskList(tasks=service.list_tasks())


@task_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create new task"
)
async def create_task(
        service: Annotated[TaskService, Depends(Stub(TaskService))],
        task: TaskInput
) -> TaskCreated:
    id = service.create_task(task)
    return TaskCreated(task_id=id)


@task_router.post(
    "/delete",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete task by id"
)
async def delete_task(
        service: Annotated[TaskService, Depends(Stub(TaskService))],
        task_id: TaskId,
) -> DefaultResponse:
    service.delete_task(task_id.id)
    return DefaultResponse()


@task_router.post(
    "/update",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update task by id"
)
async def update_task(
        service: Annotated[TaskService, Depends(Stub(TaskService))],
        task_id: Annotated[int, Body()],
        task_input: TaskInput
) -> DefaultResponse:
    service.update_task(task_id, task_input)
    return DefaultResponse()


@task_router.get(
    "/get/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Get task by id"
)
async def get_task(
        service: Annotated[TaskService, Depends(Stub(TaskService))],
        task_id: int
) -> Task | DefaultResponse:
    task = service.get_task(task_id)
    return task


@task_router.get(
    "/subtasks/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Get all subtasks of a task by id"
)
async def get_subtask(
        service: Annotated[TaskService, Depends(Stub(TaskService))],
        task_id: int
) -> TaskList | DefaultResponse:
    return TaskList(tasks=service.get_subtasks(task_id))


@task_router.post(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Set task status"
)
async def set_task_status(
        service: Annotated[TaskService, Depends(Stub(TaskService))],
        task_id: Annotated[int, Body()],
        status: Annotated[TaskStatus, Body()]
) -> DefaultResponse:
    service.set_status(task_id, status)
    return DefaultResponse()