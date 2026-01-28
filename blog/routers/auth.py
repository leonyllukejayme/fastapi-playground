from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from .. import schemas, models, hashing, token, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
router = APIRouter(
    tags=["Authentication"]
)
# Additional authentication routes would be defined here

@router.post("/login")
def login(request:Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    if not hashing.Hashing.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")

    # Generate and return token or session info here
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.get('/items')
def read_items(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="login"))]):
    return {"token": token}

# This endpoint returns information about the currently authenticated user.
# It uses dependency injection to get the current user from the oauth2.get_current_user function,
# which typically validates the JWT token and retrieves the user from the database.
@router.get("/me")
def read_current_user(current_user: schemas.ActiveUser = Depends(oauth2.get_current_user)):
    # Return a dictionary with the user's id and email.
    return {
        "id": current_user.id,
        "email": current_user.email,
    }
