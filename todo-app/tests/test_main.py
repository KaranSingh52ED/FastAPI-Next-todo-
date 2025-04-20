from fastapi.testclient import TestClient

from fastapi import FastAPI
from todo_app import setting
from sqlmodel import SQLModel, create_engine, Session
from todo_app.main import app, get_session

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


# test-1 :root Test
def test_root():
    client = TestClient(app=app)
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert data == {"message": "Welcome to todo-app"}


# test-2:post test


def test_create_todo():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:

        def db_session_overide():
            return session

    app.dependency_overrides[get_session] = db_session_overide
    client = TestClient(app=app)
    test_todo = {"content": "create todo test", "is_completed": False}
    response = client.post("/todos/", json=test_todo)
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == test_todo["content"]


# test-3: get_all
def test_get_all():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:

        def db_session_overide():
            return session

    app.dependency_overrides[get_session] = db_session_overide
    client = TestClient(app=app)
    test_todo = {"content": "get all todos test", "is_completed": False}
    response = client.post("/todos/", json=test_todo)
    data = response.json()

    response = client.get("/todos/")
    new_todo = response.json[-1]
    assert response.status_code == 200
    assert new_todo["content"] == test_todo["content"]
