from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import UserCreate, UserSchema, UserLogin
from app.database import get_db
from sqlalchemy.orm import Session
from models import User as UserModel
import bcrypt
from app.security import create_access_token, TokenData
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = UserModel(
        email=user.email,
        name=user.name,
        role=user.role,
        password=hashed_password.decode('utf-8')  
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=15))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user