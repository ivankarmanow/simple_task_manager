from dataclasses import dataclass

from app.models import Task, TaskStub


@dataclass
class TaskList:
    tasks: list[TaskStub]


@dataclass
class DefaultResponse:
    status: bool = True


@dataclass
class TaskId:
    id: int


@dataclass
class TaskCreated:
    task_id: int
    status: bool = True
