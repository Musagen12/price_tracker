from fastapi import Depends
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, inspect, DateTime
from sqlalchemy.ext.declarative import declarative_base
from scrappers.jumia.individual import get_individual_jumia_item  # Ensure this function is synchronous
from ..database import get_db
from .jumia_models import JumiaTrackedUrls
from .schemas import TrackedUrlInput

Base = declarative_base()
dynamic_tables = {}

def create_table_for_uuid(engine, uuid_str):
    """Dynamically create or retrieve a table using the provided UUID as the table name."""
    inspector = inspect(engine)

    if uuid_str in inspector.get_table_names():
        print(f"Table '{uuid_str}' already exists.")
        if uuid_str in dynamic_tables:
            return dynamic_tables[uuid_str]

        class _UUIDData(Base):
            __tablename__ = uuid_str

            id = Column(Integer, primary_key=True)
            name = Column(String)
            in_stock = Column(String)
            rating = Column(String)
            image_source = Column(String)
            price = Column(Float)
            timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

        dynamic_tables[uuid_str] = _UUIDData
        return _UUIDData
    else:
        print(f"Table '{uuid_str}' does not exist. Creating...")

        class _UUIDData(Base):
            __tablename__ = uuid_str

            id = Column(Integer, primary_key=True)
            name = Column(String)
            in_stock = Column(String)
            rating = Column(String)
            image_source = Column(String)
            price = Column(Float)
            timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

        dynamic_tables[uuid_str] = _UUIDData

        try:
            Base.metadata.create_all(engine)
            print(f"Table '{uuid_str}' created successfully.")
        except Exception as e:
            print(f"Error creating table '{uuid_str}': {str(e)}")
            return None

        return _UUIDData

def save_product_data(uuid_str: str, product_data: dict, db: Session):
    """Save product data to the dynamically created or retrieved table."""
    if not product_data:
        print(f"No product data to save for UUID '{uuid_str}'")
        return

    UUIDDataClass = create_table_for_uuid(db.bind, uuid_str)

    if UUIDDataClass is None:
        print(f"Error: Table class for UUID '{uuid_str}' could not be created.")
        return

    print(f"Saving product data for UUID '{uuid_str}': {product_data}")

    required_keys = ['name', 'in_stock', 'rating', 'image_url', 'price']
    if not all(key in product_data for key in required_keys):
        print(f"Missing keys in product data for UUID '{uuid_str}': {product_data}")
        return

    try:
        new_data = UUIDDataClass(
            name=product_data['name'],
            in_stock=product_data['in_stock'],
            rating=product_data['rating'],
            image_source=product_data['image_url'],
            price=product_data['price']
        )

        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        print(f"Saved data for UUID '{uuid_str}': {new_data}")
    except Exception as e:
        print(f"Error saving data for UUID '{uuid_str}': {str(e)}")
        db.rollback()

def process_url(url_entry, db: Session):
    """Process a single URL entry."""
    try:
        print(f"Processing URL: {url_entry.url}")
        product_data = get_individual_jumia_item(url=url_entry.url)
        print(f"Product data received: {product_data}")

        if product_data is None:
            print(f"Error: No product data returned for URL '{url_entry.url}'")
            return

        save_product_data(url_entry.id, product_data, db)

    except Exception as e:
        print(f"Error processing URL '{url_entry.url}': {str(e)}")

def automate_jumia(db: Session = Depends(get_db)):
    """Automate the scraping and saving of product data for tracked URLs."""
    urls = db.query(JumiaTrackedUrls).all()
    
    for url_entry in urls:
        process_url(url_entry, db)

def input_url(url_input: TrackedUrlInput, db: Session = Depends(get_db)):
    saved_url = JumiaTrackedUrls(url=str(url_input.url))  
    db.add(saved_url)
    db.commit()
    db.refresh(saved_url)
    return saved_url

def get_list_of_tracked_urls(db: Session = Depends(get_db)):
    urls = db.query(JumiaTrackedUrls).all()
    return urls
