from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import IssueReturnModel, BookModel
from schemas import ReturnSchema, IssueReturnRM
from datetime import datetime

def get(id: int, db: Session):
    returned_books = db.query(IssueReturnModel)\
                       .filter(
                           IssueReturnModel.user_id == id,
                           IssueReturnModel.status == 'returned'
                       ).all()

    if not returned_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} has not returned any books"
        )

    results = []
    for record in returned_books:
        results.append(
            IssueReturnRM(
                title=record.book.title,
                author=record.book.author,
                category=record.book.category,
                book_id=record.book_id,
                student_id=record.student_id,
                borrow_date=record.borrow_date,
                return_date=record.return_date,
                owner=record.book.owner,
                issue_days=record.issue_days
            )
        )

    return results


def add(request: ReturnSchema, id: int, db: Session):
    issued_record = db.query(IssueReturnModel)\
                      .filter(
                          IssueReturnModel.user_id == id,
                          IssueReturnModel.book_id == request.book_id,
                          IssueReturnModel.status == 'issued'
                      ).first()

    if not issued_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {request.book_id} is not currently borrowed by user {id}"
        )

    book = db.query(BookModel).filter(BookModel.id == request.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {request.book_id} not found in the database"
        )

    issued_record.status = 'returned'
    issued_record.return_date = datetime.utcnow()
    book.copies += 1

    db.commit()
    db.refresh(issued_record)
    db.refresh(book)

    return IssueReturnRM(
        title=book.title,
        author=book.author,
        category=book.category,
        book_id=book.id,
        student_id=issued_record.student_id,
        borrow_date=issued_record.borrow_date,
        return_date=issued_record.return_date,
        owner=book.owner,
        issue_days=issued_record.issue_days
    )