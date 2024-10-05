import os
import sqlite3
from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from typing import List
from pathlib import Path
from pydantic import BaseModel
from . import schemas, queries
from ..database import get_db
from sqlalchemy.orm import Session
from scrappers.amazon.comments import get_product_info_and_comments  
from scrappers.amazon.search import amazon_search
from .amazon_models import TrackedUrls

router = APIRouter(
    prefix="/amazon",
    tags=["Amazon"]
)


@router.post("/search", status_code=200)
def search(search_input: schemas.SearchInput):
    query = search_input.query
    product_list = amazon_search(query)
    return product_list


@router.post("/add_tracked_url", response_model=schemas.TrackedUrlResponse, status_code=201)
def add_tracked_url(url: schemas.TrackedUrlInput, db: Session = Depends(get_db)):
    tracked_url = queries.input_url(url, db)
    return tracked_url


@router.get("/get_tracked_url", status_code=200)
def get_tracked_url(db: Session = Depends(get_db)):
    tracked_urls = queries.get_list_of_tracked_urls(db)
    return tracked_urls

@router.delete("/remove_tracked_url/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tracked_url(id: str, db: Session = Depends(get_db)):
    url_query = db.query(TrackedUrls).filter(TrackedUrls.id == id)

    url_to_be_deleted = url_query.first()

    if url_to_be_deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"url with id: {id} does not exist")

    url_query.delete(synchronize_session=False)
    db.commit()

@router.post("/get_comments", status_code=200)
def get_amazon_comments(comment_input: schemas.CommentInput):
    try:
        # Fetch both comments and product description from the Amazon URL
        product_info = get_product_info_and_comments(url=str(comment_input.url))
        comments = product_info.get("comments", [])
        product_description = product_info.get("product_description", [])
        file_name = comment_input.file_name

        if not comments and not product_description:
            raise HTTPException(status_code=404, detail="No comments or product description found for the provided URL.")

        # Define the folder path where the file will be saved
        folder_path = Path("./amazon_comments")

        # Create the folder if it doesn't exist
        folder_path.mkdir(parents=True, exist_ok=True)

        # Combine folder path and file name
        file_path = folder_path / file_name

        # Save the comments and product description in a file
        with open(file_path, "w") as file:
            file.write("Product Description:\n")
            for description in product_description:
                file.write(description + "\n")
            
            file.write("\nComments:\n")
            for comment in comments:
                file.write(comment + "\n")

        return {"message": "Product description and comments successfully written to file.", "file_path": str(file_path)}

    except TypeError as e:
        raise HTTPException(status_code=500, detail=f"Type error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    rating: str
    in_stock: str
    image_source: str
    timestamp: datetime


class ProductDetailsResponse(BaseModel):
    in_stock: str
    price: float
    timestamp: datetime

class ProductDetailsResponseList(BaseModel):
    products: List[ProductDetailsResponse]

def connect_to_database(db_name):
    """Connect to the SQLite database."""
    return sqlite3.connect(db_name)

def create_cursor(connection):
    """Create a cursor object from the database connection."""
    return connection.cursor()

def execute_query(cursor, query, params=None):
    """Execute a given SQL query and return the results."""
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()  

def close_resources(cursor, connection):
    """Close the cursor and the database connection."""
    cursor.close()
    connection.close()

def get_first_complete_product(db_name, table_name):
    """Fetch the first product with all fields completely filled from the database."""
    query = """
        SELECT id, name, in_stock, rating, image_source, price, timestamp 
        FROM {} 
        WHERE id IS NOT NULL 
          AND name IS NOT NULL 
          AND name != '' 
          AND name != 'Name not found' 
          AND price IS NOT NULL 
        LIMIT 1;  -- Only get the first complete product
    """.format(table_name)  # Table names cannot be parameterized, so we format them.

    conn = connect_to_database(db_name)
    cursor = create_cursor(conn)
    try:
        result = execute_query(cursor, query)
    finally:
        close_resources(cursor, conn)
    
    return result

def quote_sql_identifier(identifier: str) -> str:
    """Safely quote an SQL identifier like a table name."""
    # Replace any existing backticks to avoid injection risks
    identifier = identifier.replace("`", "``")
    # Safely quote the table name with backticks
    return f'`{identifier}`'

@router.get("/frontend_data/{id}", response_model=ProductResponse)
def get_frontend_data(id: str):
    """Endpoint to get the first complete product from the specified table."""
    database_name = "hackathon.db"  # Specify your database name
    
    # Quote the table name to safely use it in the SQL query
    quoted_table_name = quote_sql_identifier(id)
    
    first_product = get_first_complete_product(database_name, quoted_table_name)
    
    if first_product:
        product = first_product[0]  #
        return ProductResponse(
            id=product[0],
            name=product[1],
            in_stock=product[2],
            rating=product[3],
            image_source=product[4],
            price=product[5],
            timestamp=product[6]
        )
    else:
        raise HTTPException(status_code=404, detail="No complete products found.")

def get_all_product_details(db_name, table_name):
    """Fetch all products' in_stock, price, and timestamp from the database."""
    query = f"""
    SELECT in_stock, price, timestamp 
    FROM {table_name}
    """
    
    conn = connect_to_database(db_name)
    cursor = create_cursor(conn)
    try:
        result = execute_query(cursor, query)
    finally:
        close_resources(cursor, conn)
    
    return result

@router.get("/graph_details/{id}", response_model=ProductDetailsResponseList)  # Change here
def get_graph_details_route(id: str):
    """Endpoint to get the in_stock, price, and timestamp of all complete products."""
    database_name = "hackathon.db"
    
    # Quote the table name to safely use it in the SQL query
    quoted_table_name = quote_sql_identifier(id)
    
    product_details_list = get_all_product_details(database_name, quoted_table_name)

    if product_details_list:
        products = [
            ProductDetailsResponse(
                in_stock=product[0],       
                price=product[1],          
                timestamp=product[2]
            )
            for product in product_details_list
        ]
        
        return ProductDetailsResponseList(products=products)  # Return the list here
    else:
        raise HTTPException(status_code=404, detail="No complete products found.")