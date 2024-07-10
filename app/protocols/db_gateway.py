from abc import ABC, abstractmethod

from app.models import Task, TaskInput, TaskStub, TaskStatus


class DatabaseGateway(ABC):
    @abstractmethod
    def add_task(self, task: TaskInput) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task_id: int, task: Task) -> None:
        raise NotImplementedError

    # @abstractmethod
    # def add_subtask(self, task_id: int, task: TaskInput) -> None:
    #     raise NotImplementedError

    @abstractmethod
    def get_task(self, task_id: int) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def list_tasks(self) -> list[TaskStub]:
        raise NotImplementedError

    @abstractmethod
    def get_subtasks(self, task_id: int) -> list[TaskStub]:
        raise NotImplementedError

    @abstractmethod
    def has_subtasks(self, task_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def set_status(self, task_id: int, status: TaskStatus) -> None:
        raise NotImplementedError
