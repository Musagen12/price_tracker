from fastapi import APIRouter, HTTPException
from . import schemas
from api.scrappers.amazon.comments import get_comments  
from api.scrappers.amazon.search import amazon_search

router = APIRouter(
    prefix="/amazon",
    tags=["Amazon"]
)

# @router.post("/search")
# def search(search_input: schemas.SearchInput):
#     query = search_input.query
#     product_data = amazon_search(query)
#     response = schemas.ProductList(**product_data)
#     return response

@router.post("/search")
def search(search_input: schemas.SearchInput):
    query = search_input.query
    product_list = amazon_search(query)
    return product_list


@router.post("/get_comments")
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
