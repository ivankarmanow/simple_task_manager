import datetime
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.sqlalchemy.models import Task
from app.main.di import create_session_maker
from app.main.web import app
from app.models import TaskStatus

Session = create_session_maker()
client = TestClient(app)


def create_test_task(pid: int | None = None) -> int:
    obj = {
        "title": "Test task 1",
        "description": "test description",
        "performers": "me",
        "own_plan_time": 100,
        "parent_id": pid
    }
    task = Task(**obj)
    with Session() as session:
        session.add(task)
        session.commit()
        return task.id


def delete_task(task_id: int) -> None:
    with Session() as session:
        session.delete(session.get(Task, task_id))
        session.commit()


def same_time(timestamp: str | datetime.datetime) -> bool:
    if isinstance(timestamp, str):
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
    return (datetime.datetime.now() - timestamp) < datetime.timedelta(minutes=1)


def transition(task_id: int, from_: TaskStatus, to: TaskStatus) -> tuple[bool, Task | None]:
    response = client.post("/task/status", json={
        "task_id": task_id,
        "status": to
    })
    data = response.json()
    if response.status_code == 200:
        assert data['status']
        with Session() as session:
            db_task = session.get(Task, task_id)
            assert db_task.status == to
        return True, db_task
    elif response.status_code == 400:
        assert not data['status']
        assert data['error']['task_id'] == task_id
        if data['error']['type'] == "InvalidStatusTransition":
            assert data['error']['transition']['from'] == from_
            assert data['error']['transition']['to'] == to
        return False, None
    else:
        assert False, f"Invalid response code: {response.status_code}"


@contextmanager
def TestTask(*args):
    pid = None
    if args:
        pid = args[0]
    task_id = create_test_task(pid)
    try:
        yield task_id
    finally:
        delete_task(task_id)


def test_create_task():
    create_obj = {
        "title": "Test task 1",
        "description": "test description",
        "performers": "me",
        "own_plan_time": 100
    }
    response = client.post("/task/create", json=create_obj)
    assert response.status_code == 201
    data = response.json()
    assert data['status']
    assert "task_id" in data
    assert isinstance(data['task_id'], int)
    with Session() as session:
        db_obj = session.get(Task, data['task_id'])
        assert db_obj
        assert db_obj.title == create_obj['title']
        assert db_obj.description == create_obj['description']
        assert db_obj.own_plan_time == create_obj['own_plan_time']
        assert db_obj.performers == create_obj['performers']
    delete_task(data['task_id'])


def test_delete_task():
    task_id = create_test_task()
    response = client.post("/task/delete", json={
        "id": task_id
    })
    assert response.status_code == 202
    data = response.json()
    assert data['status']
    with Session() as session:
        db_task = session.get(Task, task_id)
        assert db_task is None
    with TestTask() as task_id:
        with TestTask(task_id) as cht:
            response = client.post("/task/delete", json={
                "id": task_id
            })
            assert response.status_code == 400
            data = response.json()
            assert not data['status']
            assert data['error']['task_id'] == task_id
    response = client.post("/task/delete", json={
        "id": task_id
    })
    assert response.status_code == 404
    data = response.json()
    assert not data['status']
    assert data['error']['task_id'] == task_id


def test_list_tasks():
    with TestTask() as task_id:
        response = client.get("/task/list")
        data = response.json()
        assert response.status_code == 200
        assert "tasks" in data
        assert len(data['tasks']) > 0
        assert all(map(lambda x: x in data['tasks'][0], ("id", "title", "folder")))
        assert isinstance(data['tasks'][0]['id'], int)
        assert isinstance(data['tasks'][0]['title'], str)
        assert isinstance(data['tasks'][0]['folder'], bool)
        with Session() as session:
            db_tasks = session.execute(select(Task.id, Task.title).where(Task.parent_id is None)).all()
            api_tasks = {t['id']: t['title'] for t in data['tasks']}
            assert all(map(lambda x: x[0] in api_tasks and api_tasks[x[0]] == x[1], db_tasks))


def test_get_task():
    with TestTask() as task_id:
        response = client.get(f"/task/get/{task_id}")
        assert response.status_code == 200
        data = response.json()
        fields = (
            "id",
            "title",
            "description",
            "performers",
            "own_plan_time",
            "parent_id",
            "created_at",
            "status",
            "plan_time",
            "own_real_time",
            "real_time",
            "started_at",
            "completed_at",
            "last_paused_at",
            "pause_time"
        )
        assert all(map(lambda x: x in data, fields))
        assert data['id'] == task_id
        assert data['title'] == "Test task 1"
        assert data['description'] == "test description"
        assert data['performers'] == "me"
        assert data['own_plan_time'] == 100
        assert data['status'] == "assigned"
        assert data['plan_time'] == 100
        assert data['own_real_time'] is None
        assert data['real_time'] is None
        assert same_time(data['created_at'])
        with TestTask(task_id):
            response = client.get(f"/task/get/{task_id}")
            assert response.status_code == 200
            data = response.json()
            assert data['plan_time'] == 200
        # "2024-06-24T11:55:14.856811"
    response = client.get(f"/task/get/{task_id}")
    assert response.status_code == 404
    data = response.json()
    assert not data['status']
    assert data['error']['task_id'] == task_id


def test_update_task():
    with TestTask() as task_id:
        new_task_obj = {
            "title": "Test task 2",
            "description": "test description 2",
            "performers": "me2",
            "own_plan_time": 200
        }
        response = client.post("/task/update", json={"task_id": task_id, "task_input": new_task_obj})
        assert response.status_code == 202
        data = response.json()
        assert data['status']
        with Session() as session:
            db_task = session.get(Task, task_id)
            assert db_task
            assert db_task.title == new_task_obj['title']
            assert db_task.description == new_task_obj['description']
            assert db_task.performers == new_task_obj['performers']
            assert db_task.own_plan_time == new_task_obj['own_plan_time']
    response = client.post("/task/update", json={"task_id": task_id, "task_input": new_task_obj})
    assert response.status_code == 404
    data = response.json()
    assert not data['status']
    assert data['error']['task_id'] == task_id


def test_get_subtasks():
    with TestTask() as task_id:
        ids = [create_test_task(task_id) for i in range(5)]
        response = client.get(f"/task/subtasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert len(data['tasks']) > 0
        assert all(map(lambda x: x in data['tasks'][0], ("id", "title", "folder")))
        assert isinstance(data['tasks'][0]['id'], int)
        assert isinstance(data['tasks'][0]['title'], str)
        assert isinstance(data['tasks'][0]['folder'], bool)
        with Session() as session:
            db_tasks = session.execute(select(Task.id, Task.title).where(Task.parent_id == task_id)).all()
            api_tasks = {t['id']: t['title'] for t in data['tasks']}
            assert all(map(lambda x: x[0] in api_tasks and api_tasks[x[0]] == x[1], db_tasks))
        for i in ids:
            delete_task(i)


def test_status_transitions():
    with TestTask() as task_id:
        with Session() as session:
            db_task = session.get(Task, task_id)
            assert db_task.status == TaskStatus.ASSIGNED
            assert db_task.own_real_time is None
            assert db_task.started_at is None
            assert db_task.completed_at is None
            assert db_task.last_paused_at is None
            assert db_task.pause_time == 0
            current_status = TaskStatus.ASSIGNED
        assert not transition(task_id, current_status, TaskStatus.PAUSED)[0]
        assert not transition(task_id, current_status, TaskStatus.COMPLETED)[0]
        res, db_task = transition(task_id, current_status, TaskStatus.IN_PROGRESS)
        assert res
        assert same_time(db_task.started_at)
        current_status = TaskStatus.IN_PROGRESS
        assert not transition(task_id, current_status, TaskStatus.ASSIGNED)[0]
        res, db_task = transition(task_id, current_status, TaskStatus.PAUSED)
        assert res
        assert same_time(db_task.last_paused_at)
        current_status = TaskStatus.PAUSED
        assert not transition(task_id, current_status, TaskStatus.ASSIGNED)[0]
        res, db_task = transition(task_id, current_status, TaskStatus.IN_PROGRESS)
        assert res
        assert db_task.last_paused_at is None
        current_status = TaskStatus.IN_PROGRESS
        res, db_task = transition(task_id, current_status, TaskStatus.COMPLETED)
        assert res
        assert same_time(db_task.completed_at)
        assert db_task.own_real_time is not None
        current_status = TaskStatus.COMPLETED
        assert not transition(task_id, current_status, TaskStatus.ASSIGNED)[0]
        assert not transition(task_id, current_status, TaskStatus.PAUSED)[0]
        assert not transition(task_id, current_status, TaskStatus.IN_PROGRESS)[0]
    with TestTask() as task_id:
        assert transition(task_id, TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS)[0]
        with TestTask(task_id) as cht:
            assert not transition(task_id, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED)[0]
            assert transition(cht, TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS)[0]
            assert transition(task_id, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED)[0]


def test_time_calculations():
    with TestTask() as task_id:
        res, db_task = transition(task_id, TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS)
        assert res
        db_task.started_at = db_task.started_at - datetime.timedelta(hours=12, minutes=12)
        with Session() as session:
            session.add(db_task)
            session.commit()
        res, db_task = transition(task_id, TaskStatus.IN_PROGRESS, TaskStatus.PAUSED)
        assert res
        db_task.last_paused_at = db_task.last_paused_at - datetime.timedelta(hours=5, minutes=5)
        with Session() as session:
            session.add(db_task)
            session.commit()
        res, db_task = transition(task_id, TaskStatus.PAUSED, TaskStatus.IN_PROGRESS)
        assert res
        assert db_task.pause_time == 5
        res, db_task = transition(task_id, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED)
        assert res
        assert db_task.own_real_time == 7

