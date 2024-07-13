from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import root_router
from .api.exception import invalid_status_transition_handler, task_not_found_handler,task_cannot_be_deleted_handler, task_cannot_be_completed
from app.exceptions import TaskNotFound, TaskCannotBeDeleted, InvalidStatusTransition, TaskCannotBeCompleted


def init_routers(app: FastAPI):
    app.include_router(root_router)
    app.add_exception_handler(TaskNotFound, task_not_found_handler)
    app.add_exception_handler(InvalidStatusTransition, invalid_status_transition_handler)
    app.add_exception_handler(TaskCannotBeDeleted, task_cannot_be_deleted_handler)
    app.add_exception_handler(TaskCannotBeCompleted, task_cannot_be_completed)
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=['*'],
    #     allow_credentials=True,
    #     allow_methods=['*'],
    #     allow_headers=['*'],
    # )

