from fastapi import HTTPException,status
from models import BookModel,UserModel,BorrowReturnModel
from sqlalchemy.orm import Session
from ..schemas import BookSchema

def all(db:Session):
    books=db.query(BookModel).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No book found in database")
    return books



def get(title:str,db:Session):
    book=db.query(BookModel).where(BookModel.title==title).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No book found with id:{id}")
    return book



def create(request:BookSchema,db:Session):
    user=db.query(UserModel).filter(UserModel.id==request.user_id).first()
    if user:
        book=BookModel(title=request.title,author=request.author,ISBN=request.ISBN,user_id=request.user_id,copies=request.copies,category=request.category)

        try:
            db.add(book)
            db.commit()
            db.refresh(book)
            return book
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Failed to add book:{e}")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{request.user_id} not found")



def delete(id:int, db:Session):
    book = db.query(BookModel).filter(BookModel.id==id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No book found with id:{id}")

    borrow_exists = db.query(BorrowReturnModel).filter(BorrowReturnModel.book_id == id).first()
    if borrow_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete book: it is referenced in BorrowReturn"
        )

    db.delete(book)
    db.commit()
    return {"detail":"book deleted successfully"}

def update(id:int, request:BookSchema, db:Session):
    book = db.query(BookModel).filter(BookModel.id == id)
    if not book:
        raise HTTPException(status_code=404, detail=f"No book found with id:{id}")
    
    update_data = request.dict()
    
    # convert ISBN to string to avoid Flutter type error
    if 'ISBN' in update_data and update_data['ISBN'] is not None:
        update_data['ISBN'] = str(update_data['ISBN'])
    
    book.update(update_data, synchronize_session=False)
    db.commit()
    return {"detail":"book updated successfully"}
