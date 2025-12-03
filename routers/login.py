from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from modules.database import getDb
from models import UserModel
from modules.schemas import LoginSchema,Token
from modules.hashing import verifyPassword
from modules.JWTtoken import create_access_token
from fastapi.security import  OAuth2PasswordRequestForm



router=APIRouter(
    tags=['Authentication'],
    prefix='/login'
)


@router.post('/')
def login(request: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(getDb)):
    user=db.query(UserModel).filter(UserModel.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Invalid credentials")
    if not verifyPassword(plainPassword=request.password,hashedPassword=user.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


