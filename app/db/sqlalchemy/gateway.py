from dataclasses import asdict

from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from app.models import TaskInput, Task as TaskDataclass, TaskStub, TaskStatus
from app.protocols import DatabaseGateway
from .models import Task


class SqlaGateway(DatabaseGateway):

    def __init__(self, session: Session):
        self.session = session

    def add_task(self, task: TaskInput) -> int:
        task = Task(**asdict(task))
        self.session.add(task)
        self.session.commit()
        return task.id

    def delete_task(self, task_id: int) -> None:
        self.session.delete(self.session.get(Task, task_id))

    def update_task(self, task_id: int, task: TaskInput) -> None:
        old_task = self.session.get(Task, task_id)
        for key, value in asdict(task).items():
            setattr(old_task, key, value)
        # self.session.add(old_task)

    # def add_subtask(self, task_id: int, task: TaskInput) -> None:
    #     subtask = Task(**asdict(cast(task, dataclasses.dataclass)))
    #     self.session.get(Task, task_id).children.append(subtask)

    def get_task(self, task_id: int) -> TaskDataclass | None:
        task = self.session.get(Task, task_id)
        if task:
            return TaskDataclass(**task.__dict__, plan_time = task.own_plan_time, real_time=task.own_real_time)

    def list_tasks(self) -> list[TaskStub]:
        tasks = self.session.execute(select(Task.id, Task.title).where(Task.parent_id == None)).all()
        # print(tasks)
        res = list()
        for task in tasks:
            res.append(TaskStub(id=task[0], title=task[1], folder=self.has_subtasks(task[0])))
        return res

    def get_subtasks(self, task_id: int) -> list[TaskStub]:
        subtasks = self.session.execute(select(Task.id, Task.title).where(Task.parent_id == task_id))
        res = list()
        for subt in subtasks:
            res.append(TaskStub(id=subt.id, title=subt.title, folder=self.has_subtasks(subt.id)))
        return res

    def has_subtasks(self, task_id: int) -> bool:
        return self.session.scalar(exists().where(Task.parent_id == task_id).select())

    def set_status(self, task_id: int, status: TaskStatus) -> None:
        # task = self.session.get(Task, task_id)
        # task.status = status
        # self.session.add(task)
        self.session.get(Task, task_id).status = status

