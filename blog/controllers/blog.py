from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request, db: Session, current_user):
    new_blog = models.Blog(title=request.title, body=request.body, author=request.author, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_blog_by_id(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    return blog

def update(id: int, request, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    blog.update(request.dict())
    db.commit()
    return request

def delete(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    db.commit()
    return "Deleted Successfully"