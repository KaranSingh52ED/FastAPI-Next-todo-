from fastapi.testclient import TestClient
from fastapi import FastAPI
from todo_app import setting
from sqlmodel import SQLModel, create_engine, Session
from todo_app.main import app, get_session
import pytest

connection_string: str = str(setting.TEST_DATABASE_URI).replace(
    "postgresql", "postgresql+psycopg"
)


# engine is one for whole application
engine = create_engine(
    connection_string,
    connect_args={"sslmode": "require"},
    pool_recycle=300,
    pool_size=10,
    echo=True,
)


# ========================================================================================
# Refactor with pytest fixture
# 1- Arrange, 2-Act, 3-Assert 4- Cleanup


@pytest.fixture(scope="module", autouse=True)
def get_db_session():
    SQLModel.metadata.create_all(engine)
    yield Session(engine)


@pytest.fixture(scope="function")
def test_app(get_db_session):
    def test_session():
        yield get_db_session

    app.dependency_overrides[get_session] = test_session
    with TestClient(app=app) as client:
        yield client


# ========================================================================================


# test-1 :root Test
def test_root():
    client = TestClient(app=app)
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert data == {"message": "Welcome to todo-app"}


# test-2:post test


def test_create_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:

    #     def db_session_overide():
    #         return session

    # app.dependency_overrides[get_session] = db_session_overide
    # client = TestClient(app=app)
    test_todo = {"content": "create todo test", "is_completed": False}
    response = test_app.post("/todos/", json=test_todo)
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == test_todo["content"]


# test-3: get_all
def test_get_all(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:

    #     def db_session_overide():
    #         return session

    # app.dependency_overrides[get_session] = db_session_overide
    # client = TestClient(app=app)
    test_todo = {"content": "get all todos test", "is_completed": False}
    response = test_app.post("/todos/", json=test_todo)
    data = response.json()
    response = test_app.get("/todos/")
    all_todos = response.json()
    new_todo = all_todos[-1]
    assert response.status_code == 200
    assert new_todo["content"] == test_todo["content"]


# test-4: Single Todo
def test_get_single_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:

    #     def db_session_overide():
    #         return session

    # app.dependency_overrides[get_session] = db_session_overide
    # client = TestClient(app=app)

    test_todo = {"content": "get single todos test", "is_completed": False}
    response = test_app.post("/todos/", json=test_todo)
    todo_id = response.json()["id"]
    res = test_app.get(f"/todos/{todo_id}")
    data = res.json()
    assert res.status_code == 200
    assert data["content"] == test_todo["content"]


# test-5:Edit Todo
def test_edit_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:

    #     def db_session_overide():
    #         return session

    # app.dependency_overrides[get_session] = db_session_overide
    # client = TestClient(app=app)

    test_todo = {"content": "Edit todo test", "is_completed": False}
    response = test_app.post("/todos/", json=test_todo)
    todo_id = response.json()["id"]

    edited_todo = {"content": "We have edited this", "is_completed": True}
    res = test_app.put(f"/todos/{todo_id}", json=edited_todo)
    assert res.status_code == 200

    data = res.json()
    assert data["content"] == edited_todo["content"]
    assert data["is_completed"] == edited_todo["is_completed"]


# test-6: delete todo
def test_delete_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:

    #     def db_session_overide():
    #         return session

    # app.dependency_overrides[get_session] = db_session_overide
    # client = TestClient(app=app)

    test_todo = {"content": "Edit todo test", "is_completed": False}
    response = test_app.post("/todos/", json=test_todo)
    todo_id = response.json()["id"]

    response = test_app.delete(f"/todos/{todo_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Task Successfully Deleted!"
