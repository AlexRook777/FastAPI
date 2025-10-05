# this file contains Pydantic models (schemas) for request and response validation
 
from pydantic import BaseModel, Field, EmailStr

#-------------------------------------------------------------
# User Schemas
#-------------------------------------------------------------
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., gt=0, le=120)

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
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10)
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
