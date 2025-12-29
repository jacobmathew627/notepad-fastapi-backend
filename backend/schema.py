from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from models import TaskStatus

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in [TaskStatus.pending.value, TaskStatus.completed.value]:
            raise ValueError(f"Status must be one of: {TaskStatus.pending.value}, {TaskStatus.completed.value}")
        return v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AIParseRequest(BaseModel):
    text: str

class AIParseResponse(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    confidence: float  # 0.0 to 1.0

class PrioritySuggestion(BaseModel):
    suggestions: List[str]
    reasoning: str
    total_pending: int

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
