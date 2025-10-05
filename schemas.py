# this file contains Pydantic models (schemas) for request and response validation
 
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

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

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

class PostResponse(PostBase):
    id: int
    author: UserResponse
    class Config:
        from_attributes = True
