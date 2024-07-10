from datetime import datetime

from pydantic.dataclasses import dataclass

from .status import TaskStatus


@dataclass(kw_only=True)
class TaskInput:
    title: str
    description: str
    performers: str
    own_plan_time: int
    parent_id: int | None = None


@dataclass(kw_only=True)
class Task(TaskInput):
    id: int
    created_at: datetime
    status: TaskStatus
    plan_time: int
    own_real_time: int | None = None
    real_time: int | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    last_paused_at: datetime | None = None
    pause_time: int | None = None


@dataclass
class TaskStub:
    id: int
    title: str
    folder: bool
