from sqlalchemy import Column,Integer,String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    author = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User",back_populates="blogs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    # blog_id = Column(Integer, ForeignKey("blogs.id"))

    blogs = relationship("Blog", back_populates="users")