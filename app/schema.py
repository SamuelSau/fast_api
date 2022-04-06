from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase): #inheritance, request from client to database
    pass

#response
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

#This is a response (database to client)
class Post(PostBase): #reference pydantic documentation to define our schemas, basically what data can be strictly sent back from client to database (request) then from database to client (response)
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel): #response for our model with votes to the client
    Post: Post
    votes: int

#request
class UserCreate(BaseModel):
    email: EmailStr
    password: str


#request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
    