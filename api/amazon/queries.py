from fastapi import Depends
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, inspect, DateTime
from sqlalchemy.ext.declarative import declarative_base
from scrappers.amazon.individual import get_individual_amazon_item
from ..database import get_db
from .amazon_models import TrackedUrls
from .schemas import TrackedUrlInput

Base = declarative_base()
dynamic_tables = {}  # Store dynamically created table classes

def create_table_for_uuid(engine, uuid_str):
    """Dynamically create or retrieve a table using the provided UUID as the table name."""
    inspector = inspect(engine)

    # Check if the table already exists
    if uuid_str in inspector.get_table_names():
        print(f"Table '{uuid_str}' already exists.")
        # Check if we've already created the class for this table
        if uuid_str in dynamic_tables:
            return dynamic_tables[uuid_str]  # Return the existing class
        
        # If not, we recreate the class mapping for this table
        class _UUIDData(Base):
            __tablename__ = uuid_str

            id = Column(Integer, primary_key=True)
            name = Column(String)
            in_stock = Column(String)
            rating = Column(String)
            image_source = Column(String)
            price = Column(Float)
            timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

        dynamic_tables[uuid_str] = _UUIDData  # Store the class
        return _UUIDData  # Return the class
    else:
        # Create a new table if it doesn't exist
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

        dynamic_tables[uuid_str] = _UUIDData  # Store the class

        # Create the table
        try:
            Base.metadata.create_all(engine)
            print(f"Table '{uuid_str}' created successfully.")
        except Exception as e:
            print(f"Error creating table '{uuid_str}': {str(e)}")
            return None  # Return None on failure

        return _UUIDData  # Return the class

def save_product_data(uuid_str: str, product_data: dict, db: Session = Depends(get_db)):
    """Save product data to the dynamically created or retrieved table."""
    UUIDDataClass = create_table_for_uuid(db.bind, uuid_str)

    if UUIDDataClass is None:
        print(f"Error: Table class for UUID '{uuid_str}' could not be created.")
        return

    # Debugging: Print product_data to see its content
    print(f"Saving product data for UUID '{uuid_str}': {product_data}")

    required_keys = ['Product Name', 'In Stock', 'Rating', 'Image Source', 'Price']
    if not all(key in product_data for key in required_keys):
        print(f"Missing keys in product data for UUID '{uuid_str}': {product_data}")
        return  # Skip this entry or handle the error as needed

    try:
        # Insert data into the dynamically created or retrieved table
        new_data = UUIDDataClass(
            name=product_data['Product Name'],
            in_stock=product_data['In Stock'],
            rating=product_data['Rating'],
            image_source=product_data['Image Source'],
            price=product_data['Price']
        )

        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        print(f"Saved data for UUID '{uuid_str}': {new_data}")
    except Exception as e:
        print(f"Error saving data for UUID '{uuid_str}': {str(e)}")
        db.rollback()


def input_url(url_input: TrackedUrlInput, db: Session = Depends(get_db)):
    saved_url = TrackedUrls(url=str(url_input.url))  # Use url_input.url
    db.add(saved_url)
    db.commit()
    db.refresh(saved_url)
    return saved_url


def get_list_of_tracked_urls(db: Session = Depends(get_db)):
    urls = db.query(TrackedUrls).all()
    return urls


def automate(db: Session = Depends(get_db)):
    """Automate the scraping and saving of product data for tracked URLs."""
    urls = db.query(TrackedUrls).all()

    for url_entry in urls:
        try:
            print(f"Processing URL: {url_entry.url}")
            product_data = get_individual_amazon_item(url=url_entry.url)
            print(f"Product data received: {product_data}")

            if product_data is None:
                print(f"Error: No product data returned for URL '{url_entry.url}'")
                continue

            save_product_data(url_entry.id, product_data, db)

        except Exception as e:
            print(f"Error processing URL '{url_entry.url}': {str(e)}")



# celery -A scheduler.celery.celery_app beat --loglevel=info
# celery -A scheduler.celery.celery_app worker --loglevel=info