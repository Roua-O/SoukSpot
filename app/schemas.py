from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime


class TokenData(BaseModel):
  username: str = None
  
class UserBase(BaseModel):
    email: str
    name: str
    role: str

class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: str

class UserLogin(BaseModel):
    email: str
    password: str

class Config:
    from_attribute = True  

class ProductRecommendationSchema(BaseModel):
    product_id: str
    product_name: str

    class Config:
        from_attribute = True  

class ProductRecommendationResponseSchema(BaseModel):
    user_id: str
    recommended_products: List[ProductRecommendationSchema]
    
class VendorBase(BaseModel):
    name: str
    category: str
    SoukName: str
    profileImage: Optional[str] = None
    phoneNumber: str
    email: str
    openingHours: Optional[str] = None
    wholesaleOptions: Optional[str] = None
    retailOptions: Optional[str] = None
    facebookUrl: Optional[str] = None

class VendorCreate(VendorBase):
    pass


class VendorSchema(VendorBase):
    id: str

    class Config:
        from_attributes = True
        
class BargainingSchema(BaseModel):
    id: Optional[str] = None
    type: str
    price: Optional[float] = None


class ProductBase(BaseModel):
    vendor_id: str
    name: str
    description: Optional[str] = None
    price: float
    quantityAvailable: int
    images: Optional[str] = None
    category: Optional[str] = None
    discounts: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductSchema(ProductBase):
    id: str


    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    vendor_id: str
    user_id: str
    rating: int
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass

class ReviewSchema(ReviewBase):
   id: str
   created_at: Optional[datetime] = None

   class Config:
       from_attributes = True


   class Config:
       from_attributes = True


class OrderProductBase(BaseModel):
  product_id: str
  quantity: int
  unit_price: float
  payment_method: str
  amount: float

class OrderProductCreate(OrderProductBase):
    pass

class OrderProductSchema(OrderProductBase):
  id: str

  class Config:
     from_attributes = True

class OrderProductUpdate(OrderProductBase):
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    payment_method: Optional[str] = None
    amount: Optional[float] = None
  
class SoukBase(BaseModel):
  name: str
  location: str
  description: Optional[str] = None

class SoukCreate(SoukBase):
    pass

class SoukSchema(SoukBase):
    id: str

    class Config:
        from_attributes = True
class PurchaseCreate(BaseModel):
  user_id: str
  product_id: str

class PurchaseSchema(BaseModel):
  id: str
  user_id: str
  product_id: str
  purchase_date: datetime

  class Config:
    orm_mode = True