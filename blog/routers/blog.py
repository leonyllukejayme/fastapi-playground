from fastapi import APIRouter, Depends ,status
from .. import schemas, models,oauth2
from ..database import engine , get_db
from sqlalchemy.orm import Session
from typing import List
from ..controllers import blog as blogController

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


# Endpoint to retrieve all blogs
# This function is called when a GET request is made to the "/blog/" route.
# It depends on the database session and the current user for authorization.
@router.get("/", response_model=List[schemas.BlogPost])
def all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogController.get_all(db)

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def blog(id: int,db: Session = Depends(get_db)):
    return blogController.get_blog_by_id(id, db)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.BlogPost)
def create(request: schemas.BlogPost, db: Session = Depends(get_db), current_user: schemas.ActiveUser = Depends(oauth2.get_current_user)):
    return blogController.create(request, db, current_user)


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.BlogPost, db: Session = Depends(get_db)):
    return blogController.update(id, request, db)   

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    return blogController.delete(id, db)
