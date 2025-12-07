from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# --------- User Schemas ---------
class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    full_name: Optional[str] = Field(None, example="Daniel Delgado")

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    full_name: str = Field(..., example="Daniel Delgado")
    password: str = Field(..., min_length=6, example="secret123")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=1, example="secret123")
    
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, example="Nuevo Nombre")
    password: Optional[str] = Field(None, min_length=6, example="newpassword123")

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# --------- Dashboard Schemas ---------
class DashboardBase(BaseModel):
    title: str = Field(..., example="Mi Tablero")
    description: Optional[str] = Field(None, example="Descripción del tablero")

class DashboardOut(DashboardBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
