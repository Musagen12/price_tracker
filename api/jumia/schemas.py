from pydantic import BaseModel, HttpUrl, field_validator, ValidationError
from typing import List, Optional

class CommentInput(BaseModel):
    url: HttpUrl
    file_name: str

    @field_validator('file_name')
    def check_pdf_extension(cls, value):
        if not value.endswith('.txt'):
            raise ValueError("File must have a .txt extension")
        return value

class SearchInput(BaseModel):
    query: str

class TrackedUrlInput(BaseModel):
    url: HttpUrl

class TrackedUrlResponse(BaseModel):
    id: str
    url: HttpUrl

    class Config:
        from_attributes = True


class Product(BaseModel):
    name: str
    price: str  
    rating: str
    in_stock: str
    image_url: HttpUrl
    url: Optional[HttpUrl] = None
    unique_code: str

class ProductList(BaseModel):
    products: List[Product]