# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Deberías cargar esto desde tu config.py o variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@mysql_db/user_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de BD en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()