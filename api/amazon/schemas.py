from pydantic import BaseModel, HttpUrl
from typing import List

class Product(BaseModel):
    asin: str
    name: str
    price: float
    rating: float
    in_stock: str
    url: HttpUrl
    image_url: HttpUrl

class ProductList(BaseModel):
    products: List[Product]