from typing import List, Optional
from pydantic import BaseModel

# User model representing a user with name, email, and password
class User(BaseModel):
    name: str
    email: str
    password: str

# ActiveUser model representing a user that is currently active with an id and email
class ActiveUser(BaseModel):
    id: int
    email: str

# BlogPost model representing a blog post with title, body, and author
class BlogPost(BaseModel):
    title: str
    body: str
    author: str

# ShowUser model for displaying user information without sensitive data
class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True  # Enables compatibility with ORM models

# ShowUserWithBlogs extends ShowUser to include a list of blogs
class ShowUserWithBlogs(ShowUser):
    blogs: List[BlogPost] = []  # Default to an empty list of blogs

    class Config():
        orm_mode = True  # Enables compatibility with ORM models

# ShowBlog model for displaying a blog post along with user information
class ShowBlog(BlogPost):
    users: ShowUser  # Includes user information

    class Config():
        orm_mode = True  # Enables compatibility with ORM models

# Login model for user authentication with username and password
class Login(BaseModel):
    username: str
    password: str

# Token model representing an access token and its type
class Token(BaseModel):
    access_token: str
    token_type: str

# TokenData model for storing token-related data, such as email
class TokenData(BaseModel):
    email: Optional[str] | None = None  # Email can be None or a string