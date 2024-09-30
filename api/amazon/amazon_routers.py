from fastapi import APIRouter, HTTPException, Depends, status
import os
from pathlib import Path
from . import schemas, queries
from ..database import get_db
from sqlalchemy.orm import Session
from scrappers.amazon.comments import get_comments  
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

# @router.post("/get_comments", status_code=200)
# def get_amazon_comments(comment_input: schemas.CommentInput):
#     try:
#         comments = get_comments(url=str(comment_input.url))
#         file_name = comment_input.file_name

#         if comments is None or len(comments) == 0:
#             raise HTTPException(status_code=404, detail="No comments found for the provided URL.")

#         with open(file_name, "w") as file:
#             for comment in comments:
#                 file.write(comment + "\n")

#         return {"message": "Comments successfully written to file."}

#     except TypeError as e:
#         raise HTTPException(status_code=500, detail=f"Type error: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/get_comments", status_code=200)
def get_amazon_comments(comment_input: schemas.CommentInput):
    try:
        # Assuming get_comments fetches the comments from Amazon
        comments = get_comments(url=str(comment_input.url))
        file_name = comment_input.file_name

        if comments is None or len(comments) == 0:
            raise HTTPException(status_code=404, detail="No comments found for the provided URL.")

        # Define the folder path where the PDF will be saved
        folder_path = Path("./amazon_comments")

        # Create the folder if it doesn't exist
        folder_path.mkdir(parents=True, exist_ok=True)

        # Combine folder path and file name
        file_path = folder_path / file_name

        # Save the comments in a file within the amazon_comments folder
        with open(file_path, "w") as file:
            for comment in comments:
                file.write(comment + "\n")

        return {"message": "Comments successfully written to file.", "file_path": str(file_path)}

    except TypeError as e:
        raise HTTPException(status_code=500, detail=f"Type error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
