from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas import IssueReturnSchema
from models import IssueReturnModel, BookModel
from datetime import datetime, timedelta


def get_issued_books(user_id: int, db: Session):
    issued_books = (
        db.query(IssueReturnModel)
        .filter(IssueReturnModel.user_id == user_id)
        .filter(IssueReturnModel.status == "issued")
        .all()
    )

    if not issued_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No issued books found for this admin"
        )

    results = []
    for record in issued_books:
        results.append({
            "book_id": record.book_id,
            "title": record.book.title,
            "author": record.book.author,
            "category": record.book.category,
            "owner": {
                "name": record.book.owner.name,
                "email": record.book.owner.email
            },
            "student_id": record.student_id,
            "borrow_date": record.borrow_date,
            "return_date": record.return_date,
            "issue_days": record.issue_days
        })

    return results


def issue_book(request: IssueReturnSchema, db: Session, user_id: int):
    # 1. Validate the book exists
    book = db.query(BookModel).filter(BookModel.id == request.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {request.book_id} not found"
        )

    # 2. Check if copies are available
    if book.copies <= 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No available copies for this book"
        )

    borrow_date = datetime.utcnow()
    return_date = borrow_date + timedelta(days=request.issue_days)

    issued_book = IssueReturnModel(
        user_id=user_id,
        book_id=book.id,
        student_id=request.student_id,
        issue_days=request.issue_days,
        borrow_date=borrow_date,
        return_date=None, 
        status="issued"
    )

    try:
        db.add(issued_book)
        book.copies -= 1
        db.commit()
        db.refresh(issued_book)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to issue book: {str(e)}"
        )

    return {
        "message": "Book issued successfully",
        "book_id": book.id,
        "title": book.title,
        "author": book.author,
        "category": book.category,
        "student_id": request.student_id,
        "issue_days": request.issue_days,
        "borrow_date": issued_book.borrow_date,
        "return_date": issued_book.return_date,
        "owner": {
            "name": book.owner.name,
            "email": book.owner.email
        }
    }