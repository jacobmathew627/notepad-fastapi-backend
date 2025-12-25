from pydantic import BaseModel
from typing import Optional
from datetime import datetime 

class UserCreate(BaseModel):
    username: str
    email : str
    password : str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id : int
    username : str
    email : str
    created_at : datetime

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title : str
    description : Optional[str] = None
    due_date :Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str]=None
    description:Optional[str]=None 
    status : Optional[str]=None
    due_date: Optional[datetime]=None

class TaskResponse(BaseModel):
    id : int
    title : str 
    description : Optional[str]
    status : str
    due_date : Optional[datetime]
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True

