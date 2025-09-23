# tests/test_routes.py
import pytest
from fastapi.testclient import TestClient
from app import app  # Asegúrate de importar tu app FastAPI correctamente
from src.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base

# --- Setup DB para tests ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # SQLite temporal
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# --- Fixture de db para tests ---
@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()

# --- Fixture cliente FastAPI ---
@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

# --- Tests POST /users/register ---
def test_register_user_success(client):
    response = client.post("/users/register", params={"email": "test1@example.com", "password": "123456", "full_name": "Test One"})
    assert response.status_code == 200
    assert "Usuario test1@example.com registrado con éxito" in response.json()["message"]

def test_register_user_existing_email(client):
    client.post("/users/register", params={"email": "test2@example.com", "password": "abc123", "full_name": "Test Two"})
    response = client.post("/users/register", params={"email": "test2@example.com", "password": "abc123", "full_name": "Test Two"})
    assert response.status_code == 400
    assert response.json()["detail"] == "El usuario ya existe"

# --- Tests POST /users/login ---
def test_login_success(client):
    client.post("/users/register", params={"email": "login@example.com", "password": "pass123", "full_name": "Login User"})
    response = client.post("/users/login", params={"email": "login@example.com", "password": "pass123"})
    assert response.status_code == 200
    assert "Bienvenido" in response.json()["message"]

def test_login_wrong_password(client):
    client.post("/users/register", params={"email": "wrongpass@example.com", "password": "rightpass", "full_name": "Wrong Pass"})
    response = client.post("/users/login", params={"email": "wrongpass@example.com", "password": "wrongpass"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Contraseña incorrecta"

def test_login_user_not_found(client):
    response = client.post("/users/login", params={"email": "nonexistent@example.com", "password": "any"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Usuario no encontrado"

# --- Tests GET /users y /users/{id} ---
def test_get_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_by_id(client):
    r = client.post("/users/register", params={"email": "getuser@example.com", "password": "pass", "full_name": "Get User"})
    user_id = r.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "getuser@example.com"

def test_get_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

# --- Tests PUT /users/{id} ---
def test_update_user(client):
    r = client.post("/users/register", params={"email": "update@example.com", "password": "pass", "full_name": "Old Name"})
    user_id = r.json()["id"]
    response = client.put(f"/users/{user_id}", json={"full_name": "New Name"})
    assert response.status_code == 200
    assert response.json()["full_name"] == "New Name"

def test_update_user_not_found(client):
    response = client.put("/users/9999", json={"full_name": "No User"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

# --- Tests DELETE /users/{id} ---
def test_delete_user_soft(client):
    r = client.post("/users/register", params={"email": "softdelete@example.com", "password": "pass", "full_name": "Soft Delete"})
    user_id = r.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert "deactivated" in response.json()["message"]

def test_delete_user_hard(client):
    r = client.post("/users/register", params={"email": "harddelete@example.com", "password": "pass", "full_name": "Hard Delete"})
    user_id = r.json()["id"]
    response = client.delete(f"/users/{user_id}?hard=true")
    assert response.status_code == 204

def test_delete_user_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
