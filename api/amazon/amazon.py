from fastapi import APIRouter, HTTPException, Depends
from . import schemas, queries
from ..database import get_db
from sqlalchemy.orm import Session
from api.scrappers.amazon.comments import get_comments  
from api.scrappers.amazon.search import amazon_search

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


@router.post("/get_comments", status_code=200)
def get_amazon_comments(comment_input: schemas.CommentInput):
    try:
        comments = get_comments(url=str(comment_input.url))
        file_name = comment_input.file_name

        if comments is None or len(comments) == 0:
            raise HTTPException(status_code=404, detail="No comments found for the provided URL.")

        with open(file_name, "w") as file:
            for comment in comments:
                file.write(comment + "\n")

        return {"message": "Comments successfully written to file."}

    except TypeError as e:
        raise HTTPException(status_code=500, detail=f"Type error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
