# from fastapi import APIRouter
# from api.scrappers.amazon.comments import get_comments

# router = APIRouter(
#     prefix="/amazon",
#     tags=["amazon"]
# )

# @router.post("/get_comments")
# def get_amazon_comments(url: str, file_name: str):
#     comments = get_comments(url=url)
    
#     with open(file_name, "w") as file:
#         for comment in comments:
#             file.write(comment + "\n")
    
#     return {"message": "Comments successfully written to file."}

from fastapi import APIRouter, HTTPException
from api.scrappers.amazon.comments import get_comments  # Assuming this uses Selenium or similar

router = APIRouter(
    prefix="/amazon",
    tags=["amazon"]
)

@router.post("/get_comments")
def get_amazon_comments(url: str, file_name: str):
    try:
        comments = get_comments(url=url)

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
