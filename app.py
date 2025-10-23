# src/app.py
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware # No longer needed
from src.models import Base
from src.database import engine
from src.routes.users_routes import router as user_router

app = FastAPI(
    title="User Service API",
    description="API for user management and authentication",
    version="1.0.0"
)

# CORS is now handled by the NGINX gateway
# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "http://localhost:8080",
# ]
# 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# Create tables on startup
Base.metadata.create_all(bind=engine)

# Registrar rutas
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "User Service API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-service"}

if __name__ == "__main__":
    import uvicorn
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)