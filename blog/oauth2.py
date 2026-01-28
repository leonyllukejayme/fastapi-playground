from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models
from .database import get_db
from .token import verify_access_token
import jwt
from jwt.exceptions import InvalidTokenError

# Create an instance of OAuth2PasswordBearer, which is used to extract the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency that retrieves the current user based on the provided token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Exception to be raised if credentials are invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Verify the access token and return the user if valid, otherwise raise the exception
    return verify_access_token(token, credentials_exception, db)