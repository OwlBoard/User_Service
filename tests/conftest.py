# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database import get_db
from src.models import Base
from src.models import User  # <-- ESTA LÍNEA ES CRUCIAL

# --- Configuración de la Base de Datos de Prueba ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Sobrescritura de la Dependencia `get_db` ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# --- Creación de un Cliente de Prueba ---
@pytest.fixture(scope="function")
def client():
    # Esta línea ahora funcionará porque la importación de 'User'
    # aseguró que Base.metadata conozca la tabla 'users'.
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)