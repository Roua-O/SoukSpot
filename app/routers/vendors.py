from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from models import Vendor
from app.schemas import VendorCreate, VendorSchema
from app.security import decode_access_token, TokenData


router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.post("/", response_model=VendorSchema, status_code=status.HTTP_201_CREATED)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db), current_user:
                   TokenData = Depends(decode_access_token)):
    db_vendor = Vendor(**vendor.model_dump())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

@router.get("/", response_model=List[VendorSchema])
def get_all_vendors(db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    return db.query(Vendor).all()

@router.get("/category/{category}", response_model=List[VendorSchema])
def get_vendor_by_category(category: str, db: Session = Depends(get_db), current_user: 
                           TokenData = Depends(decode_access_token)):
    vendors = db.query(Vendor).filter(Vendor.category == category).all()
    if not vendors:
        raise HTTPException(status_code=404, detail="Vendor not found in this category")
    return vendors

@router.get("/{vendor_id}", response_model=VendorSchema)
def get_vendor_by_id(vendor_id: str, db: Session = Depends(get_db), current_user:
                      TokenData = Depends(decode_access_token)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

@router.get("/souk/{souk_name}", response_model=List[VendorSchema])
def get_vendor_by_soukname(souk_name: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    vendors = db.query(Vendor).filter(Vendor.SoukName == souk_name).all()
    if not vendors:
        raise HTTPException(status_code=404, detail="Vendor not found in this Souk")
    return vendors

@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(vendor_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(vendor)
    db.commit()
    return None