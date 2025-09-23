# src/app.py
from fastapi import FastAPI
from src.models import Base
from src.database import engine
from src.routes.users_routes import router as user_router

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar rutas
app.include_router(user_router, prefix="/users", tags=["Users"])
