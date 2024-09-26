from fastapi import APIRouter, HTTPException, Depends, status
from . import schemas, queries
from ..database import get_db
from sqlalchemy.orm import Session
from scrappers.jumia.comments import get_jumia_comments  
from scrappers.jumia.search import jumia_search
from .jumia_models import JumiaTrackedUrls

router = APIRouter(
    prefix="/jumia",
    tags=["Jumia"]
)


@router.post("/search", status_code=200)
def search(search_input: schemas.SearchInput):
    query = search_input.query
    product_list = jumia_search(query)
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
    url_query = db.query(JumiaTrackedUrls).filter(JumiaTrackedUrls.id == id)

    url_to_be_deleted = url_query.first()

    if url_to_be_deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"url with id: {id} does not exist")

    url_query.delete(synchronize_session=False)
    db.commit()

@router.post("/get_comments", status_code=200)
def get_all_jumia_comments(comment_input: schemas.CommentInput):
    try:
        # Fetch the comments using the scraper
        comments = get_jumia_comments(url=str(comment_input.url))
        file_name = comment_input.file_name

        if comments is None or len(comments) == 0:
            raise HTTPException(status_code=404, detail="No comments found for the provided URL.")

        # Write the comments into a file
        with open(file_name, "w", encoding="utf-8") as file:  # Ensure correct encoding
            for comment in comments:
                if isinstance(comment, dict):  # If comment is a dictionary
                    formatted_comment = ", ".join(f"{key}: {value}" for key, value in comment.items())  # Format dict
                elif isinstance(comment, tuple):  # If comment is a tuple
                    formatted_comment = " | ".join(str(item) for item in comment)  # Join tuple elements
                else:  # If comment is something else (string, etc.)
                    formatted_comment = str(comment)

                file.write(formatted_comment + "\n")  # Write each formatted comment on a new line

        return {"message": "Comments successfully written to file."}

    except TypeError as e:
        raise HTTPException(status_code=500, detail=f"Type error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
