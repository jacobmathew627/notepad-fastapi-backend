"""
Security Utilities for Authentication.
Provides functions for password hashing, validation, and JWT creation.
"""
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password:str):
    if not isinstance(password,str):
        raise ValueError("Password must be a string")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long")
    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at most {MAX_PASSWORD_LENGTH} characters long")

def hash_password(password:str):
    validate_password(password)
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    
    to_encode = data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)
    return encoded_jwt

