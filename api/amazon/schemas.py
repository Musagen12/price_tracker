from pydantic import BaseModel, HttpUrl, validator, ValidationError
from typing import List

class CommentInput(BaseModel):
    url: HttpUrl
    file_name: str

    @validator('file_name')
    def check_pdf_extension(cls, value):
        if not value.endswith('.pdf'):
            raise ValueError("File must have a .pdf extension")
        return value

class SearchInput(BaseModel):
    query: str

class Product(BaseModel):
    asin: str
    name: str
    price: float
    rating: str
    in_stock: str
    url: HttpUrl
    image_url: HttpUrl

class ProductList(BaseModel):
    products: List[Product]