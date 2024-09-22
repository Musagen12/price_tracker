from pydantic import BaseModel, HttpUrl
from typing import List

class Product(BaseModel):
    asin: str
    name: str
    price: float
    rating: float
    url: HttpUrl
    image_url: HttpUrl
    in_stock: str

class ProductList(BaseModel):
    products: List[Product]