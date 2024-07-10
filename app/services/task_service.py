import datetime

from app.exceptions import TaskCannotBeDeleted, TaskNotFound, InvalidStatusTransition, TaskCannotBeCompleted
from app.models import TaskInput, Task, TaskStatus, TaskStub
from app.protocols import DatabaseGateway
from app.protocols import UoW


class TaskService:
    def __init__(self, db_gateway: DatabaseGateway, uow: UoW):
        self.db = db_gateway
        self.uow = uow

    def create_task(self, task: TaskInput) -> int:
        id = self.db.add_task(task)
        self.uow.commit()
        return id

    def list_tasks(self) -> list[TaskStub]:
        return self.db.list_tasks()

    def delete_task(self, task_id: int) -> None:
        if self.db.get_task(task_id) is None:
            raise TaskNotFound(task_id)
        elif self.db.has_subtasks(task_id):
            raise TaskCannotBeDeleted(task_id)
        else:
            self.db.delete_task(task_id)
            self.uow.commit()

    def update_task(self, task_id: int, task: TaskInput) -> None:
        if self.db.get_task(task_id) is None:
            raise TaskNotFound(task_id)
        else:
            self.db.update_task(task_id, task)
            self.uow.commit()

    # def add_subtask(self, task_id: int, task: TaskInput) -> None:
    #     if self.db.get_task(task_id) is None:
    #         raise TaskNotFound()
    #     else:
    #         self.db.add_subtask(task_id, task)
    #         self.uow.commit()

    def get_task(self, task_id: int) -> Task:
        task = self.db.get_task(task_id)
        if task is None:
            raise TaskNotFound(task_id)
        else:
            if self.db.has_subtasks(task_id):
                for t in self.db.get_subtasks(task_id):
                    subta = self.db.get_task(t.id)
                    task.plan_time += subta.plan_time
                    if task.status == TaskStatus.COMPLETED and subta.status == TaskStatus.COMPLETED:
                            task.real_time += subta.real_time
            return task

    def get_subtasks(self, task_id: int) -> list[TaskStub]:
        if self.db.get_task(task_id) is None:
            raise TaskNotFound(task_id)
        else:
            return self.db.get_subtasks(task_id)

    def can_complete(self, task_id: int) -> bool:
        task = self.db.get_task(task_id)
        if task is None:
            return False
        if task.status == TaskStatus.ASSIGNED:
            return False
        subtasks = [subt.id for subt in self.db.get_subtasks(task_id)]
        if subtasks:
        # print(subtasks)
        # print(list(map(self.can_complete, subtasks)))
            return all(map(self.can_complete, subtasks))
        else:
            return True

    def set_status(self, task_id: int, status: TaskStatus) -> None:
        task = self.db.get_task(task_id)
        if task is None:
            raise TaskNotFound(task_id)
        else:
            def start(task: Task) -> None:
                task.started_at = datetime.datetime.now()
            def complete(task: Task) -> None:
                if not self.can_complete(task_id):
                    raise TaskCannotBeCompleted(task_id)
                task.completed_at = datetime.datetime.now()
                task.own_real_time = (datetime.datetime.now() - task.started_at).total_seconds() // 3600 - task.pause_time
                # print(task_id)
                for i in self.db.get_subtasks(task_id):
                    self.set_status(i.id, TaskStatus.COMPLETED)
            def pause(task: Task) -> None:
                task.last_paused_at = datetime.datetime.now()
            def unpause(task: Task) -> None:
                task.pause_time += (datetime.datetime.now() - task.last_paused_at).total_seconds() // 3600
                task.last_paused_at = None
            def complete_pause(task: Task) -> None:
                if not self.can_complete(task_id):
                    raise TaskCannotBeCompleted(task_id)
                unpause(task)
                complete(task)
            valid_transitions = {
                (TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS): start,
                (TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED): complete,
                (TaskStatus.IN_PROGRESS, TaskStatus.PAUSED): pause,
                (TaskStatus.PAUSED, TaskStatus.IN_PROGRESS): unpause,
                (TaskStatus.PAUSED, TaskStatus.COMPLETED): complete_pause,
            }
            transition = (task.status, status)
            if transition in valid_transitions:
                valid_transitions[transition](task)
                self.db.update_task(task_id, task)
                self.db.set_status(task_id, status)
                self.uow.commit()
            else:
                raise InvalidStatusTransition(transition)
