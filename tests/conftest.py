import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from src.models import Base
from app import app  # Tu FastAPI app
from src.database import get_db  # La dependencia de FastAPI para la DB

# ----------------------------
# Base de datos de test
# ----------------------------
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------------------
# Fixture para crear la base de datos
# ----------------------------
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    inspector = inspect(engine)
    print("Tablas antes de create_all:", inspector.get_table_names())

    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    print("Tablas después de create_all:", inspector.get_table_names())

    yield

    Base.metadata.drop_all(bind=engine)
    print("Tablas después de drop_all:", inspect(engine).get_table_names())

# ----------------------------
# Fixture para la sesión de DB
# ----------------------------
@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# ----------------------------
# Fixture para cliente FastAPI
# ----------------------------
from fastapi.testclient import TestClient

@pytest.fixture()
def client(db_session):
    # Sobrescribimos la dependencia get_db para usar la sesión de test
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
