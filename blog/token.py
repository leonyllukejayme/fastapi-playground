from datetime import datetime, timedelta, timezone
from fastapi import Depends
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from .database import get_db
from . import models
from . import schemas
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve secret key, algorithm, and token expiration time from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # Create a new access token with an expiration time
    to_encode = data.copy()  # Copy the data to encode
    if expires_delta:
        # If an expiration delta is provided, use it
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration time is 15 minutes
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # Add expiration to the data
    # Encode the JWT token with the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception, db: Session = Depends(get_db)):
    # Verify the provided access token
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Extract the email from the token payload
        if email is None:
            raise credentials_exception  # Raise exception if email is not found
        token_data = schemas.TokenData(email=email)  # Create token data schema
    except InvalidTokenError:
        raise credentials_exception  # Raise exception if token is invalid
    # Query the database for the user with the extracted email
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception  # Raise exception if user is not found
    return user  # Return the user object if found