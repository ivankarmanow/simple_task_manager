from app.models.status import TaskStatus


class InvalidStatusTransition(Exception):
    def __init__(self, transition: tuple[TaskStatus, TaskStatus]):
        self.transition = transition

    def __str__(self):
        return f"Cannot change task status from {self.transition[0]} to {self.transition[1]}"
