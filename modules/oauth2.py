from fastapi import HTTPException,Depends,status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from .JWTtoken import verifyToken
from sqlalchemy.orm import Session
from .database import getDb
from models import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(getDb)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verifyToken(credentials_exception, token) 
    user = db.query(UserModel).filter(UserModel.email == token_data.email).first()
    if not user:
        raise credentials_exception
    return user
    