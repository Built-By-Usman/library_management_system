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

def update(id: int, request: UserSchema, db: Session):
    # Check if user exists
    user_query = db.query(UserModel).filter(UserModel.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with id: {id}"
        )

    # Validate email
    emailPattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.fullmatch(emailPattern, request.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Please enter a valid email"
        )

    # Check if email already exists for a different user
    existing_email_user = (
        db.query(UserModel)
        .filter(UserModel.email == request.email)
        .filter(UserModel.id != id)
        .first()
    )
    if existing_email_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered"
        )

    # Prepare updated data
    update_data = request.dict(exclude_unset=True)  # optional fields are ignored
    if "password" in update_data and update_data["password"]:
        # Hash the new password
        update_data["password"] = getHashedPassword(update_data["password"])
    else:
        # Remove password key if empty so it doesn't overwrite old password
        update_data.pop("password", None)

    # Update user
    try:
        user_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(user)
        return {"detail": "User updated successfully", "user": user}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Failed to update user: {e}"
        )
