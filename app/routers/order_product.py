from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import OrderProductCreate, OrderProductSchema,OrderProductUpdate
from app.database import get_db
from sqlalchemy.orm import Session
from models import OrderProduct as OrderProductModel
from app.security import  TokenData, decode_access_token
import logging

router = APIRouter(prefix="/order_products", tags=["order_products"])

@router.get("/", response_model=List[OrderProductSchema])
def get_order_products(db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    order_products = db.query(OrderProductModel).all()
    return order_products

@router.post("/", response_model=OrderProductSchema, status_code=status.HTTP_201_CREATED, summary="Create a new order product", description="Creates a new order product in the database")
def create_order_product(order_product: OrderProductCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
     try:
       db_order_product = OrderProductModel(**order_product.model_dump())
       db.add(db_order_product)
       db.commit()
       db.refresh(db_order_product)
       return db_order_product
     except Exception as e:
       logging.error(f"Error creating order product: {e}", exc_info=True)
       raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{order_product_id}", response_model=OrderProductSchema, summary="Update an order product", description="Updates a specific order product based on its id.")
def update_order_product(order_product_id: str, order_product: OrderProductUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    try:
      db_order_product = db.query(OrderProductModel).filter(OrderProductModel.id == order_product_id).first()
      if not db_order_product:
           raise HTTPException(status_code=404, detail="Order Product not found")
      for key, value in order_product.model_dump(exclude_unset=True).items():
        setattr(db_order_product, key, value)
      db.add(db_order_product)
      db.commit()
      db.refresh(db_order_product)
      return db_order_product
    except Exception as e:
       logging.error(f"Error updating order product {order_product_id} : {e}", exc_info=True)
       raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/{order_product_id}", response_model=OrderProductSchema)
def get_order_product(order_product_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    order_product = db.query(OrderProductModel).filter(OrderProductModel.id == order_product_id).first()
    if not order_product:
        raise HTTPException(status_code=404, detail="Order Product not found")
    return order_product