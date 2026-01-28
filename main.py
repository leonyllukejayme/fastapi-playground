from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
# import uvicorn
app = FastAPI()

class blogModel(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True

@app.get('/')
def read_root():
    return {"message": "Welcome to the Blog API"}

@app.get('/blog/')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"message": f"{limit} published blogs from the db {sort}"}
    else:
        return {"message": f"{limit} blogs from the db"}



@app.get('/blog/unpublished')
def unpublished():
    return {"message": "All unpublished blogs"}

@app.get('/blog/{id}')
def show(id: int):
    return {"blog_id": id}

@app.get('/blog/{id}/comments')
def comments(id: int, limit: int = 100):
    return {"blog_id": id, "comments": limit}

@app.post('/blog/')
def create_blog(blog: blogModel):
    return {"message": f"Blog titled '{blog.title}' has been created"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)



# person = [
#     {"name": "John", "age": 30},
#     {"name": "Jane", "age": 25},
#     {"name": "Doe", "age": 40},
#     {"name": "Alice", "age": 35},
#     {"name": "Bob", "age": 28},
#     {"name": "Charlie", "age": 22},
#     {"name": "David", "age": 45},
#     {"name": "Eve", "age": 29},
#     {"name": "Frank", "age": 33},
#     {"name": "Grace", "age": 27},
#     {"name": "Hank", "age": 31},
#     {"name": "Ivy", "age": 26},
#     {"name": "Jack", "age": 38},
#     {"name": "Kathy", "age": 24},
#     {"name": "Leo", "age": 36},
#     {"name": "Mia", "age": 32},
#     {"name": "Nina", "age": 30}
# ]


# @app.get('/')
# async def index():
#     return {"message": "Hello, World!"}

# @app.get('/person')
# async def get_person():
#     return person

# @app.get('/person/{name}')
# async def get_person_by_name(name: str):
#     for p in person:
#         if p['name'].lower() == name.lower():
#             return p
#     return {"error": "Person not found"}   

# @app.get('/person/items/')
# async def read_item(skip: int = 0, limit: int = 10):
#     return person[skip: skip + limit]