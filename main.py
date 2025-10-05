from fastapi import FastAPI, HTTPException, Path
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int

class UserCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=1, max_length=50)]
    email: Annotated[str, Field(max_length=100)]
    age: Annotated[int, Field(ge=1, le=180)]

class Post(BaseModel):
    id: int
    title: str
    content: str
    author: User

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author_id: Optional[int] = None

users: List[User] = [
    User(id=1, name="Alice", email="alice@example.com", age=30),
    User(id=2, name="Bob", email="bob@example.com", age=25),
    User(id=3, name="Charlie", email="charlie@example.com", age=35),
]

posts: List[Post] = [
    Post(id=1, title="First Post", content="This is the first post.", author=users[0]),
    Post(id=2, title="Second Post", content="This is the second post.", author=users[1]),
    Post(id=3, title="Third Post", content="This is the third post.", author=users[2]),
]

@app.get("/posts")
async def get_posts() -> List[Post]:
    return posts

@app.post("/posts/add", status_code=201)
async def add_post(post: PostCreate) -> Post:
    author = next((user for user in users if user.id == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_id = max(p.id for p in posts) + 1 if posts else 1
    new_post = Post(id=new_id, title=post.title, content=post.content, author=author)
    posts.append(new_post)
    return new_post

@app.put("/posts/edit/{post_id}")
async def edit_post(post_id: int, post: PostUpdate) -> Post:  
    for i, p in enumerate(posts):
        if p.id == post_id:
            if post.title is not None:
                p.title = post.title
            if post.content is not None:
                p.content = post.content
            if post.author_id is not None:
                author = next((user for user in users if user.id == post.author_id), None)
                if not author:
                    raise HTTPException(status_code=404, detail="Author not found")
                p.author = author
            posts[i] = p
            return p
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/delete/{post_id}")
async def delete_post(post_id: int) -> None:
    for i, p in enumerate(posts):
        if p.id == post_id:
            posts.pop(i)
            return None
    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/posts/{post_id}")
async def get_post(post_id: Annotated[int, Path(..., ge=1, le=3)]) -> Post:
    for post in posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/search")
async def search_posts(post_id: Optional[int] = None) -> Post:
    if post_id is not None:
        for post in posts:
            if post.id == post_id:
                return post
        raise HTTPException(status_code=404, detail="Post not found")
    raise HTTPException(status_code=400, detail="No post_id provided")

@app.post("/users/add")
async def add_user(user: UserCreate) -> User:
    new_id = max(u.id for u in users) + 1 if users else 1
    new_user = User(id=new_id, **user.model_dump())
    users.append(new_user)
    return new_user