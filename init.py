import uuid
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Vendor, Product, User, Review, OrderProduct, Base,Souk,Purchase
from app.config import Config


SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Load environment variables from .env file
load_dotenv()

def create_tables():
    """Creates the tables in the database using SQLAlchemy."""
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully!")

    except Exception as ex:
        print(f"Error creating tables using sqlalchemy: {ex}")


def seed_database():
    """Populates the database with initial data using SQLAlchemy."""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
         # Sample data (replace with your own)
         users = [
             User(id=str(uuid.uuid4()), email="ali@example.com", password="password123", name="Ali", role="vendor"),
             User(id=str(uuid.uuid4()), email="fatma@example.com", password="password456", name="Fatma", role="customer"),
             User(id=str(uuid.uuid4()), email="mohamed@example.com", password="password789", name="Mohamed", role="owner")
         ]
         session.add_all(users)
         session.commit()

         vendors = [
            Vendor(id=str(uuid.uuid4()), name="Ali", category="Perfumes", SoukName="Souk El Attarine,Medina Tunis",
                   profileImage="url_perfumes", phoneNumber="+21690******", email="ali@example.com",
                   openingHours="Mon-Fri 9am-5pm", wholesaleOptions="Available", retailOptions="Available",
                   facebookUrl="https://facebook.com/page"
                   ),
            Vendor(id=str(uuid.uuid4()), name="Chaker", category="Fabrics", SoukName="Souk des Étoffes",
                   profileImage="url_fabrics", phoneNumber="098-765-4321", email="chaker@example.com",
                   openingHours="Mon-Sat 10am-7pm", wholesaleOptions="Not Available", retailOptions="Available",
                    facebookUrl="https://facebook.com/updatedpage"
                    )
         ]
         session.add_all(vendors)
         session.commit()

         products = [
            Product(id=str(uuid.uuid4()), vendor_id=vendors[0].id, name="Kaftan", description="Description",
                    price=100.00, quantityAvailable=100, images="https://example.com/product.jpg",
                    category="Clothing", discounts="10% off"),
            Product(id=str(uuid.uuid4()), vendor_id=vendors[1].id, name="Tapis", description="Description2",
                    price=50.00, quantityAvailable=100, images="https://example.com/product2.jpg",
                    category="Tapis", discounts="50% off")
         ]
         session.add_all(products)
         session.commit()

         reviews = [
            Review(id=str(uuid.uuid4()), vendor_id=vendors[0].id, user_id = users[0].id, rating=5,
                   review_text="Great quality"),
             Review(id=str(uuid.uuid4()), vendor_id=vendors[1].id, user_id= users[1].id, rating=4,
                    review_text="Good quality")
         ]
         session.add_all(reviews)
         session.commit()


         order_products = [
            OrderProduct(id=str(uuid.uuid4()), product_id=products[0].id,
                         quantity=2, unit_price=100.00, payment_method="credit card", amount=200.0),
            OrderProduct(id=str(uuid.uuid4()), product_id=products[1].id,
                          quantity=1, unit_price=50.00, payment_method="credit card", amount=50.0)
         ]
         session.add_all(order_products)
         session.commit()
         souks = [
            Souk(id=str(uuid.uuid4()), name="Souk El Attarine", location="Medina Tunis", description = "Perfumes and traditional products"),
            Souk(id=str(uuid.uuid4()), name="Souk des Étoffes", location="Medina Tunis", description = "Traditional Fabric souk"),
            Souk(id=str(uuid.uuid4()), name="Souk El Berka", location="Medina Tunis", description = "Jewelry and gold souk"),
            Souk(id=str(uuid.uuid4()), name="Souk El Jedid", location="Medina Tunis", description = "Traditional clothes and shoes")
        ]
         session.add_all(souks)
         session.commit()
         purchases = [
            Purchase(id=str(uuid.uuid4()), user_id=users[1].id, product_id=products[0].id), # user fatma bought kaftan
            Purchase(id=str(uuid.uuid4()), user_id=users[1].id, product_id=products[1].id), # user fatma bought tapis
            Purchase(id=str(uuid.uuid4()), user_id=users[2].id, product_id=products[0].id), # user mohamed bought kaftan
            ]
         session.add_all(purchases)
         session.commit()


         print("Database seeded successfully!")
         return True
    except Exception as ex:
        session.rollback()
        print(f"Error seeding the database using sqlalchemy: {ex}")
        return False
    finally:
        session.close()

def init_db():
    create_tables()
    seed_database()

if __name__ == "__main__":
    init_db()