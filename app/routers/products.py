from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import ProductCreate, ProductSchema
from app.database import get_db
from sqlalchemy.orm import Session
from models import Product as ProductModel
from app.security import decode_access_token, TokenData

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    products = db.query(ProductModel).all()
    return products

@router.get("/category/{category}", response_model=List[ProductSchema])
def get_products_by_category(category: str, db: Session = Depends(get_db), current_user: 
                             TokenData = Depends(decode_access_token)):
    products = db.query(ProductModel).filter(ProductModel.category == category).all()
    return products

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user:
                    TokenData = Depends(decode_access_token)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.get("/name/{product_name}", response_model=List[ProductSchema])
def get_products_by_name(product_name: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    products = db.query(ProductModel).filter(ProductModel.name == product_name).all()
    return products


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return None