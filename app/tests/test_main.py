import datetime
import json

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.sqlalchemy.models import Task
from app.main.di import create_session_maker
from app.main.web import create_app

app = create_app()
Session = create_session_maker()
client = TestClient(app)


def create_test_task(pid: int | None = None) -> int:
    obj = {
        "title": "Test task 1",
        "description": "test description",
        "performers": "me",
        "own_plan_time": 100
    }
    if pid:
        obj['parent_id'] = pid
    response = client.post("/task/create", json=obj)
    return response.json().get('task_id')


def delete_task(task_id: int) -> bool:
    response = client.post("/task/delete", json={
        "id": task_id
    })
    return response.json().get("status")


class TestTask:
    def __enter__(self):
        self.task_id = create_test_task()
        return self.task_id

    def __exit__(self, exc_type, exc_val, exc_tb):
        delete_task(self.task_id)


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
    task_id = create_test_task()
    cht = create_test_task(task_id)
    response = client.post("/task/delete", json={
        "id": task_id
    })
    assert response.status_code == 400
    data = response.json()
    assert not data['status']
    assert data['error']['task_id'] == task_id
    delete_task(cht)
    delete_task(task_id)
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
        print(f"/task/get/{task_id}")
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
        assert (datetime.datetime.now() - datetime.datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%S.%f")) < datetime.timedelta(minutes=1)
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

# def test_set_status():
#     with TestTask() as task_id:
#         response = client.post("/task/status", json=json.dumps())
