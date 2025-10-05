# https://www.youtube.com/watch?v=ZXEOw_9h0hg
from fastapi import FastAPI, HTTPException, Path, Depends
from typing import Optional, List, Annotated
from sqlalchemy.orm import Session
from models import Base, User, Post
from database import engine, SessionLocal
from schemas import UserCreate, UserUpdate, PostCreate, PostUpdate,  PostResponse, UserResponse

app = FastAPI()


Base.metadata.create_all(bind=engine)

# In-memory "database"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#-------------------------------------------------------------
# User Endpoints
#-------------------------------------------------------------
@app.get("/users/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[UserResponse]:
    users = db.query(User).offset(skip).limit(limit).all()
    return users    

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    db_user = User(name=user.name, email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db_user.age = user.age
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> dict:
    # Check if the user exists
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if the user has any posts
    if db_user.posts:
        raise HTTPException(status_code=400, detail="Cannot delete user with associated posts")
    # Delete the user
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}


#-------------------------------------------------------------
# Post Endpoints
#-------------------------------------------------------------
@app.get("/posts/", response_model=List[PostResponse])
async def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[PostResponse]:
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostResponse)
async def read_post(post_id: int, db: Session = Depends(get_db)) -> PostResponse:
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    # Check if the author exists
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Author not found")
    # Create the post
    db_post = Post(title=post.title, content=post.content, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)) -> PostResponse:
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = post.title
    db_post.content = post.content
    db_post.author_id = post.author_id
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: int, db: Session = Depends(get_db)) -> dict:
    # Check if the post exists
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # Delete the post
    db.delete(db_post)
    db.commit()
    return {"detail": "Post deleted"}
