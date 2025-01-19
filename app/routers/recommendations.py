from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import PurchaseCreate, PurchaseSchema, ProductSchema
from app.database import get_db
from sqlalchemy.orm import Session
from models import Purchase as PurchaseModel, Product as ProductModel
from collections import defaultdict
from app.security import decode_access_token, TokenData


router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("/purchases", response_model=PurchaseSchema, status_code=status.HTTP_201_CREATED)
def record_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db), current_user: 
                    TokenData = Depends(decode_access_token)):
  db_purchase = PurchaseModel(**purchase.model_dump())
  db.add(db_purchase)
  db.commit()
  db.refresh(db_purchase)
  return db_purchase

@router.get("/user/{user_id}", response_model=List[ProductSchema])
def get_recommendations_for_user(user_id: str, db: Session = Depends(get_db), current_user: 
  TokenData = Depends(decode_access_token)):
    purchases = db.query(PurchaseModel).filter(PurchaseModel.user_id == user_id).all()

    if not purchases:
        return []  
    product_counts = defaultdict(int)
    for purchase in purchases:
        product_counts[purchase.product_id] += 1

    top_product_ids = sorted(product_counts, key=product_counts.get, reverse=True)
    all_products = db.query(ProductModel).all()

    products_bought_ids = [purchase.product_id for purchase in purchases]
    available_products = [product for product in all_products if product.id not in products_bought_ids]
    if not available_products:
      return []
    return available_products[:3]