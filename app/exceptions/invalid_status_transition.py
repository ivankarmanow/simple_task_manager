from app.models.status import TaskStatus


class InvalidStatusTransition(Exception):
    def __init__(self, task_id: int, transition: tuple[TaskStatus, TaskStatus]):
        self.task_id = task_id
        self.transition = transition

    def __str__(self):
        return f"Cannot change task {self.task_id} status from {self.transition[0]} to {self.transition[1]}"
