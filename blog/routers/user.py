from fastapi import APIRouter, Depends ,status
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..controllers import user as userController

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
  return userController.create_user(request,db)

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowUserWithBlogs)
def get_user(id: int,db: Session = Depends(get_db)):
    return userController.get_user_by_id(id, db)

