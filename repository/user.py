from fastapi import HTTPException, status
from models import UserModel
from sqlalchemy.orm import Session
from schemas import UserSchema
from hashing import getHashedPassword
import re

def get(id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    return user

def create(request: UserSchema, db: Session):
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.fullmatch(email_pattern, request.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid email format"
        )

    existing_user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

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
            detail=f"Could not create user: {e}"
        )

def delete(id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

def update(id: int, request: UserSchema, db: Session):
    user_query = db.query(UserModel).filter(UserModel.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.fullmatch(email_pattern, request.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid email format"
        )

    existing_email_user = db.query(UserModel).filter(UserModel.email == request.email, UserModel.id != id).first()
    if existing_email_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    update_data = request.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["password"] = getHashedPassword(update_data["password"])
    else:
        update_data.pop("password", None)

    try:
        user_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(user)
        return {"detail": "User updated successfully", "user": user}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Could not update user: {e}"
        )