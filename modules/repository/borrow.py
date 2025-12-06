from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from ..schemas import BorrowReturnSchema
from models import BorrowReturnModel,BookModel


def get(id:int,db:Session):
    borrowedBooks=db.query(BorrowReturnModel).filter(BorrowReturnModel.user_id==id).filter(BorrowReturnModel.status=='borrowed').all()
    if not borrowedBooks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You donot borrowed any book")
    else:
        results=[]
        for b in borrowedBooks:
            results.append({
            "title": b.book.title,
            "author": b.book.author,
            "category":b.book.category,
            'book_id':b.book_id,
            "owner":b.book.owner,
            "borrow_date": b.borrow_date,
            "return_date": b.return_date,
            "status": b.status})

        return results

    

def create(request:BorrowReturnSchema,db:Session,user_id:int):
    book=db.query(BookModel).filter(BookModel.id==request.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Desired book not found in database")
    if book.copies<=0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="All copies of this book are already borrowed")
    
    borrowedBook=BorrowReturnModel(
     user_id=user_id,
     book_id=book.id
    )
    db.add(borrowedBook)
    book.copies-=1
    db.commit()
    db.refresh(borrowedBook)
    return {
        "title": book.title,
        "author": book.author,
        "category": book.category,
        "owner": {"name": book.owner.name, "email": book.owner.email},
        "borrow_date": borrowedBook.borrow_date,
        "return_date": borrowedBook.return_date
    }