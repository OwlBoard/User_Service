from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from sqlalchemy.orm import Session
from src import models, schemas
from src.database import get_db
import bcrypt
from src.models import User

router = APIRouter(tags=["Users"])

def get_password_hash(password: str) -> str:
    # Convert password to bytes and hash with bcrypt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert passwords to bytes for bcrypt verification
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# POST crear usuario
@router.post("/register")
def register(email: str = Form(...), password: str = Form(...), full_name: str = Form(None), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_password = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password, full_name=full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"Usuario {new_user.email} registrado con éxito", "id": new_user.id}

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"message": f"Bienvenido {user.full_name or user.email}", "id": user.id}

# GET todos los usuarios
@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# GET usuario por id
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# PUT actualizar usuario
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user.full_name:
        db_user.full_name = user.full_name
    if user.password:
        db_user.hashed_password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE /users/{user_id}?hard=<bool>
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, hard: bool = False, db: Session = Depends(get_db)):
    """
    Elimina un usuario.
    - Por defecto hace *soft delete* (marca is_active=False).
    - Si se llama con ?hard=true se borra físicamente de la tabla (hard delete).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if hard:
        db.delete(user)
        db.commit()
        # 204 No Content suele usarse para borrados, pero devolvemos 200/204 según preferencia.
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Soft delete
    if not user.is_active:
        # ya inactivo
        raise HTTPException(status_code=400, detail="User already inactive")
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": f"User {user.email} deactivated", "id": user.id}

# GET dashboards de usuario
@router.get("/{user_id}/dashboards", response_model=list[schemas.DashboardOut])
def get_user_dashboards(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user.dashboards
