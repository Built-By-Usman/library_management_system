from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import getDb
from models import BorrowReturnModel,BookModel
from ..schemas import BorrowReturnRM,BorrowReturnSchema
from typing import List
from ..oauth2 import get_current_user
from ..repository import returned
from datetime import datetime


def get(id: int, db: Session):
    returnedBooks = db.query(BorrowReturnModel)\
                      .filter(BorrowReturnModel.user_id == id,
                              BorrowReturnModel.status == 'returned')\
                      .all()
    if not returnedBooks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You have not returned any books")
    
    results = []
    for b in returnedBooks:
        results.append({
            "title": b.book.title,
            "author": b.book.author,
            "category": b.book.category,
            "owner": {"name": b.book.owner.name, "email": b.book.owner.email},
            "borrow_date": b.borrow_date,
            "return_date": b.return_date,
            "status": b.status
        })
    return results

def add(request: BorrowReturnSchema, id: int, db: Session):
    # Find the borrow record
    returnedBook = db.query(BorrowReturnModel)\
                     .filter(BorrowReturnModel.user_id == id,
                             BorrowReturnModel.book_id == request.book_id,
                             BorrowReturnModel.status == 'borrowed')\
                     .first()
    
    if not returnedBook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This book is not currently borrowed"
        )

    # Find the actual book
    book = db.query(BookModel).filter(BookModel.id == request.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found in the database"
        )

    # Update borrow record and book copies
    returnedBook.status = 'returned'
    returnedBook.return_date = datetime.utcnow()
    book.copies += 1

    db.commit()
    db.refresh(returnedBook)
    db.refresh(book)

    return {
        "title": book.title,
        "author": book.author,
        "category": book.category,
        "owner": {"name": book.owner.name, "email": book.owner.email},
        "borrow_date": returnedBook.borrow_date,
        "return_date": returnedBook.return_date,
        "status": returnedBook.status
    }

    
    