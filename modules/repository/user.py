from fastapi import HTTPException,status
from models import BookModel,UserModel
from sqlalchemy.orm import Session
from ..schemas import UserSchema
from ..hashing import getHashedPassword
import re






def get(id:int,db:Session):
    user=db.query(UserModel).where(UserModel.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No user found with id:{id}")
    return user



def create(request: UserSchema, db: Session):
    emailPattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(emailPattern, request.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Please enter a valid email"
        )

    # Check if user already exists
    existingUser = db.query(UserModel).filter(UserModel.email == request.email).first()
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered"
        )

    # Create new user
    user = UserModel(
        name=request.name,
        email=request.email,
        password=getHashedPassword(request.password)
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Failed to add user: {e}"
        )




def delete(id:int,db:Session):
    user=db.query(UserModel).filter(UserModel.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No user found with id:{id}")
        
    db.delete(user)
    db.commit()
    return {"detail":"User deleted successfully"}

def update(id:int,request:UserSchema,db:Session):
    user=db.query(UserModel).filter(UserModel.id==id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No user found with id:{id}")
    user.update(request.dict(),synchronize_session=False)
    db.commit()
    return {"detail":"User updated successfully"}
