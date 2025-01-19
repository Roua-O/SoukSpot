from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime
from sqlalchemy.sql import func


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    purchases = relationship("Purchase", back_populates="user")

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    SoukName = Column(String, nullable=False)
    profileImage = Column(String, nullable=True)
    phoneNumber = Column(String, nullable=False)
    email = Column(String, nullable=False)
    openingHours = Column(String, nullable=True)
    wholesaleOptions = Column(String, nullable=True)
    retailOptions = Column(String, nullable=True)
    facebookUrl = Column(String, nullable=True)

    products = relationship("Product", back_populates="vendor")
    reviews = relationship("Review", back_populates="vendor")

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantityAvailable = Column(Integer, nullable=False)
    images = Column(String, nullable=True)
    category = Column(String, nullable=True)
    discounts = Column(String, nullable=True)

    vendor = relationship("Vendor", back_populates="products")
    order_products = relationship("OrderProduct", back_populates="product")
    purchases = relationship("Purchase", back_populates="product")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    vendor = relationship("Vendor", back_populates="reviews")


class OrderProduct(Base):
    __tablename__ = "order_products"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    product = relationship("Product", back_populates="order_products")

class Souk(Base):
    __tablename__ = "souks"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=True)

class Purchase(Base): 
    __tablename__ = "purchases"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="purchases") 
    product = relationship("Product", back_populates="purchases") 

class BargainingSession(Base):
   __tablename__ = "bargaining_sessions"
   id= Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
   vendor_id = Column(String, ForeignKey("vendors.id"))
   buyer_id = Column(String, ForeignKey("users.email"))
   price = Column(Float)
   type = Column(String)
   vendor = relationship("Vendor", backref="bargaining_sessions")
   User = relationship("User", backref="bargaining_sessions")
