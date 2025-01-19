from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import ReviewCreate, ReviewSchema
from app.database import get_db
from sqlalchemy.orm import Session
from models import Review as ReviewModel
from app.security import decode_access_token, TokenData


router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/", response_model=List[ReviewSchema])
def get_reviews(db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    reviews = db.query(ReviewModel).all()
    return reviews

@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    db_review = ReviewModel(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/{review_id}", response_model=ReviewSchema)
def get_review(review_id: str, db: Session = Depends(get_db), current_user: TokenData = Depends(decode_access_token)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

