from pydantic import BaseModel

#-------------------------------------------------------------
# User Schemas
#-------------------------------------------------------------
class UserBase(BaseModel):
    name: str
    email: str
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

#-------------------------------------------------------------
# Post Schemas
#-------------------------------------------------------------
class PostBase(BaseModel):
    title: str
    content: str
    author_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    class Config:
        orm_mode = True