from os import environ
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = environ.get('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    """
    Данная функция при тестах будет подменять функцию get_db() в main.py.
    Таким образом приложение будет подключаться к тестовой базе данных.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению


def test_create_bank():
    response = client.post(
        "/bank/",
        json={"name": "test", "address": "test 1"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "test"


def test_create_client():
    response = client.post(
        "/users/?bank_id=1",
        json={
            "card_code": "test",
            "second_name": "test",
            "name": "test",
            "patronymic": "test",
            "address": "test",
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["second_name"] == "test"


def test_create_exist_client():
    response = client.post(
        "/users/?bank_id=1",
        json={
            "card_code": "test",
            "second_name": "test",
            "name": "test",
            "patronymic": "test",
            "address": "test",
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Client already registered"


def test_create_not_bank_client():
    response = client.post(
        "/users/?bank_id=124",
        json={
            "card_code": "test21",
            "second_name": "test",
            "name": "test",
            "patronymic": "test",
            "address": "test",
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Bank not found"


def test_create_atm():
    response = client.post(
        "/atm/?bank_id=1",
        json={
            "address": "test",
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["address"] == "test"


def test_create_not_bank_atm():
    response = client.post(
        "/atm/?bank_id=124",
        json={
            "address": "test",
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Bank not found"


def test_create_operation():
    response = client.post(
        "/operation/?client_id=1&atm_id=1",
        json={
            "date": "2022-12-07T08:23:26.046Z",
            "commission": True,
            "amount": 10
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["amount"] == 10


def test_create_bad_user_operation():
    response = client.post(
        "/operation/?client_id=125&atm_id=1",
        json={
            "date": "2022-12-07T08:23:26.046Z",
            "commission": True,
            "amount": 10
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_create_bad_atm_operation():
    response = client.post(
        "/operation/?client_id=1&atm_id=156",
        json={
            "date": "2022-12-07T08:23:26.046Z",
            "commission": True,
            "amount": 10
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "ATM not found"


def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["second_name"] == "test"
    assert data["card_code"] == "test"
    assert data["address"] == "test"


def test_get_not_exist_user():
    response = client.get("/users/156")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Client not found"


def test_get_bank():
    response = client.get("/banks/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "test"
    assert data["address"] == "test 1"


def test_get_not_exist_bank():
    response = client.get("/banks/156")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Bank not found"


def test_get_atm():
    response = client.get("/atms/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["address"] == "test"


def test_get_not_exist_atm():
    response = client.get("/atms/156")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "ATM not found"


def test_get_operations_by_client():
    response = client.get("/client_operation/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["commission"]
    assert data[0]["amount"] == 10


def test_get_operations_by_atm():
    response = client.get("/atm_operation/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["commission"]
    assert data[0]["amount"] == 10


def test_get_operation():
    response = client.get("/operation/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["commission"]
    assert data["amount"] == 10


def test_get_not_exist_operation():
    response = client.get("/operation/156")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Operation not found"
