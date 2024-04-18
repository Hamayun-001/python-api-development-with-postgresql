from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
from typing import Optional

app = FastAPI()

my_posts = [
    {
        "id": 1,
        "title": "post 1 title",
        "content": "post 1 content",
    }
]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome to fastapi-course"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts, "status": 200}


@app.post("/posts")
async def create_post(post: Post):
    new_post = post.model_dump()
    new_post["id"] = randrange(0, 1000000)
    my_posts.append(new_post)
    return {
        "data": new_post,
        "status": 201,
    }


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found.",
        )

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found.",
        )

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    index = find_post_index(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found.",
        )

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
