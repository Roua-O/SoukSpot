from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from uuid import uuid4
from app.config import Config
import logging
import os
import sys
import datetime

SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_database():
    """Populates the database with initial data using SQLAlchemy."""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        from models import Vendor, Product, User, Review, OrderProduct, Souk,Purchase
        users = [
            User(id=str(uuid4()), email="ali@example.com", password="password123", name="Ali", role="vendor"),
            User(id=str(uuid4()), email="fatma@example.com", password="password456", name="Fatma", role="customer"),
            User(id=str(uuid4()), email="mohamed@example.com", password="password789", name="Mohamed", role="owner")
        ]
        session.add_all(users)
        session.commit()

        vendors = [
            Vendor(id=str(uuid4()), name="Ali", category="Perfumes", SoukName="Souk El Attarine,Medina Tunis",
                   profileImage="url_perfumes", phoneNumber="+21690******", email="ali@example.com",
                   openingHours="Mon-Fri 9am-5pm", wholesaleOptions="Available", retailOptions="Available",
                   facebookUrl="https://facebook.com/page"
                   ),
            Vendor(id=str(uuid4()), name="Chaker", category="Fabrics", SoukName="Souk des Étoffes",
                   profileImage="url_fabrics", phoneNumber="098-765-4321", email="chaker@example.com",
                   openingHours="Mon-Sat 10am-7pm", wholesaleOptions="Not Available", retailOptions="Available",
                    facebookUrl="https://facebook.com/updatedpage"
                    )
         ]
        session.add_all(vendors)
        session.commit()

        products = [
            Product(id=str(uuid4()), vendor_id=vendors[0].id, name="Kaftan", description="Description",
                    price=100.00, quantityAvailable=100, images="https://example.com/product.jpg",
                    category="Clothing", discounts="10% off"),
            Product(id=str(uuid4()), vendor_id=vendors[1].id, name="Tapis", description="Description2",
                    price=50.00, quantityAvailable=100, images="https://example.com/product2.jpg",
                    category="Tapis", discounts="50% off")
         ]
        session.add_all(products)
        session.commit()

        reviews = [
             Review(id=str(uuid4()), vendor_id=vendors[0].id, user_id = users[0].id, rating=5,
                   review_text="Great quality"),
             Review(id=str(uuid4()), vendor_id=vendors[1].id, user_id = users[1].id, rating=4,
                    review_text="Good quality")
         ]
        session.add_all(reviews)
        session.commit()

        order_products = [
            OrderProduct(id=str(uuid4()), product_id=products[0].id,
                         quantity=2, unit_price=100.00, payment_method="credit card", amount=200.0,shipping_address="sousse"),
            OrderProduct(id=str(uuid4()), product_id=products[1].id,
                          quantity=1, unit_price=50.00, payment_method="credit card", amount=50.0,hipping_address="tunis")
         ]
        session.add_all(order_products)
        session.commit()
        logging.info(f"Added order products: {[order_product.id for order_product in order_products]}")
        souks = [
            Souk(id=str(uuid4()), name="Souk El Attarine", location="Medina Tunis", description = "Perfumes and traditional products"),
            Souk(id=str(uuid4()), name="Souk des Étoffes", location="Medina Tunis", description = "Traditional Fabric souk"),
             Souk(id=str(uuid4()), name="Souk El Berka", location="Medina Tunis", description = "Jewelry and gold souk"),
            Souk(id=str(uuid4()), name="Souk El Jedid", location="Medina Tunis", description = "Traditional clothes and shoes")
        ]
        session.add_all(souks)
        session.commit()
        purchases = [
        Purchase(id=str(uuid4()), user_id=users[1].id, product_id=products[0].id), # user fatma bought kaftan
        Purchase(id=str(uuid4()), user_id=users[1].id, product_id=products[1].id), # user fatma bought tapis
        Purchase(id=str(uuid4()), user_id=users[2].id, product_id=products[0].id), # user mohamed bought kaftan
            ]
        session.add_all(purchases)
        session.commit()
        
        return True #success
    except Exception as e:
      print(f"Error seeding the database: {e}")
      return False #failed
    finally:
        session.close()