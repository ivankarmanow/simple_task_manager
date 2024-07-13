from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions import TaskNotFound, TaskCannotBeDeleted, InvalidStatusTransition, TaskCannotBeCompleted


async def task_not_found_handler(request: Request, e: TaskNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": False,
            "error": {
                "type": e.__class__.__name__,
                "task_id": e.task_id,
                "text": str(e),
            }
        }
    )


async def task_cannot_be_deleted_handler(request: Request, e: TaskCannotBeDeleted) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": False,
            "error": {
                "type": e.__class__.__name__,
                "task_id": e.task_id,
                "text": str(e),
            }
        }
    )

async def task_cannot_be_completed(request: Request, e: TaskCannotBeCompleted) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": False,
            "error": {
                "type": e.__class__.__name__,
                "task_id": e.task_id,
                "text": str(e)
            }
        }
    )

async def invalid_status_transition_handler(request: Request, e: InvalidStatusTransition) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": False,
            "error": {
                "type": e.__class__.__name__,
                "task_id": e.task_id,
                "transition": {
                    "from": e.transition[0],
                    "to": e.transition[1],
                },
                "text": str(e)
            }
        }
    )