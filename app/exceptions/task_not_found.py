class TaskNotFound(Exception):

    def __init__(self, task_id: int):
        self.task_id = task_id

    def __str__(self):
        return f"Task {self.task_id} not found"
