from fastapi import HTTPException, status
from models import BookModel, UserModel
from sqlalchemy.orm import Session
from schemas import BookSchema

def all(db: Session):
    books = db.query(BookModel).all()
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books found in the database"
        )
    return books


def create(request: BookSchema, db: Session):
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {request.user_id} not found"
        )


    book = BookModel(
        title=request.title,
        author=request.author,
        ISBN=request.ISBN,
        user_id=request.user_id,
        copies=request.copies,
        category=request.category,
        url=getattr(request, "url", None) 
    )

    try:
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Failed to add book: {e}"
        )


def update(id: int, request: BookSchema, db: Session):
    book_query = db.query(BookModel).filter(BookModel.id == id)
    book = book_query.first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {id} not found"
        )

    # Update the book
    try:
        book_query.update(request.model_dump(), synchronize_session=False)
        db.commit()
        db.refresh(book) 
        return {"detail": f"Book with id {id} updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Failed to update book: {e}"
        )