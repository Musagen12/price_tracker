import uuid
from sqlalchemy import Column, Integer, String
from ..database import Base

class TrackedUrls(Base):
    __tablename__ = "tracked_urls"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID as string
    url = Column(String, nullable=False)





# asin: str
#     name: str
#     price: float
#     rating: float
#     in_stock: str
#     url: HttpUrl
#     image_url: HttpUrl