from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from modules.database import Base
from datetime import datetime


class UserModel(Base):
    __tablename__="users"
    id=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)


    books=relationship("BookModel",back_populates="owner")

class BookModel(Base):
    __tablename__="books"
    id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String)
    author=Column(String)
    category=Column(String)
    ISBN=Column(String)
    copies=Column(Integer)
    user_id:int

    user_id=Column(Integer,ForeignKey("users.id"))
    owner=relationship("UserModel",back_populates="books")



class BorrowReturnModel(Base):
    __tablename__="BorrowReturn"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    book_id=Column(Integer,ForeignKey("books.id"))
    status=Column(String,default="borrowed")
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)


    user=relationship("UserModel")
    book=relationship("BookModel")
    

