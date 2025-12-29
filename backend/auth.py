from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from models import UserDB
from database import get_db
from sqlalchemy.orm import Session
from config import SECRET_KEY, ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user_id(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
def get_current_user(
        user_id:int = Depends(get_current_user_id),
        db:Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

