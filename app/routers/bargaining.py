from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import  BargainingSchema
from app.database import get_db
from sqlalchemy.orm import Session
from models import Vendor, User, BargainingSession 
from app.security import decode_access_token, TokenData

router = APIRouter(prefix="/bargaining", tags=["Bargaining"])

@router.post("/offer/{vendor_id}", response_model=BargainingSchema, status_code=status.HTTP_201_CREATED)
def make_offer(vendor_id: str, offer: BargainingSchema, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
          raise HTTPException(status_code=404, detail="Vendor not found")
    buyer = db.query(User).filter(User.email == current_user.username).first()
    if not buyer:
          raise HTTPException(status_code=404, detail="Buyer not found")
    
    db_bargain = db.query(BargainingSession).filter(BargainingSession.vendor_id == vendor_id, BargainingSession.buyer_id == current_user.username).first()

    if not db_bargain:
        db_bargain = BargainingSession(vendor_id=vendor_id, buyer_id = current_user.username, price = offer.price, type = "offer")
        db.add(db_bargain)
    else:
       db_bargain.price = offer.price
       db_bargain.type = "offer"
    db.commit()
    db.refresh(db_bargain)
    return db_bargain

@router.get("/status/{vendor_id}", response_model=BargainingSchema)
def get_bargaining_status(vendor_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    db_bargain = db.query(BargainingSession).filter(BargainingSession.vendor_id == vendor_id, BargainingSession.buyer_id == current_user.username).first()
    if not db_bargain:
       raise HTTPException(status_code=404, detail="Bargaining session not found")
    return db_bargain

@router.post("/accept/{vendor_id}", response_model=BargainingSchema, status_code=status.HTTP_201_CREATED)
def accept_offer(vendor_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
      vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
      if not vendor:
          raise HTTPException(status_code=404, detail="Vendor not found")
      if vendor.email != current_user.username:
         raise HTTPException(status_code=401, detail="Not authorized to accept this offer")
      
      db_bargain = db.query(BargainingSession).filter(BargainingSession.vendor_id == vendor_id, BargainingSession.buyer_id == current_user.username).first()
      if not db_bargain:
           raise HTTPException(status_code=404, detail="Bargaining session not found")

      db_bargain.type = "accept"
      db.commit()
      db.refresh(db_bargain)
      return db_bargain