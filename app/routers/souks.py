from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from models import Souk
from app.schemas import SoukCreate, SoukSchema
from app.security import decode_access_token, TokenData

router = APIRouter(prefix="/souks", tags=["Souks"])

@router.post("/", response_model=SoukSchema, status_code=status.HTTP_201_CREATED)
def create_souk(souk: SoukCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    db_souk = Souk(**souk.model_dump())
    db.add(db_souk)
    db.commit()
    db.refresh(db_souk)
    return db_souk


@router.get("/", response_model=List[SoukSchema])
def get_all_souks(db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    return db.query(Souk).all()


@router.get("/{souk_id}", response_model=SoukSchema)
def get_souk_by_id(souk_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    souk = db.query(Souk).filter(Souk.id == souk_id).first()
    if not souk:
        raise HTTPException(status_code=404, detail="Souk not found")
    return souk

@router.get("/name/{souk_name}", response_model=SoukSchema)
def get_souk_by_name(souk_name: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    souk = db.query(Souk).filter(Souk.name == souk_name).first()
    if not souk:
      raise HTTPException(status_code=404, detail="Souk not found")
    return souk
@router.delete("/{souk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_souk(souk_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    souk = db.query(Souk).filter(Souk.id == souk_id).first()
    if not souk:
        raise HTTPException(status_code=404, detail="Souk not found")
    db.delete(souk)
    db.commit()
    return None