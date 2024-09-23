from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .amazon_models import TrackedUrls
from .schemas import TrackedUrlInput

def input_url(url_input: TrackedUrlInput, db: Session = Depends(get_db)):
    saved_url = TrackedUrls(url=str(url_input.url))  # Use url_input.url
    db.add(saved_url)
    db.commit()
    db.refresh(saved_url)
    return saved_url